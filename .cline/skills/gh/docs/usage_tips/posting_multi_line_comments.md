# 멀티라인 주석 (Multi-line Comment) 추가하기

Github CLI를 사용하여 Issue 또는 Pull Request에 멀티라인 주석을 추가할 때 `--body-file` 옵션을 활용할 수 있습니다. 이 옵션은 파일에 작성된 내용을 주석 본문으로 사용합니다.

예시:

1.  `comment_body.md` 파일에 주석 내용을 작성합니다.

    ```
    이것은 첫 번째 줄입니다.
    이것은 두 번째 줄입니다.

    세 번째 줄은 비어 있습니다.
    ```

2.  `gh issue comment` 또는 `gh pr comment` 명령어와 함께 `--body-file` 옵션을 사용하여 주석을 추가합니다.

    ```bash
    gh issue comment <issue-number> --body-file comment_body.md
    gh pr comment <pr-number> --body-file comment_body.md
    ```

또한, `gh api graphql` 명령어를 사용하여 GraphQL API로 Issue 또는 Pull Request에 주석을 추가하는 경우에도 `--input file` 또는 `-F body=@filename` 옵션을 활용할 수 있습니다.

```bash
# --input file 옵션 사용 예시 (body 변수에 파일 내용을 할당하는 GraphQL 쿼리라고 가정)
gh api graphql --input comment_body.json -f query=\'mutation($body: String!){ addComment(input:{subjectId:"<issue-or-pr-id>",body:$body}) { commentEdge { node { body } } } }\'

# -F body=@filename 옵션 사용 예시
gh api graphql -F query=\'mutation($body: String!){ addComment(input:{subjectId:"<issue-or-pr-id>",body:$body}) { commentEdge { node { body } } } }\' -F body=@comment_body.md
```
