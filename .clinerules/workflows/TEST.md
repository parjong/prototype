Your task is to improve a pull request specified in "Target Pull Request"
section below via interactive interaction with a user via Github

### Steps

1. Read all the comments from the target pull request with Github CLI (gh)
   - Including conversational, review, and inlined review comments
   - SHOULD exclude "outdated" or "resolved" comments
   - **IMPORTANT: ONLY consider comments that explicitly mention "Cline".**
2. Do one one the following action for each comments that mentions "Cline".
   - Update the code if the user requests code modification (usually via inlined review comments)
     - If changes are made, commit them to git and push.
   - Post a comment if the user simply ask something according to the comment type
     - Conversational, or review comments
       - Post a conversational comment
     - Inlined review comments
       - Post a reply

### Interaction

Repeat all the the above steps if the user say something similar "reviewed" or "please take another look".

### Lessons Learned

During this task, I encountered and resolved several issues, leading to the following key lessons:

1.  **`gh pr view --json` fields**: For detailed comment fetching, using `gh pr view --json comments,reviews` is a good starting point, but `gh api` is necessary to access individual inline review comments.
2.  **`gh api` for inline review comment replies**: Directly replying to inline comments via `gh api` is complex due to specific parameter requirements (`pull_request_review_id`, `commit_id`, `path`, `position`, `in_reply_to_comment_id`). A simpler approach for some cases is to post a new conversational comment referencing the original inline comment.
3.  **Token optimization**: When using `gh api` or `gh pr view --json`, explicitly specifying only the necessary fields (e.g., `body`, `path`, `line`, `original_line`, `id`, `html_url`) can significantly reduce token usage.
4.  **Distinguishing instruction types**: It's important to differentiate between instructions that require direct code modification in the project files and those that require an update to the agent's internal process or understanding.

### Target Pull Request

- #32
