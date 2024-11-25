import os
import subprocess
import json
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain.schema.runnable import RunnablePassthrough, RunnableSequence
import re


def fix_klee_includes(code):
    lines = code.splitlines()
    processed_lines = []

    for line in lines:
        if "#include #include" in line:
            print(line)
            line = line.replace("#include #include", "#include")
        processed_lines.append(line)

    return "\n".join(processed_lines)


def preprocess_code_with_llm(source_code_path, llm):
    with open(source_code_path, "r") as file:
        source_code = file.read()

    prompt = PromptTemplate(
        template=(
            "DONT GO AGAINST THE INSTRUCTIONS"
            "You are tasked with making the following C/C++ code compatible with KLEE for symbolic execution. "
            "The goal is to identify vulnerabilities such as buffer overflows, use-after-free, integer overflows or other memory-related issues. "
            "Replace any user input mechanisms (e.g., scanf, fgets) or external data sources with symbolic variables using KLEE's APIs. "
            "Remove all printf statements which include symbolic variables or any variable which is their result"
            "Directly printing pointers like buffer is invalid in klee_print_expr. Instead, access specific bytes (e.g., buffer[0])"
            "Ensure the code includes <klee/klee.h>, and use klee_make_symbolic() to replace user inputs or dynamic data sources. "
            "klee_print_expr() does not handle format strings like printf and requires the symbolic expression to be passed directly without formatting. For example:- Using printf: printf (\"Buffer content: %\s\n\", buffer);- The equivalent klee_print_expr: klee_print_expr(\"Buffer content:\", buffer);"
            "Avoid marking local variables as symbolic if they are directly influenced by symbolic inputs, as this is unnecessary. "
            "KLEE will automatically propagate symbolic properties through operations. "
            "The modified code should strictly adhere to KLEE-compatible practices. Proof-check the modified code "
            "for correctness and proper integration of KLEE-specific modifications. Do not include comments in the code.\n\n"
            "Original Code:\n{source_code}\n\n"
            "KLEE-Compatible Code:"
        ),
        input_variables=["source_code"]
    )


    llm_chain = LLMChain(llm=llm, prompt=prompt)
    klee_friendly_code = llm_chain.run({"source_code": source_code})
    klee_friendly_code = fix_klee_includes(klee_friendly_code)

    klee_friendly_path = source_code_path.replace(".c", "_klee.c")
    with open(klee_friendly_path, "w") as file:
        file.write(klee_friendly_code)
    print(f"KLEE-compatible code written to {klee_friendly_path}")
    return klee_friendly_path

def generate_llvm_ir(source_code, output_name="output"):
    bc_file = f"{output_name}.bc"

    clang_command = f"clang -emit-llvm -I /snap/klee/10/usr/local/include -g -fsanitize=signed-integer-overflow -fsanitize=undefined -fsanitize=signed-integer-overflow -c -o {bc_file} {source_code}"
    subprocess.run(clang_command, shell=True, check=True)

    print(f"LLVM bitcode generated: {bc_file}")
    return bc_file


def run_klee(bc_file, source_code, llm):
    klee_command = f"klee --libc=uclibc --posix-runtime {bc_file}"

    print(f"Running KLEE with command: {klee_command}")
    subprocess.run(klee_command, shell=True, check=True)
    print(f"KLEE execution completed for {bc_file}")

def parse_klee_output(klee_output_dir, llm):
    test_cases = []
    klee_messages = ""
    
    error_files = [file for file in os.listdir(klee_output_dir) if file.endswith(".err")]

    for err_file in error_files:
        test_case_base = err_file.split(".")[0]
        
        ktest_file = os.path.join(klee_output_dir, f"{test_case_base}.ktest")
        err_file_path = os.path.join(klee_output_dir, err_file)
        
        if os.path.exists(ktest_file):
            try:
                ktest_output = subprocess.check_output(
                    f"ktest-tool {ktest_file}", shell=True, text=True
                )
                
                with open(err_file_path, "r") as f:
                    err_content = f.read()

                test_cases.append({
                    "ktest_file": ktest_file,
                    "err_file": err_file_path,
                    "ktest_output": ktest_output,
                    "err_content": err_content
                })
            except subprocess.CalledProcessError as e:
                print(f"Error reading {ktest_file} or {err_file}: {e}")
    
    prompt = PromptTemplate(
        template=(
            "You are analyzing KLEE error reports to identify vulnerabilities. "
            "For each error, provide a concise summary of the vulnerability, the test case name, and the input that caused it (check the input from ktest output given to you). "
            "For example: Vulnerability: \nTest Case Name: \nInput that triggered it: \n"
            "Do not write unnecessary details."
            "\n\n"
            "Test Cases and Errors:\n{test_cases}"
        ),
        input_variables=["test_cases"]
    )
    
    formatted_test_cases = [
        f"Test Case: {case['ktest_file']}\nInput: {case['ktest_output']}\nError: {case['err_content']}"
        for case in test_cases
    ]


    llm_chain = LLMChain(llm=llm, prompt=prompt)
    
    try:
        summary = llm_chain.run({
            "test_cases": "\n\n".join(formatted_test_cases)
        })
        print("LLM Analysis:\n", summary)
    except Exception as e:
        print(f"Error during LLM analysis: {e}")


if __name__ == "__main__":
    load_dotenv()
    OpenAI.api_key = os.getenv("OPENAI_API_KEY")
    llm = OpenAI()

    source_code_file = "uaf.c"

    klee_friendly_code = preprocess_code_with_llm(source_code_file, llm)

    bc_file = generate_llvm_ir(klee_friendly_code)

    with open(klee_friendly_code, "r") as file:
        source_code = file.read()

    run_klee(bc_file, klee_friendly_code, llm)

    klee_output_dir = "./klee-last"
    parse_klee_output(klee_output_dir, llm)
