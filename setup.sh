#!/bin/bash

./env/bin/pyinstaller --onefile ./src/buy.py && cp ./dist/buy /usr/local/bin/shouldibuy