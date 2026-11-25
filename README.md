# Codyssey Git 협업 연습 (B2-2)

> Codyssey AI 올인원 2기 · 본과정 AI·SW 기초 · **Python과 Git 심화** 미션
> 3~5인이 실제 협업 상황을 시뮬레이션하며 GitHub Flow · PR 리뷰 · 충돌 해결을 체득합니다.

**복잡한 기능 구현이 목적이 아닙니다.** 결과물 퀄리티보다 **협업 과정**(브랜치·PR·리뷰·이슈·충돌 해결·기록)이 중요합니다.

## 우리 팀이 GitHub Flow를 선택한 이유 (3줄)

1. 브랜치가 `main` 과 `feature/*` 둘뿐이라 **규칙이 단순해 팀원이 헷갈릴 일이 적다.**
2. 모든 변경이 **PR 한 곳**을 지나므로 리뷰와 이력이 자연스럽게 쌓인다.
3. `main` 을 항상 "깨지지 않는 상태"로 두면 누구든 언제든 거기서 새 작업을 시작할 수 있다.

## 팀원 (= 결과물 목록)

과제의 "간단한 결과물"은 **(B) 팀 소개**를 택했습니다.
각자 `team/<이름>.md` 에 자기소개 파일을 하나 추가하고, **이 표에 자기 줄을 직접 추가**합니다.
코딩 없이 글만 쓰면 되므로 **Git 협업 과정(브랜치·PR·리뷰·충돌)** 에 집중할 수 있습니다.

| 이름 | GitHub | 소개 | 담당 |
| --- | --- | --- | --- |
| 하은 | [@haeunyn](https://github.com/haeunyn) | [소개](team/haeun.md) | 저장소 세팅 · 문서 뼈대 · 트러블슈팅 amend |
| 지원 | [@geewon07](https://github.com/geewon07) | [소개](team/geewon.md) | 개발 환경 · 협업 규칙 · 트러블슈팅 revert/stash |

> 쓰는 법과 양식: [`team/README.md`](team/README.md)
>
> ⚠️ **팀원 전원이 이 표의 같은 자리를 고칩니다.** 충돌이 나는 게 정상이고,
> 과제 7번이 요구하는 **비자명 충돌**(같은 파일의 같은 hunk 를 서로 다르게 수정)이 여기서 생깁니다.
> 해결한 사람이 [`docs/conflict-resolution.md`](docs/conflict-resolution.md) 에 기록합니다.

## 문서

| 문서 | 내용 |
| --- | --- |
| [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) | 브랜치·커밋·PR·리뷰 규칙, 충돌 대응 흐름 |
| [docs/conflict-resolution.md](docs/conflict-resolution.md) | 충돌 해결 기록 |
| [docs/troubleshooting-log.md](docs/troubleshooting-log.md) | Git 트러블슈팅 기록 (amend/reset/revert/stash) |
| [SUBMISSION.md](SUBMISSION.md) | 제출물 인덱스 (팀원별 PR 링크) |

## 시작하기

```bash
git clone https://github.com/haeunyn/codyssey-git-collab.git
cd codyssey-git-collab

git switch -c feature/<본인이름>-<주제>     # 예: feature/haeun-intro
# ... 작업 ...
git add -A && git commit -m "docs: add haeun intro to team"
git push -u origin feature/<본인이름>-<주제>
# GitHub 에서 PR 생성 (본문에 Closes #이슈번호 포함)
```

⚠️ `main` 에는 직접 push 할 수 없습니다. **반드시 PR 을 통해 병합**하며 **1명 이상의 승인**이 필요합니다.
