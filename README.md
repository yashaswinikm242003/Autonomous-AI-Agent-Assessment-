# Autonomous-AI-Agent-Assessment
This Python-based system allows you to run natural language instructions that the agent can execute through:
- Headless browser searches (via Selenium)
- Terminal command execution
- File creation and manipulation
- Automatic CSV report generation

## Features

- **Search Automation:** Google search queries via headless Chrome (Selenium)
- **Terminal Commands:** Executes shell commands securely and logs output
- **File Management:** Read, write, and move files as instructed
- **Report Generation:** Outputs results to `.csv` and logs execution
- **Simple NLP Parsing:** Uses spaCy to tokenize and handle instructions

## Components

| Class             | Responsibility                                  |
|------------------|--------------------------------------------------|
| `BrowserAutomation` | Automates Google search using headless Chrome |
| `TerminalExecutor` | Runs shell commands and captures output        |
| `FileManager`       | File I/O: create, read, and move files        |
| `NLPParser`         | Parses user instruction as a single task      |
| `ReportGenerator`   | Saves results into a CSV report               |
| `TaskExecutor`      | Orchestrates all actions based on instruction |


## Example Commands

```bash
search latest news in AI
run echo "Hello from AI"
save hello.txt
```


## Installation

```bash
pip install selenium pandas spacy reportlab openai
python -m spacy download en_core_web_sm
```
 Also make sure you have Chrome installed and chromedriver in your PATH.



## Usage

```bash
python Autonomous_Ai_System.py
```
You'll be prompted to enter commands like:
Enter your command (or type 'exit' to quit): search top 5 AI tools

The system will process it, execute the action, save logs/results, and generate a report.



 ## Output
- execution.log — Detailed logs of actions and errors
- report.csv — Structured task results
- Optional created files: search_results.txt, summary.txt, etc.




 ## Tech Stack
- Python 3.x
- Selenium (Web Automation)
- spaCy (NLP)
- Pandas (Reporting)
- ReportLab (Optional PDF Generation)



