# Conflict Resolution Log

> 충돌을 해결한 사람이 직접 기록합니다.
> **과제 필수: 팀 전체 최소 2회 이상, 그중 최소 1회는 "비자명 충돌"**

## 비자명 충돌이란?

아래 둘 중 **하나 이상**을 충족해야 합니다.

| 유형 | 설명 |
| --- | --- |
| **A** | 같은 파일의 **같은 hunk(인접 라인)** 를 서로 다르게 수정 |
| **B** | 한쪽은 **파일 이동/이름 변경/삭제**, 다른 한쪽은 **내용 수정** |

> 서로 다른 파일을 고친 건 애초에 충돌이 나지 않습니다.
> 같은 파일의 **멀리 떨어진 줄**을 고친 것도 Git 이 알아서 합치므로 "자명한" 경우입니다.

### 비자명 충돌 만드는 법 (유형 A 예시)

```bash
# 두 사람이 각자 브랜치에서 src/utils/text.py 의 "같은 함수"를 고친다
# A: truncate() 의 기본 길이를 20 → 30 으로
# B: 같은 줄에서 suffix 를 "..." → "…" 로
# 먼저 병합된 쪽이 main 에 들어가면, 나중 PR 에서 충돌이 난다
```

### 비자명 충돌 만드는 법 (유형 B 예시)

```bash
# A: src/utils/text.py → src/utils/string_utils.py 로 파일명 변경
# B: 같은 시간에 src/utils/text.py 의 내용을 수정
# → Git 이 "한쪽은 지웠고 한쪽은 고쳤다"며 판단을 사람에게 넘긴다
```

---

## 충돌 기록 #1

### 참여자

