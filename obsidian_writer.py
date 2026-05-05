"""옵시디언 마크다운 전자책 저장기"""

import os
from datetime import datetime


def _table_md(rows: list[list[str]]) -> list[str]:
    if not rows or len(rows) < 2:
        return []
    lines = []
    header = rows[0]
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * len(header)) + " |")
    for row in rows[1:]:
        lines.append("| " + " | ".join(row) + " |")
    return lines


def to_markdown(
    title: str,
    icon: str,
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
    tags: list[str],
) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    lines: list[str] = []

    # Frontmatter
    lines += [
        "---",
        f"date: {today}",
        "tags:",
        "  - 전자책",
        "  - notion",
    ]
    for tag in tags:
        lines.append(f"  - {tag}")
    if github_url:
        lines.append(f"github_link: {github_url}")
    lines += ["관련노트: []", "---", ""]

    # 제목
    lines += [f"# {icon} {title}", ""]

    # 인트로 callout
    if intro:
        lines.append("> [!info] 소개")
        for line in intro.splitlines():
            lines.append(f"> {line}")
        lines.append("")

    # GitHub 링크
    if github_url:
        lines += [f"[GitHub]({github_url})", ""]

    lines.append("---")
    lines.append("")

    # 이게 뭔가?
    lines += ["## 이게 뭔가?", "", what_is_it, ""]

    # 왜 필요한가?
    if why_needed and len(why_needed) > 1:
        lines += ["## 왜 필요한가?", ""]
        lines += _table_md(why_needed)
        lines.append("")

    # 핵심 기능
    if features and len(features) > 1:
        lines += ["## 핵심 기능", ""]
        lines += _table_md(features)
        lines.append("")

    # 설치 방법
    if install_steps:
        lines += ["## 📦 설치 방법", ""]
        for i, step in enumerate(install_steps, 1):
            lines.append(f"**STEP {i}**")
            lines.append("")
            lines.append(step)
            lines.append("")

    # 실전 활용
    if usage_examples:
        lines += ["## 💻 실전 활용", ""]
        for example in usage_examples:
            lines.append(f"- {example}")
        lines.append("")

    # 잘/덜 맞는 경우
    if fits_well or fits_less:
        lines += ["## 언제 잘 맞고, 언제 안 맞나", ""]
        max_len = max(len(fits_well), len(fits_less))
        rows = [["잘 맞는 경우", "덜 맞는 경우"]]
        for i in range(max_len):
            well = fits_well[i] if i < len(fits_well) else ""
            less = fits_less[i] if i < len(fits_less) else ""
            rows.append([well, less])
        lines += _table_md(rows)
        lines.append("")

    # 주의사항
    if warning_text:
        lines.append("> [!warning] 주의사항")
        for line in warning_text.splitlines():
            lines.append(f"> {line}")
        lines.append("")

    # 핵심 3줄 요약
    if summary_lines:
        lines.append("> [!tip] 핵심 3줄 요약")
        for i, line in enumerate(summary_lines, 1):
            lines.append(f"> {i}. {line}")
        lines.append("")

    # 저작권
    lines += [
        "---",
        "",
        "본 전자책의 저작권은 **airaum**에 있습니다. 무단 복제 및 재배포를 금지합니다.",
        "**Copyright © airaum All Rights Reserved.**",
    ]

    return "\n".join(lines)


def save_to_obsidian(
    title: str,
    content: str,
    base_path: str = "D:/내프로젝트폴더/space/전자책",
) -> str:
    os.makedirs(base_path, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    safe_title = "".join(c for c in title if c not in r'\/:*?"<>|')
    filename = f"{today}_{safe_title}.md"
    filepath = os.path.join(base_path, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath
