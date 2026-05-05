# 노션+옵시디언 전자책 자동화 MCP

Claude Code에서 말 한마디로 노션 페이지와 옵시디언 파일을 동시에 생성하는 MCP 서버.

---

## 이런 게 됩니다

공부한 내용, 정리한 자료, 툴 사용법 같은 걸 Claude Code에 설명하면 알아서 전자책 형식으로 만들어줍니다.

```
"오늘 공부한 MCP 개발 내용 전자책으로 정리해줘"
"Claude Code 사용법 정리해서 노션에 전자책으로 저장해줘"
"전자책 목록 보여줘"
```

노션에는 목차·표·Callout이 갖춰진 페이지로, 옵시디언에는 .md 파일로 동시에 저장됩니다.

---

## 현재 버전 (v1.1.0)

| 도구 | 기능 |
|------|------|
| `create_ebook` | 노션 + 옵시디언 동시 생성 |
| `list_ebooks` | 저장된 전자책 목록 + 노션 URL 조회 |
| `read_ebook_content` | 기존 전자책 내용 확인 |

---

## 자동으로 만들어지는 구조

| 섹션 | 내용 |
|------|------|
| 목차 | 전체 섹션 자동 링크 |
| 인트로 | 파란 Callout — 소개 |
| 이게 뭔가? | 한 단락 설명 |
| 왜 필요한가? | 표 (상황/원인/해결) |
| 핵심 기능 | 표 (기능/설명) |
| 설치 방법 | 단계별 코드 |
| 실전 활용 | 예시 리스트 |
| 잘/덜 맞는 경우 | 비교 표 |
| 주의사항 | 노란 Callout |
| 핵심 3줄 요약 | 초록 Callout |
| 저작권 | 고정 마지막 섹션 |

---

## 설치 방법

**Claude Code(또는 확장 프로그램)에 아래 URL을 붙여넣고 "이거 설치해줘"라고 하면 됩니다.**

```
https://github.com/airaum/notion-obsidian-ebook-mcp
```

Claude가 clone, 라이브러리 설치까지 알아서 해줍니다.

---

설치 과정에서 아래 3가지는 직접 준비해야 합니다.

**1. 노션 토큰**
- [notion.so/my-integrations](https://www.notion.so/my-integrations) → New integration → 토큰 복사
- 전자책 저장할 노션 페이지 우측 상단 `···` → Connections → 내 integration 연결

**2. 노션 페이지 ID**
- 전자책을 저장할 노션 페이지 URL의 마지막 32자리
- 예: `notion.so/My-Page-3505443bd8f880ff969af6d67642b56b` → `3505443b-d8f8-80ff-969a-f6d67642b56b`

**3. 옵시디언 폴더 경로**
- .md 파일을 저장할 옵시디언 내부 폴더 경로
- 예: `D:/Obsidian/전자책`

준비된 값 3개를 `config.example.py`를 복사해 만든 `config.py`에 채워넣으면 됩니다.

---

### 설치 확인

Claude Code 재시작 후:

```
전자책 목록 보여줘
```

목록이 반환되면 성공입니다.

---

## 사용 예시

```
"RAG 시스템 공부한 내용 전자책으로 만들어줘"
"이 노션 전자책 내용 확인해줘: https://www.notion.so/..."
"지금까지 만든 전자책 목록 보여줘"
"Claude Code 프롬프트 작성법 전자책으로 정리해줘"
```

---

## 주의사항

- 노션 integration을 대상 페이지에 연결하지 않으면 생성이 실패합니다.
- `config.py`에 토큰이 들어있으므로 GitHub에 올리지 마세요. (`.gitignore`에 포함되어 있음)
- 스캔된 이미지 PDF는 지원하지 않습니다.
- Claude Code 재시작 후 MCP가 연결됩니다.

---

## 라이선스

MIT License — Copyright © 2026 airaum
