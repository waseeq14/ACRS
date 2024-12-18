import os
import subprocess
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")


def color_text(text, color):
    """Helper function to add ANSI color codes to text."""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "cyan": "\033[96m",
        "reset": "\033[0m",
        "white": "\033[97m"
    }
    return f"{colors[color]}{text}{colors['reset']}"


def clean_code_segment(segment):
    """Remove unwanted markers (e.g., '```c' and '```') from a code segment."""
    return segment.replace("```c", "").replace("```", "").strip()


class AddressSanitizer:
    def __init__(self, llm, filePath):
        self.llm = llm
        self.filePath = filePath
        self.modified_code_path = None
        self.binary_path = "asan_binary"
        self.asan_output = None

    def preprocess_code_with_main(self):
        with open(self.filePath, "r") as file:
            source_code = file.read()

        prompt = PromptTemplate(
            template=(
                "You are tasked with analyzing the following C/C++ code. If it lacks a main() function, add one."
                "The main() function should test all major functionality of the code to ensure coverage for AddressSanitizer analysis."
                "Do not add unnecessary code or formatting. Output only the plain modified code."
                "\n\nOriginal Code:\n{source_code}\n\nModified Code with main():"
            ),
            input_variables=["source_code"],
        )

        llm_chain = LLMChain(llm=self.llm, prompt=prompt)
        modified_code = llm_chain.run({"source_code": source_code})
        modified_code = clean_code_segment(modified_code)

        self.modified_code_path = self.filePath.replace(".c", "_asan.c")
        with open(self.modified_code_path, "w") as file:
            file.write(modified_code)

        print(color_text(f"Modified code with main() written to {self.modified_code_path}", "green"))

    def compile_with_asan(self):
        compile_command = (
            f"clang -fsanitize=address -O1 -fno-omit-frame-pointer -g -o {self.binary_path} {self.filePath}"
        )

        try:
            subprocess.run(compile_command, shell=True, check=True)
            print(color_text(f"Successfully compiled {self.filePath} with AddressSanitizer.", "green"))
        except subprocess.CalledProcessError as e:
            print(color_text(f"Compilation failed: {e}", "red"))
            raise

    def run_asan(self):
        try:
            result = subprocess.run(f"./{self.binary_path}", shell=True, text=True, capture_output=True)
            print(color_text("Program executed. Capturing AddressSanitizer output.", "green"))
            if result.returncode != 0:
                print(color_text("Program encountered an error (expected with ASan).", "yellow"))
            self.asan_output = result.stdout + result.stderr
        except subprocess.CalledProcessError as e:
            print(color_text(f"Execution failed: {e}", "red"))
            raise

    def analyze_asan_output(self):
        with open(self.modified_code_path, "r") as file:
            source_code = file.read()

        prompt = PromptTemplate(
            template=(
                "You are analyzing AddressSanitizer output to detect vulnerabilities in the code provided."
                "Provide a concise summary of each vulnerability, including the type (e.g., buffer overflow, use-after-free),"
                "the exact location (file and line number), and a brief explanation of the issue.\n\n"
                "Code:\n{source_code}\n\nASan Output:\n{asan_output}\n\nAnalysis:"
            ),
            input_variables=["asan_output", "source_code"],
        )

        llm_chain = LLMChain(llm=self.llm, prompt=prompt)
        try:
            analysis = llm_chain.run({"asan_output": self.asan_output, "source_code": source_code})
            print(color_text("LLM Analysis:\n", "green"), color_text(analysis, "white"))
            with open("asan_analysis.txt", "w") as analysis_file:
                analysis_file.write(analysis)
            return analysis
        except Exception as e:
            print(color_text(f"Error during LLM analysis: {e}", "red"))
            raise

