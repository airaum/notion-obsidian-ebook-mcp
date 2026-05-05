"""Notion API 블록 빌더 — 전자책 표준 템플릿용"""


def rich_text(content: str, bold: bool = False, link: str = None) -> dict:
    rt = {"type": "text", "text": {"content": content}}
    if bold:
        rt["annotations"] = {"bold": True}
    if link:
        rt["text"]["link"] = {"url": link}
    return rt


def toc_block() -> dict:
    return {"object": "block", "type": "table_of_contents", "table_of_contents": {"color": "default"}}


def divider_block() -> dict:
    return {"object": "block", "type": "divider", "divider": {}}


def heading2_block(text: str) -> dict:
    return {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [rich_text(text)]}}


def heading3_block(text: str) -> dict:
    return {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [rich_text(text)]}}


def paragraph_block(text: str) -> dict:
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [rich_text(text)]}}


def callout_block(text: str, icon: str = "💡", color: str = "blue_background") -> dict:
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [rich_text(text)],
            "icon": {"type": "emoji", "emoji": icon},
            "color": color,
        },
    }


def github_link_block(url: str) -> dict:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [rich_text("GitHub", link=url)]},
    }


def table_block(rows: list[list[str]], has_header: bool = True) -> dict | None:
    if not rows or not rows[0]:
        return None
    table_width = len(rows[0])
    table_rows = []
    for row in rows:
        # 열 수가 맞지 않으면 패딩
        padded = row + [""] * (table_width - len(row))
        cells = [[rich_text(cell)] for cell in padded[:table_width]]
        table_rows.append({
            "object": "block",
            "type": "table_row",
            "table_row": {"cells": cells},
        })
    return {
        "object": "block",
        "type": "table",
        "table": {
            "table_width": table_width,
            "has_column_header": has_header,
            "has_row_header": False,
            "children": table_rows,
        },
    }


def code_block(code: str, language: str = "bash") -> dict:
    return {
        "object": "block",
        "type": "code",
        "code": {
            "language": language,
            "rich_text": [rich_text(code)],
        },
    }


def bulleted_item(text: str) -> dict:
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": [rich_text(text)]},
    }


def numbered_item(text: str) -> dict:
    return {
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {"rich_text": [rich_text(text)]},
    }


def toggle_block(title: str, children: list[dict]) -> dict:
    return {
        "object": "block",
        "type": "toggle",
        "toggle": {
            "rich_text": [rich_text(title)],
            "children": [c for c in children if c is not None],
        },
    }


def copyright_blocks() -> list[dict]:
    return [
        divider_block(),
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    rich_text("본 전자책의 저작권은 "),
                    rich_text("airaum", bold=True),
                    rich_text("에 있습니다. 무단 복제 및 재배포를 금지합니다."),
                ]
            },
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [rich_text("Copyright © airaum All Rights Reserved.", bold=True)]
            },
        },
    ]


_CODE_PREFIXES = (
    "```", "$", "npm", "pip", "git", "python", "node", "cargo", "curl",
    "claude", "npx", "/plugin", "obscura", "tar ", "cd ", "echo ",
    "where ", "./", "{", "}", "#", '"',
)


def _is_code_line(text: str) -> bool:
    s = text.strip()
    return bool(s) and any(s.startswith(p) for p in _CODE_PREFIXES)


def _step_to_blocks(step_num: int, step: str) -> list[dict]:
    """한 설치 단계를 prose/code 혼합 블록으로 변환"""
    blocks: list[dict] = [paragraph_block(f"STEP {step_num}")]
    prose_buf: list[str] = []
    code_buf: list[str] = []

    for raw_line in step.split("\n"):
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped:
            if code_buf:
                blocks.append(code_block("\n".join(code_buf)))
                code_buf = []
            if prose_buf:
                blocks.append(paragraph_block(" ".join(prose_buf)))
                prose_buf = []
            continue

        if _is_code_line(stripped):
            if prose_buf:
                blocks.append(paragraph_block(" ".join(prose_buf)))
                prose_buf = []
            code_buf.append(stripped)
        else:
            if code_buf:
                blocks.append(code_block("\n".join(code_buf)))
                code_buf = []
            prose_buf.append(stripped)

    if code_buf:
        blocks.append(code_block("\n".join(code_buf)))
    if prose_buf:
        blocks.append(paragraph_block(" ".join(prose_buf)))

    return blocks


def build_ebook_blocks(
    intro: str,
    github_url: str,
    what_is_it: str,
    why_needed: list[list[str]],
    features: list[list[str]],
    install_steps: list[str],
    usage_examples: list[str],
    fits_well: list[str],
    fits_less: list[str],
    warning_text: str,
    summary_lines: list[str],
) -> list[dict]:
    blocks: list[dict] = []

    # 목차
    blocks.append(toc_block())
    blocks.append(divider_block())

    # 인트로 callout (파란색 통일)
    if intro:
        blocks.append(callout_block(intro, "💡", "blue_background"))

    # GitHub 링크
    if github_url:
        blocks.append(github_link_block(github_url))

    blocks.append(divider_block())

    # 이게 뭔가?
    blocks.append(heading2_block("이게 뭔가?"))
    if what_is_it:
        blocks.append(paragraph_block(what_is_it))

    # 왜 필요한가?
    if why_needed:
        blocks.append(heading2_block("왜 필요한가?"))
        tbl = table_block(why_needed)
        if tbl:
            blocks.append(tbl)

    # 핵심 기능
    if features:
        blocks.append(heading2_block("핵심 기능"))
        tbl = table_block(features)
        if tbl:
            blocks.append(tbl)

    # 설치 방법 (Toggle 제거 → 바로 표시)
    if install_steps:
        blocks.append(heading2_block("📦 설치 방법"))
        for i, step in enumerate(install_steps, 1):
            blocks.extend(_step_to_blocks(i, step))
        blocks.append(divider_block())

    # 실전 활용 (Toggle 제거 → 바로 표시)
    if usage_examples:
        blocks.append(heading2_block("💻 실전 활용"))
        for example in usage_examples:
            if _is_code_line(example):
                blocks.append(code_block(example.strip()))
            else:
                blocks.append(bulleted_item(example))

    # 잘/덜 맞는 경우 표
    if fits_well or fits_less:
        blocks.append(heading2_block("언제 잘 맞고, 언제 안 맞나"))
        max_len = max(len(fits_well), len(fits_less))
        rows = [["잘 맞는 경우", "덜 맞는 경우"]]
        for i in range(max_len):
            well = fits_well[i] if i < len(fits_well) else ""
            less = fits_less[i] if i < len(fits_less) else ""
            rows.append([well, less])
        tbl = table_block(rows)
        if tbl:
            blocks.append(tbl)

    # 주의사항 callout (노란색)
    if warning_text:
        blocks.append(callout_block(warning_text, "⚠️", "yellow_background"))

    # 핵심 3줄 요약 callout (초록색)
    if summary_lines:
        summary_text = "핵심 3줄 요약\n" + "\n".join(
            f"{i + 1}. {line}" for i, line in enumerate(summary_lines)
        )
        blocks.append(callout_block(summary_text, "💡", "green_background"))

    # 저작권
    blocks.extend(copyright_blocks())

    return [b for b in blocks if b is not None]
