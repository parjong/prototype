# PoC: Nix로 Rust + GCC 개발 환경

`nix develop` 한 번으로 gcc, rustc, cargo, rustfmt, clippy, rust-analyzer 환경을 구성합니다.

## 사용법

```bash
cd poc/nix-rust-gcc
nix develop
```

## 검증 결과

Determinate Nix 3.24.2 (nix 2.35.3), WSL2 / x86_64-linux 에서 확인:

- gcc 16.2.0
- rustc 1.99.1 / cargo 1.99.0
- `cargo new hello && cargo run` → `Hello, world!`

모든 패키지가 cache.nixos.org 바이너리 캐시에서 받아져 로컬 빌드는 발생하지 않았습니다.

## 참고

- nixpkgs의 rustc를 사용합니다. nightly / 특정 버전 / 크로스 타깃이 필요하면 `rust-overlay` 또는 `fenix`를 고려하세요.
- 지원 시스템은 `x86_64-linux`만 정의했습니다. 필요 시 `flake-utils` 등으로 확장하세요.
- direnv + `use flake` 로 디렉터리 진입 시 자동 활성화할 수 있습니다.
