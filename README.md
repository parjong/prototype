# prototype
For fast prototyping!

### How?

1. Install ollama on Windows
2. Open ollama app and enable "Expose Ollama to the network"
   - As of now, I failed to find a way to restrict access scope (such as subnet)
3. Set ``OLLAMA_HOST`` as ``host.docker.internal`` from WSL
   - https://m.blog.naver.com/techshare/223497992045
4. Run any ollama command :)

