# dvt_chatbot

## Quick Usage

▶️ Option 1: Use the Shell Script
```{bash}
bash setup.sh
```
    It will:
    Create the virtual environment
    Install dependencies
    Prompt you to launch in web or CLI mode
    If web, use your browser to connect to the displayed address:port

▶️ Option 2: Use the Makefile
```{bash}
make install    # Sets up venv and installs packages
make run        # Launches Flask web app
make cli        # Launches CLI version
make clean      # Cleans virtual env and cache
```
