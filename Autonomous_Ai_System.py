import os
import subprocess
import json
import shutil
import pandas as pd
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import openai
import spacy
import reportlab
import time

# Configure Logging
logging.basicConfig(filename="execution.log", level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load NLP model
nlp = spacy.load("en_core_web_sm")

class BrowserAutomation:
    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=options)

    def search_google(self, query):
        """Perform a Google search and return results."""
        try:
            self.driver.get(f"https://www.google.com/search?q={query}")
            time.sleep(2)
            results = self.driver.find_element(By.TAG_NAME, "body").text
            return results
        except Exception as e:
            logging.error(f"Browser Error: {str(e)}")
            return f"Error: {str(e)}"

    def close(self):
        self.driver.quit()

class TerminalExecutor:
    def run_command(self, command):
        """Execute a terminal command and return output."""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            logging.error(f"Terminal Error: {str(e)}")
            return f"Error: {str(e)}"

class FileManager:
    def create_file(self, filename, content):
        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(content)
        except Exception as e:
            logging.error(f"File Error: {str(e)}")
            return f"Error: {str(e)}"

    def read_file(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            logging.error(f"File Read Error: {str(e)}")
            return f"Error: {str(e)}"

    def move_file(self, src, dest):
        try:
            shutil.move(src, dest)
        except Exception as e:
            logging.error(f"File Move Error: {str(e)}")
            return f"Error: {str(e)}"

class NLPParser:
    def parse_instruction(self, instruction):
        """Treat the full instruction as a single task."""
        return [instruction]

class ReportGenerator:
    def generate_report(self, data, filename="report.pdf"):
        """Generate a report from structured data."""
        try:
            df = pd.DataFrame(data)
            df.to_csv("report.csv", index=False)
            return f"Report saved as {filename}"
        except Exception as e:
            logging.error(f"Report Error: {str(e)}")
            return f"Error: {str(e)}"

class TaskExecutor:
    def __init__(self):
        self.browser = BrowserAutomation()
        self.terminal = TerminalExecutor()
        self.file_manager = FileManager()
        self.nlp_parser = NLPParser()
        self.report_generator = ReportGenerator()

    def execute_task(self, task):
        """Executes a single task with error handling and logs execution."""
        try:
            task_lower = task.lower()
            if task_lower.startswith("search"):
                query = task.partition("search")[2].strip()
                if not query:
                    return {"task": task, "result": "Error: Please provide a search query after 'search'"}
                result = self.browser.search_google(query)
                self.file_manager.create_file("search_results.txt", result)
                return {"task": task, "result": result[:200]}
            elif task_lower.startswith("run"):
                command = task.partition("run")[2].strip()
                if not command:
                    command = "dir" if os.name == "nt" else "ls -l"
                result = self.terminal.run_command(command)
                return {"task": task, "result": result}
            elif task_lower.startswith("save"):
                filename = task.partition("save")[2].strip() or "summary.txt"
                content = "This file was created by the AI system based on your 'save' command."
                self.file_manager.create_file(filename, content)
                return {"task": task, "result": f"File '{filename}' saved successfully"}

            else:
                return {"task": task, "result": "Task not recognized"}
        except Exception as e:
            logging.error(f"Task Execution Error ({task}): {str(e)}")
            return {"task": task, "error": str(e)}

    def execute_tasks(self, instruction):
        """Process instructions and execute tasks sequentially with logging."""
        tasks = self.nlp_parser.parse_instruction(instruction)
        results = []

        for task in tasks:
            result = self.execute_task(task)
            results.append(result)

        report_status = self.report_generator.generate_report(results)
        logging.info("Execution Completed! " + report_status)
        print("Execution Completed!", report_status)
        self.browser.close()

# Interactive CLI
if __name__ == "__main__":
    executor = TaskExecutor()
    while True:
        user_input = input("Enter your command (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            print("Exiting program.")
            break
        executor.execute_tasks(user_input)