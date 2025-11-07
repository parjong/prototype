# prototype
For fast prototyping!

```sh
function hey_goose()
{
  local PROMPT="$*"
  echo "PROMPT: '$PROMPT'"
  goose run --no-session -t "$PROMPT"
}
```
