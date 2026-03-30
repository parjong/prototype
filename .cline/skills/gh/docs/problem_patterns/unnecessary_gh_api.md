# 불필요한 `gh api` 사용

`gh` CLI의 기본 기능을 `gh api`로 대체하여 사용하는 것은 불필요한 복잡성을 초래하며 효율성을 저해합니다. 

`gh api`는 `gh` CLI가 직접 지원하지 않는 특정 GitHub API 호출 시 사용되지만, `gh pr list`와 같이 전용 명령어가 있는 경우 `gh api`를 사용하는 것은 더 많은 인자와 복잡한 JSON 파싱을 요구합니다.
이는 스크립트의 복잡도를 높이고 유지보수를 어렵게 만듭니다. 

`gh` CLI의 풍부한 기능을 최대한 활용하고 전용 명령어를 사용하는 것이 코드의 간결성과 가독성을 향상시킵니다.

## 나쁜 예시

```bash
gh api repos/{owner}/{repo}/pulls --jq ".[\]].number"
```

## 좋은 예시 (권장)

```bash
gh pr list --json number --jq ".[\]].number"
```