- 작성자: 지원 ([@geewon07](https://github.com/geewon07))
- 상대: 하은 ([@haeunyn](https://github.com/haeunyn))
- 발생일: 2026-11-25

### 상황 (What happened)

- 작업 브랜치: `feature/geewon-dev-env`
- 병합 대상: `origin/main`
- 파일: `docs/CONTRIBUTING.md`
- 연결 Issue: #3

지원은 개발 환경 추가 및 브랜치 네이밍 규칙,
커밋 메시지 컨벤션 보완 작업을 진행하였다.

하은의 PR #2가 먼저 main에 병합되면서
CONTRIBUTING.md의 동일한 부분이 변경되었다.

지원의 PR #11을 병합하려는 과정에서
다음 두 구간에 충돌이 발생하였다.

1. 브랜치 네이밍 예시 표
2. 커밋 메시지의 좋은 예시

### 충돌 유형

- [ ] 자명
- [x] **비자명 A** — 같은 hunk를 서로 다르게 수정
- [ ] 비자명 B — 한쪽 이동/삭제 + 한쪽 수정

### 충돌 내용 (Conflict markers)

#### 충돌 구간 1: 브랜치 네이밍 예시

```txt
<<<<<<< HEAD
| `feature/haeun-intro` | 팀원 자기소개 추가 |
| `feature/geewon-dev-env` | 개발 환경 문서 작성 |
| `feature/geewon-revert` | revert 트러블슈팅 실습 |
=======
| `feature/haeun-intro` | 하은이 자기소개 파일 추가 |
| `feature/haeun-update-intro` | 하은이 자기소개 내용 수정 |
| `docs/haeun-contributing` | 문서 작업 (feature 대신 docs 접두사 허용) |
>>>>>>> origin/main
```

#### 충돌 구간 2: 커밋 메시지 예시

```txt
<<<<<<< HEAD
docs: add geewon team introduction
docs: add development environment to CONTRIBUTING
docs: improve branch naming rules
docs: record git stash experiment
docs: add team role based on review feedback
fix: resolve README merge conflict
chore: add pull request template
=======
docs: add haeun intro to team
docs: fix broken link in team list
docs: add branch naming rules to CONTRIBUTING
>>>>>>> origin/main
```

#### 충돌 마커의 의미

- `<<<<<<< HEAD`: 현재 작업 중인 지원의 feature 브랜치 내용
- `=======`: 두 브랜치 내용의 구분선
- `>>>>>>> origin/main`: 병합하려는 최신 main 브랜치 내용

### 해결 과정 (How)

- 선택한 전략: `choose one`
- 두 충돌 구간에서 HEAD 쪽 내용을 유지하였다.

디스코드에서 하은과 충돌 상황을 공유하고
어느 쪽의 내용을 유지할지 협의하였다.

팀에서 합의한 최신 브랜치 네이밍 규칙은
모든 작업 브랜치를 feature/로 통일하는 것이므로
지원이 작성한 내용을 유지하기로 결정하였다.

다른 파일의 자동 병합 결과는 그대로 보존하고,
CONTRIBUTING.md의 충돌 구간 두 곳만 직접 수정하였다.

#### 실제 수행한 명령어

```bash
# 현재 브랜치와 작업 상태 확인
git status

# 최신 원격 저장소 정보 가져오기
git fetch origin

# 현재 feature 브랜치에 최신 main 병합
git merge origin/main

# 충돌 발생 상태 확인
git status

# 실제 충돌 구간 확인
git --no-pager diff --cc docs/CONTRIBUTING.md

# 충돌 파일을 열어 직접 수정
open -e docs/CONTRIBUTING.md

# 충돌 마커가 남아 있는지 확인
grep -nE '^(<<<<<<<|=======|>>>>>>>)' docs/CONTRIBUTING.md

# 공백 오류 검사
git diff --check

# 기존 작업 브랜치 내용과 비교
git --no-pager diff HEAD -- docs/CONTRIBUTING.md
```

#### 해결 방법

1. HEAD 쪽 내용을 유지하였다.
2. origin/main 쪽의 충돌 구간 내용을 제거하였다.
3. 충돌 마커 3종을 모두 제거하였다.
4. 수정한 파일을 저장하였다.
5. 충돌 마커와 공백 오류가 없는 것을 확인하였다.

### 결과 (Outcome)

- 관련 PR:
  - [PR #2 — 팀 소개 방식으로 변경](https://github.com/haeunyn/codyssey-git-collab/pull/2)
  - [PR #11 — 개발 환경 및 협업 규칙 보완](https://github.com/haeunyn/codyssey-git-collab/pull/11)
- 관련 커밋:
  - `18337d7`: 개발 환경 및 협업 규칙 작성
  - `77eb6c5`: Windows 환경 관련 리뷰 반영
  - `a5bdef9`: 병합 대상 origin/main의 커밋

동일 파일에서 발생한 두 충돌 구간을 해결하였다.

충돌 마커 검사 및 공백 오류 검사에서
별도의 오류가 출력되지 않았다.

팀에서 합의한 feature/ 브랜치 네이밍 규칙과
커밋 메시지 컨벤션을 유지하였다.

현재 충돌 파일 수정 및 검증을 완료했으며,
merge commit 생성과 PR 최종 병합을 진행할 예정이다.

### 배운 점 (Learnings)

- 서로 다른 브랜치에서 작업하더라도 동일한 파일의
  같은 부분을 수정하면 충돌이 발생할 수 있다.
- 충돌이 발생하면 한쪽 내용을 무조건 삭제하기보다
  팀원과 협의하여 최종 내용을 결정해야 한다.
- HEAD는 항상 main을 의미하는 것이 아니라
  현재 체크아웃한 브랜치를 의미한다.
- 공통 문서를 수정할 때는 작업 범위를 미리 공유하고
  다른 PR의 병합 상황을 확인해야 한다.
- 공유된 브랜치의 이력을 보호하기 위해
  강제 push나 rebase 대신 merge를 활용하였다.
- 충돌 발생부터 해결까지 명령어와 결과를 기록하면
  이후 동일한 문제를 재현하고 해결하기 쉽다.

---

## 충돌 기록 #2

### 참여자

- 작성자: 하은 ([@haeunyn](https://github.com/haeunyn)) — 해결 및 기록
- 상대: 하은 본인의 선행 PR #8 (같은 줄을 먼저 바꿔 main 에 들어가 있었다)
- 발생일: 2026-11-25

### 상황 (What happened)

- 작업 브랜치: `feature/haeun-team-table` (PR #14, 연결 Issue #13)
- 병합 대상: `origin/main` (`394ccc8`)
- 파일: `README.md` **22번 줄** — 팀원 표의 하은 줄

두 PR 이 **같은 한 줄의 서로 다른 칸**을 고쳤다.

| PR | 고친 칸 | 내용 |
| --- | --- | --- |
| #8 (먼저 병합됨) | **소개** | `_(작성 예정)_` → `[소개](team/haeun.md)` |
| #14 (나중) | **담당** | `저장소 세팅 · 문서 뼈대` → `... · 트러블슈팅 amend` |

Git 은 **줄 단위로 비교**한다. 사람 눈에는 "서로 다른 칸이니 겹치지 않는다"지만,
Git 에게는 **같은 줄이 양쪽에서 다르게 바뀐 것**이라 어느 쪽을 살릴지 판단할 수 없다.
그래서 사람에게 넘겼다. 과제 7번의 **비자명 충돌 유형 A**(같은 파일의 같은 hunk)에 해당한다.

### 충돌 내용 (Conflict markers)

```txt
<<<<<<< HEAD
| 하은 | [@haeunyn](https://github.com/haeunyn) | _(작성 예정)_ | 저장소 세팅 · 문서 뼈대 · 트러블슈팅 amend |
=======
| 하은 | [@haeunyn](https://github.com/haeunyn) | [소개](team/haeun.md) | 저장소 세팅 · 문서 뼈대 |
>>>>>>> origin/main
```

- `<<<<<<< HEAD` ~ `=======` : **지금 내 브랜치**(`feature/haeun-team-table`)의 내용
- `=======` ~ `>>>>>>> origin/main` : **가져오려는 쪽**(main)의 내용

### 해결 과정 (How)

**전략: keep both (둘 다 살리기).**
서로 다른 칸을 고친 것이라 **어느 하나를 버릴 이유가 없다.**
main 의 소개 링크와 내 브랜치의 담당 갱신을 **한 줄에 합쳤다.**

```bash
git switch feature/haeun-team-table
git fetch origin
git merge origin/main          # ← 여기서 충돌

# README.md 22번 줄: 마커 3줄(<<<<<<<, =======, >>>>>>>)을 모두 지우고
# 소개 링크 + 담당 갱신을 합친 한 줄로 수정

git add README.md
git commit                     # 병합 커밋 메시지는 기본값 사용
git push
```

### 결과 (Outcome)

```
| 하은 | [@haeunyn](https://github.com/haeunyn) | [소개](team/haeun.md) | 저장소 세팅 · 문서 뼈대 · 트러블슈팅 amend |
```

- 마커 잔존 **0건** (`grep -c "<<<<<<<"` 로 확인)
- 두 변경이 모두 살아 있다.

### 주의점 / 다음에 피하는 법

- **rebase 를 쓰지 않았다.** 이미 push 한 브랜치라 rebase 는 강제 푸시가 필요하고,
  그건 팀 규칙(`CONTRIBUTING.md` 운영 안정성)과 과제 제약에 어긋난다.
- **마커 3줄을 전부 지워야 한다.** 하나라도 남으면 그대로 커밋되어 문서가 깨진다.
- **재발 방지** — 같은 줄을 건드리는 PR 을 동시에 열지 않는다.
  불가피하면 **먼저 병합되는 쪽을 정해두고**, 나중 쪽이 바로 `git merge origin/main` 으로 따라잡는다.
- 표처럼 **한 줄에 여러 정보가 들어가는 구조**는 충돌이 잦다.
  팀원별로 **줄을 나눠** 쓰면 충돌 범위가 줄어든다.


---

## 충돌 기록 #3

### 참여자

- 작성자: 규영 ([@fromdance](https://github.com/fromdance)) — 해결 및 기록
- 상대: 하은 ([@haeunyn](https://github.com/haeunyn)) PR #8, 지원 ([@geewon07](https://github.com/geewon07)) PR #15 (둘 다 먼저 main 에 병합됨)
- 발생일: 2026-11-26

### 상황 (What happened)

- 작업 브랜치: `feature/kyuyeong-intro` (연결 Issue #10)
- 병합 대상: `origin/main` (`8c0e2ca`)
- 파일: `README.md` 팀원 표 — 하은 줄 바로 아래

내 브랜치는 #8 · #15 가 병합되기 **전의 main** 에서 갈라져 나왔다. 그 사이 main 에서는 같은 자리가 두 번 바뀌었다.

| 쪽 | 바뀐 내용 |
| --- | --- |
| main (#8) | 하은 줄의 소개 칸 `_(작성 예정)_` → `[소개](team/haeun.md)`, 담당에 `트러블슈팅 amend` 추가 |
| main (#15) | 하은 줄 바로 아래에 **지원 줄 추가** |
| 내 브랜치 | 하은 줄 바로 아래에 **규영 줄 추가** |

하은 줄은 양쪽에서 내용이 다르고, 그 바로 아래 같은 위치에 서로 다른 줄이 추가되었다.
인접 라인이라 Git 이 하나의 hunk 로 묶었고, 어느 쪽을 살릴지 판단할 수 없어 사람에게 넘겼다.

### 충돌 유형

- [ ] 자명
- [x] **비자명 A** — 같은 파일의 같은 hunk 를 서로 다르게 수정
- [ ] 비자명 B

### 충돌 내용 (Conflict markers)

```txt
<<<<<<< HEAD
| 하은 | [@haeunyn](https://github.com/haeunyn) | _(작성 예정)_ | 저장소 세팅 · 문서 뼈대 |
| 규영 | [@fromdance](https://github.com/fromdance) | [소개](team/kyuyeong.md) | 리뷰 규칙 보완 · 트러블슈팅(`git reset`) |
=======
| 하은 | [@haeunyn](https://github.com/haeunyn) | [소개](team/haeun.md) | 저장소 세팅 · 문서 뼈대 · 트러블슈팅 amend |
| 지원 | [@geewon07](https://github.com/geewon07) | [소개](team/geewon.md) | 개발 환경 · 협업 규칙 · 트러블슈팅 revert/stash |
>>>>>>> origin/main
```

- `HEAD` 쪽: 내 브랜치 — **예전 하은 줄** + 내가 추가한 규영 줄
- `origin/main` 쪽: **최신 하은 줄** + 지원 줄

### 해결 과정 (How)

**전략: 줄마다 다르게 판단했다.**

| 줄 | 전략 | 이유 |
| --- | --- | --- |
| 하은 | **choose one** (main 쪽) | 내 브랜치의 하은 줄은 내가 고친 게 아니라 갈라질 당시의 옛 내용이다. main 쪽이 최신 |
| 지원 · 규영 | **keep both** | 서로 다른 사람의 줄을 각각 추가한 것이라 버릴 이유가 없다. 병합된 순서대로 지원 → 규영 |

```bash
git switch feature/kyuyeong-intro
git fetch origin
git merge origin/main          # ← 여기서 README.md 충돌

# 마커 3줄을 모두 지우고 하은(main) → 지원 → 규영 순으로 정리
# 규영 줄 담당 칸은 다른 줄 표기에 맞춰 "트러블슈팅 reset --soft" 로 통일

git add README.md
git commit                     # 제목은 기본값, 본문에 충돌 원인·전략 기록
git push
```

> merge 중 `git status` 에 CODEOWNERS · troubleshooting-log 등 main 의 변경이 staged 로 보였다.
> 이는 main 에서 가져온 내용이 merge 커밋에 함께 담기는 것이라 **정상**이다.
> 내리면(`git restore --staged`) 팀원 작업을 지우는 셈이 되므로 그대로 커밋했다.

### 결과 (Outcome)

```
| 하은 | [@haeunyn](https://github.com/haeunyn) | [소개](team/haeun.md) | 저장소 세팅 · 문서 뼈대 · 트러블슈팅 amend |
| 지원 | [@geewon07](https://github.com/geewon07) | [소개](team/geewon.md) | 개발 환경 · 협업 규칙 · 트러블슈팅 revert/stash |
| 규영 | [@fromdance](https://github.com/fromdance) | [소개](team/kyuyeong.md) | 리뷰 규칙 보완 · 트러블슈팅 reset --soft |
```

- merge 커밋: `060d696`
- 마커 잔존 **0건**
- `git diff --stat origin/main...HEAD` 로 PR 에는 내 변경(README 1줄 · SUBMISSION · team/kyuyeong.md)만 남은 것을 확인

### 주의점 · 재발 방지

- 충돌 블록 안에는 **내가 고치지 않은 옛 내용**(하은 줄)도 섞여 나온다. 무조건 keep both 하면 옛 내용이 되살아나므로 줄마다 어느 쪽이 최신인지 확인해야 한다.
- 이미 push 한 브랜치라 rebase 대신 merge 로 따라잡았다 (강제 푸시 금지).
- 새 브랜치를 main 에서 다시 따면 충돌 없이 끝나지만, 이번에는 실습 기록을 위해 **기존 브랜치에서 merge** 했다.

## 기록 템플릿 — 새 기록을 쓸 때 복사해서 쓰세요

> 번호는 **다음 번호**로 바꿉니다. (지금까지 #1 ~ #3 작성됨 → 다음은 **#4**)

````markdown
## 충돌 기록 #N

### 참여자
- 작성자:
- 상대:
- 발생일:

### 상황 (What happened)
- 작업 브랜치 / 병합 대상 / 파일·줄 / 연결 Issue

### 충돌 유형
- [ ] 자명
- [ ] 비자명 A — 같은 파일의 같은 hunk 를 서로 다르게 수정
- [ ] 비자명 B — 한쪽은 이동·이름변경·삭제, 다른 쪽은 내용 수정

### 충돌 내용 (Conflict markers)
```txt
<<<<<<< HEAD
=======
>>>>>>> origin/main
```

### 해결 과정 (How)
- 선택한 전략(keep both / choose one / refactor)과 이유
- 실제로 실행한 명령

### 결과 (Outcome)

### 주의점 · 재발 방지
````
