#!./env/bin/python3

import subprocess
from pathlib import Path
import shutil
import os
import json
import pwd

EXEC_FILE_NAME = "shouldibuy"
HOME = Path.home()
EXEC_PATH = f"{HOME}/.local/bin/{EXEC_FILE_NAME}"

def setup():
	os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

	Path(f"{HOME}/.{EXEC_FILE_NAME}").mkdir(parents=True, exist_ok=True)

	Path(f"{HOME}/.local/bin").mkdir(parents=True, exist_ok=True)

	with open(f"{HOME}/.{EXEC_FILE_NAME}/portfolio.json", "w") as file:
		file.write(json.dumps({
			"portfolios": []
		}))

	subprocess.call([
		"./env/bin/pyinstaller",
		"./src/__init__.py",
		"--onefile",
		f"--name={EXEC_FILE_NAME}"
	])

	shutil.copyfile(f"./dist/{EXEC_FILE_NAME}", EXEC_PATH)

	os.chmod(EXEC_PATH, 0o777)

if __name__ == "__main__":
	setup()