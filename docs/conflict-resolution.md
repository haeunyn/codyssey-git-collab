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
- 작성자:
- 상대:

### 상황 (What happened)

### 충돌 유형
- [ ] 자명
- [ ] 비자명 A
- [ ] 비자명 B

### 충돌 내용 (Conflict markers)

```txt

```

### 해결 과정 (How)

### 결과 (Outcome)

### 배운 점 (Learnings)
