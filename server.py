"""노션 + 옵시디언 전자책 자동 생성 MCP 서버"""

import sys
import os

# Claude Code가 어느 디렉토리에서 실행하든 모듈을 찾을 수 있도록
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp.server.fastmcp import FastMCP
from notion_client import Client

from notion_builder import build_ebook_blocks
from obsidian_writer import to_markdown, save_to_obsidian

# ── 설정 ──────────────────────────────────────────────────────
# 우선순위: 환경변수 > config.py > 오류
try:
    from config import NOTION_TOKEN, PARENT_PAGE_ID, OBSIDIAN_PATH
except ImportError:
    NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
    PARENT_PAGE_ID = os.getenv("NOTION_PARENT_PAGE_ID", "")
    OBSIDIAN_PATH = os.getenv("OBSIDIAN_PATH", "")

notion = Client(auth=NOTION_TOKEN)
mcp = FastMCP("notion-obsidian-ebook-mcp")


# ── 내부 헬퍼 ─────────────────────────────────────────────────

def _create_notion_page(title: str, icon: str, blocks: list) -> dict:
    page = notion.pages.create(
        parent={"page_id": PARENT_PAGE_ID},
        icon={"type": "emoji", "emoji": icon},
        properties={
            "title": {"title": [{"type": "text", "text": {"content": title}}]}
        },
    )
    # Notion API는 한 번에 100블록 제한
    for i in range(0, len(blocks), 100):
        batch = [b for b in blocks[i : i + 100] if b is not None]
        if batch:
            notion.blocks.children.append(page["id"], children=batch)
    return page


def _format_page_id(raw: str) -> str:
    pid = raw.strip().replace("-", "").replace("https://www.notion.so/", "").replace("https://notion.so/", "")
    # URL 형식에서 마지막 32자리만 추출
    pid = pid[-32:] if len(pid) >= 32 else pid
    if len(pid) == 32:
        return f"{pid[:8]}-{pid[8:12]}-{pid[12:16]}-{pid[16:20]}-{pid[20:]}"
    return raw


# ── MCP 도구 ──────────────────────────────────────────────────

@mcp.tool()
def create_ebook(
    title: str,
    icon: str = "📘",
    intro: str = "",
    github_url: str = "",
    what_is_it: str = "",
    why_needed: list[list[str]] = [],
    features: list[list[str]] = [],
    install_steps: list[str] = [],
    usage_examples: list[str] = [],
    fits_well: list[str] = [],
    fits_less: list[str] = [],
    warning_text: str = "",
    summary_lines: list[str] = [],
    tags: list[str] = [],
) -> str:
    """노션 + 옵시디언에 전자책을 동시 생성합니다.

    Args:
        title: 전자책 제목
        icon: 이모지 아이콘 (예: 📘, 🛡️, ⭐)
        intro: 인트로 소개 문구 (파란 callout에 들어감)
        github_url: GitHub 링크 URL (없으면 빈 문자열)
        what_is_it: '이게 뭔가?' 섹션 한 단락 설명
        why_needed: 왜 필요한가 표. [[헤더1, 헤더2, 헤더3], [행...], ...]
        features: 핵심 기능 표. [[헤더1, 헤더2], [행...], ...]
        install_steps: 설치 단계 리스트 (Toggle 안에 들어감)
        usage_examples: 실전 활용 예시 리스트 (Toggle 안에 들어감)
        fits_well: 잘 맞는 경우 리스트
        fits_less: 덜 맞는 경우 리스트
        warning_text: 주의사항 callout (노란색). 없으면 빈 문자열
        summary_lines: 핵심 3줄 요약 (3개 항목 리스트)
        tags: 옵시디언 태그 리스트
    """
    try:
        blocks = build_ebook_blocks(
            intro, github_url, what_is_it, why_needed, features,
            install_steps, usage_examples, fits_well, fits_less,
            warning_text, summary_lines,
        )

        page = _create_notion_page(title, icon, blocks)
        notion_url = page["url"]

        md_content = to_markdown(
            title, icon, intro, github_url, what_is_it,
            why_needed, features, install_steps, usage_examples,
            fits_well, fits_less, warning_text, summary_lines, tags,
        )
        obsidian_path = save_to_obsidian(title, md_content, OBSIDIAN_PATH)

        return (
            f"전자책 생성 완료!\n"
            f"노션: {notion_url}\n"
            f"옵시디언: {obsidian_path}"
        )

    except Exception as e:
        return f"오류 발생: {type(e).__name__}: {e}"


@mcp.tool()
def list_ebooks() -> str:
    """클로드 전자책 모음 페이지의 전자책 목록을 조회합니다."""
    try:
        response = notion.blocks.children.list(block_id=PARENT_PAGE_ID)
        books = []
        for block in response.get("results", []):
            if block.get("type") == "child_page":
                book_title = block.get("child_page", {}).get("title", "제목 없음")
                bid = block["id"].replace("-", "")
                url = f"https://www.notion.so/{bid}"
                books.append(f"- {book_title}: {url}")
        if books:
            return "현재 전자책 목록:\n" + "\n".join(books)
        return "등록된 전자책이 없습니다."
    except Exception as e:
        return f"오류: {type(e).__name__}: {e}"


@mcp.tool()
def read_ebook_content(page_id_or_url: str) -> str:
    """기존 전자책의 텍스트 내용을 추출합니다. fix_ebook 작업 전 내용 확인용.

    Args:
        page_id_or_url: 노션 페이지 ID 또는 URL
    """
    try:
        pid = _format_page_id(page_id_or_url)
        page = notion.pages.retrieve(pid)
        title_prop = page.get("properties", {}).get("title", {}).get("title", [])
        title = title_prop[0]["text"]["content"] if title_prop else "제목 없음"

        blocks_response = notion.blocks.children.list(block_id=pid)
        sections: list[str] = [f"제목: {title}", ""]

        for block in blocks_response.get("results", []):
            btype = block.get("type", "")
            content = block.get(btype, {})
            rt = content.get("rich_text", [])
            text = "".join(t.get("text", {}).get("content", "") for t in rt)

            if btype in ("heading_1", "heading_2", "heading_3"):
                sections.append(f"\n## {text}")
            elif btype == "paragraph" and text:
                sections.append(text)
            elif btype == "callout" and text:
                sections.append(f"[callout] {text}")
            elif btype == "toggle" and text:
                sections.append(f"[toggle] {text}")
            elif btype == "code" and text:
                sections.append(f"```\n{text}\n```")

        return "\n".join(sections)

    except Exception as e:
        return f"오류: {type(e).__name__}: {e}"


if __name__ == "__main__":
    mcp.run()
