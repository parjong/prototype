all:
	make -f Makefile.T1.plain

rest:
	make -f Makefile.T1.plain.old_CMake
	make -f Makefile.T1.uvx
	make -f Makefile.T1.uvx.old_CMake
