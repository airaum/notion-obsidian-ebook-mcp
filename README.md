# 노션+옵시디언 전자책 자동화 MCP

Claude Code에서 말 한마디로 노션 페이지와 옵시디언 파일을 동시에 생성하는 MCP 서버.

표지·목차·표·Callout이 갖춰진 전자책 형식으로 — 코드 없이 Claude에게 말만 하면 됩니다.

---

## 이런 게 됩니다

```
"Claude Code 프롬프트 최적화 전자책 만들어줘"
"MCP 개발 입문 가이드 전자책으로 정리해줘"
"전자책 목록 보여줘"
"이 노션 페이지 내용 확인해줘 [URL]"
```

→ Claude Code가 노션 + 옵시디언에 동시 저장합니다. 직접 노션에서 만들 필요 없음.

---

## 현재 버전 (v1.1.0) — 사용 가능

| 도구 | 기능 |
|------|------|
| `create_ebook` | 노션 페이지 + 옵시디언 .md 동시 생성 |
| `list_ebooks` | 저장된 전자책 목록 + 노션 URL 조회 |
| `read_ebook_content` | 기존 전자책 텍스트 내용 추출 |

### 자동 생성되는 전자책 구조

| 섹션 | 내용 |
|------|------|
| 목차 | 전체 섹션 자동 링크 |
| 인트로 | 파란 Callout — 소개 문구 |
| 이게 뭔가? | 한 단락 설명 |
| 왜 필요한가? | 표 형식 (상황/원인/해결) |
| 핵심 기능 | 표 형식 (기능/설명) |
| 설치 방법 | 단계별 코드 포함 |
| 실전 활용 | 예시 리스트 |
| 잘/덜 맞는 경우 | 2열 비교 표 |
| 주의사항 | 노란 Callout |
| 핵심 3줄 요약 | 초록 Callout |
| 저작권 | 고정 마지막 섹션 |

---

## 로드맵 — 업데이트 예정

### v1.2.0 — 전자책 수정 기능

| 도구 | 기능 |
|------|------|
| `fix_ebook` | 기존 노션 페이지를 새 내용으로 덮어쓰기 |

현재는 수정 시 새 페이지를 만들고 구버전을 수동 삭제해야 합니다. `fix_ebook`이 추가되면 기존 페이지를 직접 업데이트합니다.

### v1.3.0 — 분류 + 검색

- 카테고리별 서브페이지 자동 분류 (AI 도구 / MCP / 개발 도구 등)
- 제목·태그로 전자책 검색하는 `search_ebooks` 도구
- 옵시디언 MOC 노트에 자동 링크 추가

### v2.0.0 — 콘텐츠 자동 생성

- 주제만 입력하면 각 섹션 내용까지 Claude가 자동으로 채워서 전자책 완성
- 전자책 → PDF 변환 파이프라인

---

## 설치 방법 (v1.1.0)

### 사전 조건 확인

```powershell
python --version   # 3.10 이상 필요
pip --version
git --version
```

### STEP 1: 다운로드

```powershell
git clone https://github.com/airaum/notion-obsidian-ebook-mcp.git
cd notion-obsidian-ebook-mcp
```

### STEP 2: 라이브러리 설치

```powershell
pip install -r requirements.txt
```

### STEP 3: config.py 설정

`config.example.py`를 복사해 `config.py`로 저장한 뒤 아래 3가지를 채웁니다.

```python
NOTION_TOKEN = "ntn_..."          # notion.so/my-integrations 에서 발급
PARENT_PAGE_ID = "페이지ID"        # 전자책 저장할 노션 페이지 ID (32자리)
OBSIDIAN_PATH = "D:/경로/전자책"   # 옵시디언 폴더 경로
```

> **노션 페이지 ID 추출법**: 노션 URL 마지막 32자리  
> 예: `https://www.notion.so/My-Page-3505443bd8f880ff969af6d67642b56b`  
> → `3505443b-d8f8-80ff-969a-f6d67642b56b`

> **노션 토큰 발급**: notion.so/my-integrations → New integration → 토큰 복사  
> 이후 해당 페이지에서 우측 상단 ··· → Connections → 내 integration 추가 필요

### STEP 4: Claude Code 설정 등록

`C:/Users/{사용자명}/.claude/settings.json` 파일의 `mcpServers` 블록에 추가합니다.

```json
"notion-obsidian-ebook-mcp": {
  "command": "python",
  "args": ["C:/경로/notion-obsidian-ebook-mcp/server.py"]
}
```

> 경로는 실제 다운로드한 위치로 변경하세요.  
> 현재 경로 확인: PowerShell에서 `pwd` 입력

### STEP 5: 설치 확인

Claude Code를 재시작한 뒤 채팅창에서 입력:

```
"전자책 목록 보여줘"
```

목록이 반환되면 성공입니다.

---

## 사용 예시

```
"Claude Code 입문 가이드 전자책 만들어줘"
"MCP 개발 A to Z 전자책으로 정리해줘"
"현재 저장된 전자책 목록 보여줘"
"이 노션 페이지 내용 확인해줘: https://www.notion.so/..."
```

---

## 주의사항

- 노션 integration을 대상 페이지에 연결하지 않으면 페이지 생성이 실패합니다.
- `config.py`는 `.gitignore`에 포함되어 있습니다. 절대 GitHub에 올리지 마세요.
- Claude Code 재시작 후 MCP 서버가 연결됩니다.

---

## 라이선스

MIT License — Copyright © 2026 airaum
