.PHONY: build

setup: create-env init

create-env:
	python3 -m venv env

install:
	./env/bin/python3 -m pip install $(package)

lock:
	./env/bin/pip3 freeze > requirements.txt

list:
	./env/bin/pip3 list

init:
	./env/bin/pip3 install -r requirements.txt

test:
	./execute_test.sh 

build:
	./env/bin/python3 setup.py bdist_wheel

publish:
	twine upload dist/* --verbose

remove-old-builds:
	rm -rf ./.eggs ./build ./dist ./yahoo_fin_api.egg-info

check-typing:
	./env/bin/mypy yahoo_fin_api
