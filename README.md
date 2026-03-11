# prototype
For fast prototyping!

Let's rock-n-roll with Gemini CLI!
- https://geminicli.com/docs/
  - https://geminicli.com/docs/tools/file-system/
  - https://geminicli.com/docs/cli/headless/
  - https://geminicli.com/docs/cli/custom-commands/
  - https://geminicli.com/docs/cli/skills/
  - https://geminicli.com/docs/extensions/writing-extensions/
  - https://geminicli.com/docs/issue-and-pr-automation/
  - https://geminicli.com/docs/core/policy-engine/
  - https://geminicli.com/docs/core/tools-api/

## Examples from Document

- [Rename your photographs based on content](https://geminicli.com/docs/get-started/examples/#rename-your-photographs-based-on-content)
  - Multimodal (image captioning + tool calling)
- Explain a repository by reading its code
- Combine two spreadsheets into one spreadsheet
  - Is it necessary to use LLM..?
  - Maybe for one-time job, it is a bit costly to write a script for one time job
- Run unit tests (js)
  - How about C++ and Python unittest?
  - Is there any benchmark?

## Use Case: Article Triage

```
wget -O 20260126.html https://news.hada.io/topic?id=26122
gemini --allowed-tools write_file -p "/summarize 20260126.html test.json"
```
