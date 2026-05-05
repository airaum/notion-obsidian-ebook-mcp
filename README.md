# notion-obsidian-ebook-mcp

Claude Code에서 말 한마디로 **노션 페이지 + 옵시디언 .md 파일**을 동시에 생성하는 MCP 서버.

`전자책 만들어줘` → 표지·목차·표·Callout이 갖춰진 전자책이 노션과 옵시디언에 동시 저장됨.

---

## 제공하는 도구

| 도구 | 설명 |
|------|------|
| `create_ebook` | 노션 + 옵시디언에 전자책 동시 생성 |
| `list_ebooks` | 전자책 목록 조회 |
| `read_ebook_content` | 기존 전자책 내용 추출 |

---

## 설치 방법

### 1. 사전 조건 확인

```
python --version   # 3.10 이상
```

### 2. 파일 준비

```
notion-obsidian-ebook-mcp/
├── server.py
├── notion_builder.py
├── obsidian_writer.py
├── requirements.txt
├── config.example.py  ← 이걸 복사해서 config.py로 저장
└── .gitignore
```

### 3. 라이브러리 설치

```
pip install -r requirements.txt
```

### 4. config.py 설정

`config.example.py`를 복사해 `config.py`로 저장한 뒤 아래 3가지를 채운다:

```python
NOTION_TOKEN = "ntn_..."          # notion.so/my-integrations 에서 발급
PARENT_PAGE_ID = "페이지ID"        # 전자책 저장할 노션 페이지 ID (32자리)
OBSIDIAN_PATH = "D:/경로/전자책"   # 옵시디언 폴더 경로
```

> **노션 페이지 ID 추출법**: 노션 URL 마지막 32자리  
> 예: `https://www.notion.so/My-Page-3505443bd8f880ff969af6d67642b56b`  
> → `3505443b-d8f8-80ff-969a-f6d67642b56b`

### 5. Claude Code settings.json 등록

`C:/Users/{사용자명}/.claude/settings.json`의 `mcpServers` 블록에 추가:

```json
"notion-obsidian-ebook-mcp": {
  "command": "python",
  "args": ["D:/경로/notion-obsidian-ebook-mcp/server.py"]
}
```

### 6. 설치 확인

Claude Code 재시작 후:

```
전자책 목록 보여줘
```

`list_ebooks`가 실행되면 성공.

---

## 사용 예시

```
전자책 만들어줘 — Claude Code 프롬프트 최적화 가이드
```

```
기존 전자책들 목록 보여줘
```

---

## 전자책 표준 템플릿

생성되는 전자책은 아래 구조로 고정됩니다:

1. 목차(TOC)
2. 인트로 Callout (💡 파란색)
3. GitHub 링크 (있을 때)
4. 이게 뭔가?
5. 왜 필요한가? (표)
6. 핵심 기능 (표)
7. 설치 방법 (단계별)
8. 실전 활용 예시
9. 잘 맞는 경우 / 덜 맞는 경우 (표)
10. 주의사항 Callout (⚠️ 노란색)
11. 핵심 3줄 요약 Callout (💡 초록색)
12. 저작권

---

## 라이선스

MIT
