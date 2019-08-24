import pip
from pip._internal import main as i_main

try:
    if hasattr(pip, 'main'):
        pip.main(["install", "--upgrade", "pip"])
        pip.main(["install", "-r", "requirements.txt"])
    else:
        i_main(["install", "--upgrade", "pip"])
        i_main(["install", "-r", "requirements.txt"])
except SystemExit as e:
    print(e)
    pass