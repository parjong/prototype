# prototype
For fast prototyping!

## How to enable LSP for C/C++?

```
git clone https://github.com/neovim/nvim-lspconfig ~/.config/nvim/pack/nvim/start/nvim-lspconfig
```

Run ``:lua vim.lsp.enable('clangd')``

Add the following line to ``~/.config/nvim/init.lua``
```lua
vim.lsp.enable('clangd')
```


## Extra Reqruiements

- https://neovim.io/doc/user/plugins.html
- https://cdecl.github.io/devops/nvim-plug/
  - Use vim
- https://github.com/LazyVim/LazyVim
  - Too heavy for me

Configuration file?
- Either ``~/.config/nvim/init.vim`` or ``~/.config/nvim/init.lua``

From https://github.com/folke/lazy.nvim
> lazy.nvim is a modern plugin manager for Neovim.i

From https://github.com/mason-org/mason.nvimq
> mason.nvim is a Neovim plugin that allows you to easily manage external editor tooling such as LSP servers, DAP servers, linters, and formatters through a single interface. It runs everywhere Neovim runs (across Linux, macOS, Windows, etc.), with only a small set of external requirements needed.


