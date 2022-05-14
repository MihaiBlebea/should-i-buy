#!/bin/bash

./env/bin/pyinstaller --onefile --name=shouldibuy ./src/__init__.py && cp ./dist/shouldibuy /usr/local/bin/shouldibuy