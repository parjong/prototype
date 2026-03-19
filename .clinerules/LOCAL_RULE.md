When operating on a file at any given path, the following `RULE.md` files, if they exist, must be consulted and adhered to, in order of precedence from most specific to most general:

1. `RULE.md` located in the file's immediate directory.
2. `RULE.md` files located in each of the file's ancestor directories, moving upwards towards the root.

These rules provide contextual guidelines for tasks performed within their respective directory scopes.
