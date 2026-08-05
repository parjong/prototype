# prototype
For fast prototyping!

### 참고

nix를 이용해서 모든 패키지 관리

### 디렉토리 구조

```
flake.nix
pyproject.toml
3rdparyty/
  pyproject.toml // Customized GEM5를 python 패키지로 빌드
  gem5 // submodule https://github.com/gem5/gem5/tree/v25.1
  src/
    (custom SystemC model, 0x10번지에 1byte unsigned integer를 write하면 0x20번지에 +1된 값을 저장)
pyproject.toml // 3rdparry 폴더를 dependency로 가지도록
smaple.cpp // 0x10번지에 1을 write하고 0x20번지를 출력하는 코드
sample.out // sample.cpp를 static linking한 코드 (gitignore)
sample.py // 수행하면 sample.out을 수행
```