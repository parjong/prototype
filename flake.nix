{
  description = "GEM5 Prototyping Environment with SystemC and Python";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
      in
      {
        devShells.default = pkgs.mkShell.override { stdenv = pkgs.gcc14Stdenv; } {
          buildInputs = with pkgs; [
            scons
            cmake
            pkg-config
            swig
            bison
            flex
            m4

            systemc
            boost
            protobuf
            gperftools
            zlib
            hdf5
            capstone
            pngpp
            libpng

            python312
            python312Packages.setuptools
            python312Packages.wheel
            python312Packages.pybind11
            python312Packages.numpy
            python312Packages.scikit-build-core
            uv
          ];

          shellHook = ''
            export SYSTEMC_HOME=${pkgs.systemc}
            export PYTHON=${pkgs.python312}/bin/python3
            export PYTHON_CONFIG=${pkgs.python312}/bin/python3-config
            echo "GEM5 Prototyping Environment initialized."
          '';
        };
      }
    );
}
