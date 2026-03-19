Your task is to improve a pull request specified in "Target Pull Request"
section below via interactive interaction with a user via Github

### Steps

1. Read all the comments from the target pull request with Github CLI (gh)
   - Including conversational, review, and inlined review comments
   - SHOULD exclude "outdated" or "resolved" comments
2. Do one one the following action for each comments that explicitly mentions "cline".
   - Update the code if the user requests code modification (usually via inlined review comments)
     - If changes are made, commit them to git and push.
   - Post a comment if the user simply ask something according to the comment type
     - Conversational, or review comments
       - Post a conversational comment
     - Inlined review comments
       - Post a reply

### Interaction

Repeat all the the above steps if the user say something similar "reviewed" or "please take another look".

### Target Pull Request

- #32
