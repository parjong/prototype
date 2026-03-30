# Github Discussion 접근하기

`gh` CLI를 사용하여 GitHub Discussion에 접근하고 관리하는 방법을 설명합니다. 다음 `gh api` 명령을 통해 Discussion에 접근할 수 있습니다.

*   **Discussion 목록 보기**: `gh api repos/[OWNER]/[REPO]/discussions`
*   **특정 Discussion 자세히 보기**: `gh api repos/[OWNER]/[REPO]/discussions/[DISCUSSION_NUMBER]` 또는 GraphQL API 사용

Discussion 생성은 `gh api graphql`을 통해 GraphQL API를 직접 호출해야 할 수 있습니다. 예를 들어, 다음 GraphQL 쿼리와 `gh api graphql` 명령어를 조합하여 Discussion을 생성할 수 있습니다. (`repositoryId`, `categoryId` 등은 실제 값으로 대체해야 합니다.)

```graphql
mutation CreateDiscussion($repositoryId: ID!, $categoryId: ID!, $title: String!, $body: String!) {
  createDiscussion(
    input: {
      repositoryId: $repositoryId
      categoryId: $categoryId
      title: $title
      body: $body
    }
  ) {
    discussion {
      url
    }
  }
}
```

```bash
REPOSITORY_ID=$(gh api repos/OWNER/REPO --jq ".node_id")
CATEGORY_ID=$(gh api repos/OWNER/REPO/discussion/categories --jq ".viewerCanCreateCategory[0].id") # 또는 특정 카테고리 ID

gh api graphql -f query=\'mutation CreateDiscussion($repositoryId: ID!, $categoryId: ID!, $title: String!, $body: String!) { createDiscussion(input: { repositoryId: $repositoryId, categoryId: $categoryId, title: $title, body: $body }) { discussion { url } } }\' \
-f repositoryId=\"$REPOSITORY_ID\" \
-f categoryId=\"$CATEGORY_ID\" \
-f title=\'새로운 Discussion 제목\' \
-f body=\'새로운 Discussion 내용입니다.\' \
--body-file 옵션을 사용하여 멀티라인 주석을 파일에서 로드할 수 있습니다. 예를 들어, `discussion_body.md` 파일에 주석 내용을 작성한 후 `-f body=\"$(cat discussion_body.md)\"` 또는 `--body-file discussion_body.md`와 같이 사용할 수 있습니다.
```

Discussion을 효율적으로 관리하고, 복잡한 작업이나 직접적인 명령어 지원이 없는 경우에는 `gh api`와 GraphQL을 조합하여 유연하게 대응할 수 있습니다.
