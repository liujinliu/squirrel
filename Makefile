all:
	@echo "do nothing"

clean:
	rm -f `find . -type f -name '*.py[co]' `
	rm -fr */*.egg-info build dist

build_egg: clean
	python setup.py build_py -O2 bdist_egg --exclude-source-files

install_egg: build_egg
	easy_install dist/*.egg

build: clean
	python setup.py build_py bdist_wheel
	cp Makefile dist

install: build
	pip install dist/*.whl -U

local_install: build
	virtualenv --no-site-packages dist/tmp
	. dist/tmp/bin/activate && pip install dist/*.whl -U	

install_whl: install

deploy:
	pip install *.whl -U

uninstall:
	pip uninstall -y squirrel 

.PHONY : all clean build_egg install_egg local_install build install install_whl uninstall
