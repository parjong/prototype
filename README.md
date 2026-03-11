# prototype
For fast prototyping!

## Goal

Let's learn how to use GITHUB APP token!

## Candidate

https://github.com/buty4649/gh-app-token

`secret/app.envrc`
```
export GH_APP_TOKEN_APP_ID="..."
export GH_APP_TOKEN_PRIVATE_KEY="path/to/pem"
```

```
GH_TOKEN=$(gh app-token --repo parjong/prototype) gh issue comment 31 --body "Hello?"
```

## Candiadte

- https://github.com/Link-/gh-token

## References

- https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-json-web-token-jwt-for-a-github-app

