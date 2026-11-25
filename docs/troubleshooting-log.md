# Troubleshooting Log

> **과제 필수: 아래 4가지 시나리오를 팀 전체가 모두 수행하고 기록합니다.**
> **각 팀원은 최소 1개 시나리오의 기록 작성에 참여해야 하며, 이름이 문서에 드러나야 합니다.**

## 담당 배정

| 시나리오 | 담당 | 상태 |
| --- | --- | --- |
| a. `git commit --amend` | 하은 ([@haeunyn](https://github.com/haeunyn)) | ✅ |
| b. `git reset --soft HEAD~1` | 규영 ([@fromdance](https://github.com/fromdance)) | ⬜ |
| c. `git revert` | 지원 ([@geewon07](https://github.com/geewon07)) | ⬜ |
| d. `git stash` / `stash pop` | 지원 ([@geewon07](https://github.com/geewon07)) | ⬜ |

---

## 시나리오 a — `git commit --amend` (최근 커밋 메시지 수정)

> ✅ **2026-11-25 실제 수행함.** 아래는 템플릿이 아니라 실제로 돌린 기록입니다.

### 참여자
- 하은 ([@haeunyn](https://github.com/haeunyn)) — 수행 및 기록

### 상황
- PR #8(README 소개 링크 + CODEOWNERS) 작업 중, 커밋 메시지를 **`update`** 로 적어버렸다.
- 우리 팀 컨벤션(`docs/CONTRIBUTING.md`)은 `update` 를 **"의미없는 메시지"로 금지**한다.
  과제 명세 4-4번의 판정 기준에도 들어 있다.
- 아직 **push 하기 전**이었다.

### 시도한 명령/절차

```bash
git log --oneline -1
# d2d9b35 update                     ← 고칠 커밋

git commit --amend -F -              # 편집기 대신 표준입력으로 메시지 교체
# docs: link haeun intro in README and fill CODEOWNERS
# ...

git log --oneline -1
# c89427b docs: link haeun intro in README and fill CODEOWNERS
```

### 결과

| | 해시 | 메시지 |
| --- | --- | --- |
| amend 전 | `d2d9b35` | `update` |
| amend 후 | `c89427b` | `docs: link haeun intro in README and fill CODEOWNERS` |

**해시가 바뀌었다.** amend 는 기존 커밋을 고치는 게 아니라 **새 커밋으로 교체**하는 것이기 때문이다.
변경 내용(diff)은 똑같은데 해시만 달라졌다 — 커밋 해시는 메시지·작성시각까지 포함해 계산되기 때문이다.

옛 커밋은 사라진 게 아니라 **reflog 에 남아 있다.**

```bash
git reflog -3 --format='%h %gs'
# c89427b commit (amend): docs: link haeun intro in README and fill CODEOWNERS
# d2d9b35 commit: update
# a5bdef9 checkout: moving from main to feature/haeun-readme-link
```

### 왜 이 방법을 선택했는가 (Why)
- 아직 **push 하지 않았으므로** 히스토리를 바꿔도 남에게 영향이 없다.
- 메시지만 틀렸고 내용은 맞았다. `reset` 으로 커밋을 되돌렸다가 다시 묶을 이유가 없다.
- `revert` 는 **내용을 되돌릴 때** 쓴다. 여기는 내용이 아니라 메시지가 문제였다.

### ⚠️ 주의할 점
- **이미 push 한 커밋에 amend 를 쓰면 안 된다.** 해시가 달라져 강제 푸시가 필요해지고,
  다른 팀원의 로컬 히스토리와 어긋난다. (과제 제약: 팀 합의 없이 강제 푸시 금지)
- ★ **그렇다고 push 한 뒤에 `revert` 를 쓰면 안 된다.** `revert` 는 **변경 내용을 되돌리는**
  명령이라, 메시지만 고치려다 **멀쩡한 변경까지 취소**된다. 두 명령은 고치는 대상이 다르다.

  | 무엇이 잘못됐나 | push 전 | push 후 |
  | --- | --- | --- |
  | **커밋 메시지** | `commit --amend` | **그냥 둔다.** 다음 커밋이나 PR 본문에서 설명한다 |
  | **변경 내용** | `reset` / `amend` | `revert` (시나리오 c) |

  push 한 커밋의 메시지를 꼭 고쳐야 한다면 강제 푸시가 필요한데, 그건 팀 합의 사항이다.
  메시지 하나 때문에 남의 히스토리를 깨뜨릴 이유는 거의 없다.
- 잘못 amend 했을 때는 reflog 의 옛 해시로 돌아갈 수 있다 — `git reset --hard d2d9b35`.
  단 `--hard` 는 커밋 안 한 변경을 지우므로 주의한다.

### 재현하는 법
```bash
git switch -c tmp-amend-test
echo test > tmp.txt && git add tmp.txt && git commit -m "update"
git log --oneline -1          # 해시 적어두기
git commit --amend -m "docs: add tmp note"
git log --oneline -1          # 해시가 바뀐 것 확인
git switch - && git branch -D tmp-amend-test
```

## 시나리오 b — `git reset --soft HEAD~1` (로컬 커밋 취소 + 변경 유지)

### 참여자
-

### 상황
- 커밋을 너무 일찍 했다. 파일 하나를 빠뜨려서 커밋을 되돌리고 다시 묶고 싶다.

### 시도한 명령/절차

```bash
git log --oneline -2
git reset --soft HEAD~1       # 커밋만 취소, 변경 내용은 staged 상태로 남음
git status                    # 변경이 그대로 있는지 확인
git add <빠뜨린 파일>
git commit -m "feat: add truncate() with tests"
```

### 결과
- 커밋은 사라지고 **작업 내용은 그대로** 남는다.

### 왜 이 방법을 선택했는가 (Why)

| 옵션 | 커밋 | 스테이징 | 작업 파일 | 쓰는 때 |
| --- | --- | --- | --- | --- |
| `--soft` | 취소 | **유지** | 유지 | 커밋만 다시 묶고 싶을 때 |
| `--mixed` (기본) | 취소 | 취소 | 유지 | add 부터 다시 하고 싶을 때 |
| `--hard` | 취소 | 취소 | **삭제** | 전부 버리고 싶을 때 ⚠️ |

- `--soft` 를 쓴 이유: 작업한 내용을 잃지 않으면서 커밋 단위만 다시 잡고 싶었기 때문.

### ⚠️ 주의할 점
- `--hard` 는 **작업 파일까지 지운다.** 되돌릴 수 없다 (reflog 로 커밋은 찾을 수 있지만 미커밋 변경은 못 찾는다).
- reset 도 **push 한 뒤에는 쓰지 않는다.**

---

## 시나리오 c — `git revert` (원격에 push 된 커밋 취소)

### 참여자
-

### 상황
- 이미 `main` 에 병합되어 push 된 커밋에 문제가 있다. 되돌려야 한다.

### 시도한 명령/절차

```bash
git log --oneline -5                 # 되돌릴 커밋 해시 확인
git revert <커밋해시>                 # "그 커밋을 취소하는 새 커밋" 생성
git push
```

### 결과
- 기존 커밋은 **그대로 남고**, 그것을 되돌리는 **새 커밋이 추가**된다.
- 히스토리가 길어지지만 **아무도 깨지지 않는다**.

### 왜 reset 대신 revert 를 선택했는가 (Why) ★ 평가 단골 질문
- `reset` 은 히스토리에서 커밋을 **없앤다**. 이미 다른 사람이 그 커밋을 받아갔다면
  내 히스토리와 남의 히스토리가 어긋나고, 맞추려면 **강제 푸시**가 필요하다.
- `revert` 는 **아무것도 지우지 않고 되돌리는 커밋을 더한다.** 그래서 공유 브랜치에서 안전하다.
- 한 줄 요약: **혼자만 본 히스토리는 reset, 남이 이미 본 히스토리는 revert.**

### ⚠️ 주의할 점
- 머지 커밋을 revert 할 때는 `-m 1` 처럼 어느 쪽을 "원래 줄기"로 볼지 지정해야 한다.

---

## 시나리오 d — `git stash` / `git stash pop` (작업 보관 후 전환)

### 참여자
-

### 상황
- 작업하던 중에 급한 리뷰 요청이 왔다. 지금 변경은 커밋하기엔 덜 됐고, 버리기는 아깝다.

### 시도한 명령/절차

```bash
git stash                     # 현재 변경을 치워두고 깨끗한 상태로
git switch main
git switch -c feature/review-fix
# ... 급한 일 처리 ...
git switch feature/원래브랜치
git stash list                # 보관된 목록 확인
git stash pop                 # 가장 최근 것 꺼내고 목록에서 제거
```

### 결과
- 작업 중이던 변경이 그대로 돌아온다.

### 왜 이 방법을 선택했는가 (Why)
- 덜 된 작업을 커밋하면 `wip` 같은 **의미없는 커밋**이 생긴다 (팀 컨벤션 위반).
- stash 는 커밋 히스토리를 더럽히지 않고 잠시 치워둘 수 있다.

### ⚠️ 주의할 점
- `pop` 은 꺼내면서 **목록에서 지운다.** 남겨두려면 `git stash apply`.
- stash 는 **브랜치에 묶이지 않는다.** 다른 브랜치에서 pop 하면 거기에 적용되므로 주의.
- 충돌이 나면 pop 이 중단되고 stash 가 남아 있다. 충돌 해결 후 `git stash drop`.
