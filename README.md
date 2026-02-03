# prototype
For fast prototyping!

### URL Samples

- https://news.hada.io/topic?id=26122 
  - Expected
    - ``[2026/01/26] Clawdbot - 모든 OS와 플랫폼에서 작동하는 개인용 AI 비서``


### Referneces

- https://ai.google.dev/gemini-api/docs/quickstart


```
cat URL.lst  | xargs -i sh -c "uv run trafilatura -u {} --with-metadata --json | jq '. | {title, date, source}'"
```

```
cat URL.lst \
| xargs -i sh -c "uv run trafilatura -u {} --with-metadata --json \
| jq '. | {source, title, date, text, categories, comments}'"
```
