
.PHONY: ninja

ifeq ($(OS),Windows_NT)
HOST=windows
else
HOST=linux
endif


default: ninja


build/linux/build.ninja:
	meson --default-library=static build/$(HOST)

# Meson's qt5 module has a bug with debug build when building with mingw.
# Therefore a release build
build/windows/build.ninja:
	meson --default-library=static --buildtype=release build/$(HOST)

ninja: build/$(HOST)/build.ninja
	cd build/$(HOST) && ninja

clean:
	cd build/$(HOST) && ninja clean

cleanall:
	rm -rf build/$(HOST)

run-qt: ninja
	build/$(HOST)/frontend/qt/kratos-qt
	
run-cli: ninja
	build/$(HOST)/frontend/cli/kratos-cli

