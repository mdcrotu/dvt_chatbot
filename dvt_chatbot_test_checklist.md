# ✅ DVT IDE Chatbot Test Checklist

This checklist helps verify that both the CLI and Web interfaces of your DVT IDE chatbot are functioning correctly before integrating fallback search logic.

---

## 🖥️ CLI Mode (`make cli`)

| Test # | Action                                      | Expected Result                                     |
|--------|---------------------------------------------|-----------------------------------------------------|
| 1      | Type: `How do I open the DVT Console?`       | Exact match, score 100                              |
| 2      | Type: `open console`                         | Fuzzy match to DVT Console, score ~80+              |
| 3      | Type: `new build config`                     | Fuzzy match to Build Configuration, score ~70+      |
| 4      | Type: `reverse simulate`                     | No match, fallback message + fuzzy suggestion       |
| 5      | Type: `exit`                                 | Exits CLI loop                                      |

---

## 🌐 Web UI Mode (`make run`, then visit `http://127.0.0.1:5000/`)

| Test # | Action                                      | Expected Result                                     |
|--------|---------------------------------------------|-----------------------------------------------------|
| 1      | Enter: `How can I create a new build configuration?` | Exact match from YAML                        |
| 2      | Enter: `build config`                       | Fuzzy match result + score shown                   |
| 3      | Enter: `compile waveform`                   | "Sorry, I don’t know yet." + fuzzy suggestion      |
| 4      | Enter: gibberish like `asdfghjk`            | "Sorry, I don’t know yet." with no suggestion      |
| 5      | Refresh form                                | Previously asked question is cleared               |

---

## 🔍 What to Watch For

- **Score thresholds** working as expected (e.g., fuzzy cutoff ~70)
- **Suggestions** only appear when confidence is reasonably high
- **No errors** in the terminal or browser console
- **Formatting clean** (no double-encoded HTML in answers)
