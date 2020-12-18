
.PHONY: ninja

ifeq ($(OS),Windows_NT)
HOST=windows
else
HOST=linux
endif


default: ninja


build/$(HOST)/build.ninja:
	meson --default-library=static build/$(HOST)

ninja: build/$(HOST)/build.ninja
	cd build/$(HOST) && ninja

clean:
	cd build/$(HOST) && ninja clean

cleanall:
	rm -rf build/$(HOST)

run-qt: ninja
	cd build/$(HOST) && frontend/qt/kratos-qt
	
run-cli: ninja
	cd build/$(HOST) && frontend/cli/kratos-cli

