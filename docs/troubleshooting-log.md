# Troubleshooting Log

> **과제 필수: 아래 4가지 시나리오를 팀 전체가 모두 수행하고 기록합니다.**
> **각 팀원은 최소 1개 시나리오의 기록 작성에 참여해야 하며, 이름이 문서에 드러나야 합니다.**

## 담당 배정

| 시나리오 | 담당 | 상태 |
| --- | --- | --- |
| a. `git commit --amend` | 하은 ([@haeunyn](https://github.com/haeunyn)) | ✅ |
| b. `git reset --soft HEAD~1` | 규영 ([@fromdance](https://github.com/fromdance)) | ⬜ |
| c. `git revert` | 지원 ([@geewon07](https://github.com/geewon07)) | ✅ |
| d. `git stash` / `stash pop` | 지원 ([@geewon07](https://github.com/geewon07)) | ✅ |

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

> ✅ **2026-11-25 실제 수행함.**

### 참여자

- 지원 ([@geewon07](https://github.com/geewon07)) — 수행 및 기록

### 상황

- 이미 원격 저장소에 push 한 커밋의 변경 내용을 취소해야 하는 상황을 재현하였다.
- main 브랜치에 영향을 주지 않기 위해 `feature/geewon-troubleshooting` 브랜치에서 실습하였다.
- 관련 Issue: #16

### 시도한 명령/절차

```bash
# 실습용 파일 생성 및 커밋
echo "This change should be reverted." > revert-test.txt
git add revert-test.txt
git commit -m "test: add temporary file for revert experiment"

# 원격 저장소에 push
git push -u origin feature/geewon-troubleshooting

# 취소 대상 커밋 확인
git log --oneline -1

# 기존 커밋 취소
git revert --no-edit 3e36f6b

# 취소 결과 확인
git log --oneline -3
git status
git show --stat HEAD
ls revert-test.txt

# 취소 커밋 push
git push

# 최종 확인
git status
git log --oneline -3
```

### 결과

| 구분 | 커밋 해시 | 결과 |
| --- | --- | --- |
| 기존 커밋 | `3e36f6b` | 실습용 파일 생성 |
| revert 커밋 | `0cf7f88` | 실습용 파일 삭제 |

실제 git log 결과:

```text
0cf7f88 Revert "test: add temporary file for revert experiment"
3e36f6b test: add temporary file for revert experiment
```

파일 삭제 확인:

```text
ls: revert-test.txt: No such file or directory
```

최종 상태:

```text
Your branch is up to date with 'origin/feature/geewon-troubleshooting'.
nothing to commit, working tree clean
```

- 기존 커밋이 삭제되지 않고 이력에 남아 있다.
- 기존 변경을 취소하는 새로운 커밋이 생성되었다.
- 강제 push 없이 원격 저장소에 반영하였다.

### 왜 reset 대신 revert를 선택했는가 (Why)

- reset은 브랜치가 가리키는 커밋을 이동시키므로 이미 공유된 이력을 변경할 수 있다.
- 이미 push한 커밋을 reset으로 제거하면 원격 저장소에 반영하기 위해 강제 push가 필요할 수 있다.
- 우리 팀은 팀 합의 없는 강제 push를 금지한다.
- revert는 기존 커밋을 유지하면서 변경 내용을 반대로 적용하는 새로운 커밋을 생성한다.
- 이미 원격 저장소에 push한 커밋이므로 협업 이력을 보호하기 위해 revert를 선택하였다.
- 한 줄 요약: **공유하지 않은 커밋은 reset, 이미 공유한 커밋의 변경 취소는 revert.**

### ⚠️ 주의할 점

- 취소하려는 커밋의 해시를 정확하게 확인해야 한다.
- 이후 변경사항과 겹치면 revert 과정에서도 충돌이 발생할 수 있다.
- merge commit을 revert할 때는 `-m` 옵션으로 기준 부모를 지정해야 한다.
- main 브랜치의 변경 취소 역시 팀 규칙에 따라 PR을 통해 진행해야 한다.
- 실제 실습에서는 공용 PC를 사용하므로 개인 GitHub 인증 정보가 credential helper에 저장되지 않도록 `git -c credential.helper= push`를 사용하였다. 일반적인 환경에서는 `git push`를 사용하면 된다.

---

## 시나리오 d — `git stash` / `git stash pop` (작업 보관 후 전환)

> ✅ **2026-11-25 실제 수행함.**

### 참여자

- 지원 ([@geewon07](https://github.com/geewon07)) — 수행 및 기록

### 상황

- 트러블슈팅 문서를 작성하던 중 다른 브랜치로 급하게 이동해야 하는 상황을 재현하였다.
- 아직 완료되지 않은 작업을 커밋하지 않고 임시 저장한 뒤 복원하고자 하였다.
- 작업 브랜치: `feature/geewon-troubleshooting`
- 관련 Issue: #16

### 시도한 명령/절차

```bash
# 커밋하지 않은 변경사항 생성
printf '\n<!-- stash experiment: work in progress -->\n' >> docs/troubleshooting-log.md

# 변경사항 확인
git status --short
git --no-pager diff docs/troubleshooting-log.md

# 작업 임시 저장
git stash push -m "geewon: troubleshooting work in progress"

# 임시 저장 상태 확인
git stash list
git status

# main 브랜치로 이동
git switch main
git status

# 기존 작업 브랜치로 복귀
git switch feature/geewon-troubleshooting
git stash list

# 임시 저장한 작업 복원
git stash pop 'stash@{0}'

# 복원 결과 확인
git status --short
git --no-pager diff docs/troubleshooting-log.md
git stash list
```

### 결과

#### 1. stash 실행 후

```text
stash@{0}: On feature/geewon-troubleshooting: geewon: troubleshooting work in progress
nothing to commit, working tree clean
```

- 변경사항이 stash에 임시 저장되었다.
- 작업 디렉터리가 깨끗해졌다.

#### 2. 브랜치 전환

- main 브랜치로 정상적으로 이동하였다.
- 기존 작업 브랜치로 정상적으로 복귀하였다.
- stash 목록에 보관한 작업이 유지되어 있었다.

#### 3. stash pop 실행 후

```text
Dropped stash@{0}
```

```text
 M docs/troubleshooting-log.md
```

복원된 변경 내용:

```html
<!-- stash experiment: work in progress -->
```

- 커밋하지 않았던 변경사항이 정상적으로 복원되었다.
- 복원에 성공한 stash 항목은 목록에서 제거되었다.
- 실습용 주석은 최종 기록 문서를 작성하면서 제거하였다.

### 왜 이 방법을 선택했는가 (Why)

- 완료되지 않은 작업을 임시로 커밋할 필요가 없다.
- 변경사항을 잃지 않고 다른 브랜치로 이동할 수 있다.
- 불필요한 커밋을 생성하지 않고 기존 작업을 이어갈 수 있다.

### ⚠️ 주의할 점

- 기본 stash는 추적되지 않는 파일을 포함하지 않는다. 필요한 경우 `git stash -u`를 사용한다.
- stash는 특정 브랜치에만 묶여 있지 않으므로 복원할 브랜치를 확인해야 한다.
- `git stash pop`은 복원에 성공하면 해당 stash 항목을 제거한다.
- 보관 내용을 유지하면서 복원하려면 `git stash apply`를 사용한다.
- 복원 과정에서 충돌이 발생하면 내용을 확인하고 해결한 후 stash를 제거해야 한다.
