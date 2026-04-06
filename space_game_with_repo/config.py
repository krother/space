import os
from pathlib import Path
from dotenv import load_dotenv

BASE_PATH = Path(__file__).parent

print("config")
load_dotenv(dotenv_path=BASE_PATH.parent / ".env", override=True, verbose=True)

LANG = os.getenv("LANG")
print(os.getenv("REPO_TYPE"))
