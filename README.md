# dvt_chatbot

## 🔁 Current Chatbot Workflow (CLI + Web)
🔹 Shared Core Logic
* custom_answers.yaml = primary answer source
* find_answer_with_score() (in answer_engine.py) does:
    1. Exact match check
    2. Fuzzy match (token_set_ratio)
    3. Returns (answer, matched_question, score) or suggestion

### 🖥️ Web UI (Flask app.py)
```{bash}
make run        # Launches Flask web app
```
Access at http://127.0.0.1:5000/

Features:
* Ask question in form
* Displays answer + matched question and score (if fuzzy)
* If no match: shows “Sorry…” message and best suggestion

### 🖱️CLI Interface
```{bash}
make cli        # Launches CLI version
```
OR
```{bash}
venv/bin/python appy.py cli
```
Features:
* Interactive loop
* Typing a question:
    * Prints answer + matched question + score
* Typing exit or quit: ends session


## ✅ Testing Tips
1. Check known question
    ```{bash}
    > How do I open the DVT Console?
    ```
    Should return exact match

2. Try fuzzy variant
    ```{bash}
    > open console
    ```
    Should show best match with score ~80+

3. Try unknown question
    ```{bash}
    > how do I reverse simulate?
    ```
    Should say: “Sorry, I don’t know yet.” \
    And maybe offer a fuzzy suggestion (e.g., build config?)


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
make scrape     # Scrapes the DVT User Guide (scrape_dvt_guide.py)
                # Creates the dvt_guide.data.json file
make embed      # Reads the dvt_guide.data.json and adds embeddings (embed_dvt_guide.py)
                # Creates the dvt_guide_data_with_embeddings.json file
make search     # Standalone script to test searching the DVT User Guide results (search_cli.py)
make test       # Runs test_validate_embeddings.py
                # Loads dvt_guide_data_with_embeddings.json
                # Checks for valid embedding fields
                # Prints:
                    # Total entries
                    # First 5 embeddings and their length
                    # Cosine similarity between the first two sections
make clean      # Cleans virtual env and cache
```
