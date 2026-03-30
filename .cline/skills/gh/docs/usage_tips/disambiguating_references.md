# `#<NUM>` 참조 타입 파악 및 접근 가이드

Github에서 `#<NUM>` 형식의 참조는 Issue, Pull Request, Discussion 중 하나일 수 있으며, 이들의 정확한 타입을 파악하고 접근하기 위해 GitHub GraphQL API를 활용하는 것이 효과적입니다.

GraphQL 쿼리를 통해 주어진 번호(`number`)가 `Issue`, `PullRequest`, `Discussion` 중 어떤 타입인지 확인할 수 있습니다. (`[OWNER]`, `[REPO]`, `[NUMBER]`는 실제 값으로 대체)

```graphql
query LookupReference($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    issueOrPullRequest(number: $number) {
      __typename
    }
    discussion(number: $number) {
      __typename
    }
  }
}
```

`gh api graphql` 명령어를 사용하여 이 쿼리를 실행하면 `__typename` 필드로 타입을 알 수 있습니다. 예를 들어, `gh api graphql -f query='...' -f owner='my-org' -f repo='my-repo' -f number=123`와 같이 사용합니다. 타입이 파악되면 `gh issue view <NUMBER>`, `gh pr view <NUMBER>`, `gh discussion view <NUMBER>` 등 해당 타입에 맞는 `gh` CLI 명령어로 접근할 수 있습니다. `#<NUM>` 참조의 정확한 타입을 모를 때는 GraphQL API로 먼저 파악하여 모호함을 줄이고 정보에 빠르게 도달하는 것이 좋습니다.
