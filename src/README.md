# src — 팀원별 유틸 함수 모음

과제의 "간단한 결과물" 중 **(A) 유틸 함수 모음**을 선택했습니다.
**복잡한 기능이 목적이 아닙니다.** 각자 함수 1개면 충분합니다.

## 내 함수 추가하는 법

1. **Issue 생성** — `feat: add <주제> utils`
2. **브랜치 생성**
   ```bash
   git switch main && git pull
   git switch -c feature/<본인이름>-<주제>
   ```
3. **파일 작성** — `src/utils/<주제>.py`
   - 함수 1개 이상
   - **docstring 에 사용 예시**를 꼭 넣기 (아래 `text.py` 참고)
4. **커밋** — `feat: add <함수명>() to <주제> utils`
5. **push & PR** — 본문에 `Closes #이슈번호`
6. **README 표에 본인 함수 추가** (같은 PR 에 포함해도 됩니다)

## 실행해보기

```bash
cd src
python -c "from utils.text import truncate; print(truncate('안녕하세요 반갑습니다', 8))"
```

## 현재 목록

| 모듈 | 함수 | 작성자 |
| --- | --- | --- |
| `utils/text.py` | `truncate()` | 하은 |
