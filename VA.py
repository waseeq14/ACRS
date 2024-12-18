from io import StringIO
import os
import subprocess
from pyfiglet import Figlet
import warnings
from dotenv import load_dotenv
from contextlib import redirect_stderr
import time
import shutil
stderr_buffer = StringIO()
with redirect_stderr(stderr_buffer):
    from langchain.prompts import PromptTemplate
    from langchain_openai import OpenAI
    from langchain.chains import LLMChain
    from langchain.chat_models import ChatOpenAI
    from asan import AddressSanitizer
    from semgrep_ai import SarifResultAnalyzer
    from klee import KleeProcessor
    from klee2 import KleeProcessor2
    from classifyVuln import ClassifyVuln

    
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)


class VA:
    def __init__(self, filePath, llm):
        self.filePath = filePath
        self.llm = llm

    def setFilePath(self, newFilePath):
        self.filePath = newFilePath

    def ASAN(self):
        try:
            print("[+] PREPARING FOR ADDRESS SANITIZATION....")
            asan = AddressSanitizer(self.llm, self.filePath)
            asan.preprocess_code_with_main()
            asan.compile_with_asan()
            asan.run_asan()
            results = asan.analyze_asan_output()
            print("[+] ADDRESS SANITIZATION COMPLETED!")
            return results
        except Exception as e:
            print("[-] Error Occured (ASAN): ", e)

    def RULES(self):
        try:
            print("[+] PREPARING TO APPLY SOME STRICT RULES :3...")
            rules = SarifResultAnalyzer(self.filePath, self.llm)
            rules.run_semgrep()
            results =  rules.extract_and_analyze_results()
            print("[+] RULES APPLIED!")
            return results
        except Exception as e:
            print("[-] Error Occured (RULES): ", e)

    def SYMBOLIC(self):
        try:
            print("[+] PREPARING TO KLEEN YOUR CODE. . . ")
            process = KleeProcessor(self.filePath, self.llm)
            process.preprocess_code_with_llm()
            process.generate_llvm_ir()
            process.run_klee()
            results = process.parse_klee_output()
            print("[+] CODE HAS BEEN KLEENED!")
            return results
        except Exception as e:
            print("[-] Error Occured (KLEE): ", e)

    def SYMBOLIC2(self):
        try:
            print("[+] PREPARING TO KLEEN YOUR CODE. . . ")
            process = KleeProcessor2(self.filePath, self.llm)
            process.extract_vulnerable_segments()
            process.generate_llvm_ir_for_segments()
            process.run_klee_on_segments()
            print("[+] CODE HAS BEEN KLEENED!")
        except Exception as e:
            print("[-] Error occured (KLEE): ", e)

    def getCWE(self):
            process = ClassifyVuln(llm, self.filePath)
            print(process.getVulns())
            cwes = process.getCWE()
            i = 1
            for cwe in cwes:
                print(f"{i}) ID#:{cwe[0]} - {cwe[1]} - Similarity Score: {cwe[2]}\n")
                i+=1
            return cwes

def display_logo_and_clear(file_path):
    try:
        with open(file_path, 'r') as file:
            logo = file.read()

        columns, rows = shutil.get_terminal_size()

        logo_lines = logo.splitlines()

        padding_top = (rows - len(logo_lines)) // 2

        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" * padding_top) 

        for line in logo_lines:
            padding_left = (columns - len(line)) // 2
            print(" " * padding_left + line)
            time.sleep(0.09)  

        time.sleep(2)

        os.system('cls' if os.name == 'nt' else 'clear')

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def menu():
    print("\nSelect an option:")
    print("1. ASAN Analysis")
    print("2. Rules Analysis")
    print("3. Symbolic Execution")
    print("4. Symbolic Segments Analysis")
    print("5. Change source file")
    print("6. Fetch CWEs (after VA)")
    print("7. Exit")

    option = input("Enter your choice: ")
    return option

if __name__ == "__main__":
    load_dotenv()
    OpenAI.api_key = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    f = Figlet(font='slant')
    display_logo_and_clear("logo.txt")
    print(f.renderText('ACRS'))
    filePath = input("Enter path of source file: ")

    process = VA(filePath, llm)

    while(True):
        option = menu()
        if option == "1":
            asanAnalysis = process.ASAN()
        elif option == "2":
            rulesAnalysis = process.RULES()
        elif option == "3":
            kleeAnalysis = process.SYMBOLIC()
        elif option == "4":
            process.SYMBOLIC2()
        elif option == "5":
            filePath = input("Enter new path of source file: ")
            process.setFilePath(filePath)
        elif option == "6":
            print("\nFetching CWEs..hold your horses..\n")
            process.getCWE()
        elif option == "7":
            print("Yahin tak tha jo tha..bye")
            break
        else:
            print("Invalid choice, please try again.")
