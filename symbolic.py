import os
import subprocess
import requests
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

# ============ CWE REST API Configuration ============
CWE_API_ROOT = "https://cwe-api.mitre.org/api/v1/cwe"

def fetch_cwe_by_vulnerability(vulnerability_name):
    """
    Use the CWE REST API to map a vulnerability name to a corresponding CWE.
    """
    search_url = f"{CWE_API_ROOT}/weakness"  # Base endpoint for weaknesses
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        all_cwes = response.json()

        # Search for CWE matching the vulnerability name
        for cwe in all_cwes.get('weaknesses', []):
            if vulnerability_name.lower() in cwe.get('name', '').lower():
                return cwe['id'], cwe['name'], cwe['description']
        return None, None, "No matching CWE found."
    except requests.exceptions.RequestException as e:
        print(f"Error fetching CWE: {e}")
        return None, None, f"Error fetching CWE: {e}"

def fetch_cwe_details(cwe_id):
    """
    Fetch detailed information for a specific CWE ID using the CWE REST API.
    """
    cwe_details_url = f"{CWE_API_ROOT}/weakness/{cwe_id}"
    try:
        response = requests.get(cwe_details_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching CWE details: {e}")
        return None

# ============ Step 2: Generate LLVM IR ============
def generate_llvm_ir(source_code, output_name="output"):
    """
    Generate LLVM IR (.bc and .ll files) from source code using Clang.
    """
    bc_file = f"{output_name}.bc"
    ll_file = f"{output_name}.ll"

    # Generate LLVM bytecode
    clang_command = f"clang -emit-llvm -c -o {bc_file} {source_code}"
    subprocess.run(clang_command, shell=True, check=True)

    # Convert LLVM bytecode to human-readable LLVM IR
    disassemble_command = f"llvm-dis {bc_file} -o {ll_file}"
    subprocess.run(disassemble_command, shell=True, check=True)

    print(f"LLVM IR generated: {ll_file}")
    return ll_file

# ============ Step 3: Generate CFG and Prioritize Paths ============
def generate_cfg_and_prioritize(ll_file, llm, vulnerability_type=None):
    """
    Generate the control flow graph and prioritize paths using LLM.
    Dynamically fetch CWE details if no CWE is provided.
    """
    # Generate CFG using LLVM opt tool
    opt_command = f"opt --dot-cfg {ll_file}"
    subprocess.run(opt_command, shell=True, check=True)

    # Read CFG file (assumes DOT format)
    cfg_files = [file for file in os.listdir() if file.endswith(".dot")]

    print(f"Generated CFG files: {cfg_files}")

    prioritized_paths = []

    # Fetch CWE details if a vulnerability type is not provided
    cwe_id, cwe_name, cwe_description = None, None, None
    # if not vulnerability_type:
    #     # Query the LLM for a vulnerability type
    #     vulnerability_prompt = PromptTemplate(
    #         input_variables=["cfg"],
    #         template="Given the control flow graph:\n{cfg}\n"
    #                  "Identify any potential vulnerabilities and their type."
    #     )
    #     llm_chain = LLMChain(llm=llm, prompt=vulnerability_prompt)
    #     llm_response = llm_chain.run(cfg=";".join(cfg_files))
    #     print(f"LLM identified vulnerability: {llm_response}")

    #     # Map the identified vulnerability to a CWE
    #     cwe_id, cwe_name, cwe_description = fetch_cwe_by_vulnerability(llm_response)

    # Process CFG files and use LLM to prioritize paths
    for cfg_file in cfg_files:
        with open(cfg_file, "r") as f:
            cfg_data = f.read()

        # Construct the LLM prompt
        llm_prompt = PromptTemplate(
            input_variables=["cfg", "cwe_info"],
            template="""
            Given the following control flow graph:
            {cfg}

            CWE Information:
            {cwe_info}

            Which paths are most likely to contain vulnerabilities? Please prioritize and explain.
            """
        )
        cwe_info = f"ID: {cwe_id}, Name: {cwe_name}, Description: {cwe_description}" if cwe_id else "No CWE details available."
        llm_chain = LLMChain(llm=llm, prompt=llm_prompt)
        response = llm_chain.run(cfg=cfg_data, cwe_info=cwe_info)

        prioritized_paths.append(response)

    return prioritized_paths

# ============ Step 4: Use KLEE for Vulnerability Detection ===========

def run_klee(prioritized_paths, ll_file):
    """
    Run KLEE on prioritized paths to confirm vulnerabilities.
    """
    for path in prioritized_paths:
        # Ensure paths are sanitized for KLEE (extract function names from path)
        sanitized_path = extract_function_name(path)  # Modify this function to extract valid entry points
        print(f"Sanitized entry point: {sanitized_path}")
        
        klee_command = f"klee --only-output-states-covering-new {ll_file.replace('.ll', '.bc')} --entry-point={sanitized_path}"
        print(f"Running KLEE with command: {klee_command}")
        
        # Run the KLEE command
        subprocess.run(klee_command, shell=True, check=True)

def extract_function_name(path):
    """
    Extracts the function name from the prioritized path (you may need to customize this).
    """
    # Example: Extract function name from the path string (you may need to adjust this logic)
    # Assuming path is something like: "Path from Node0x5625c97e8da0 to Node0x5625c97e8e60"
    # Extract function name or basic block identifiers
    if "Node" in path:
        # Simulate extracting a function name or relevant entry point
        return "vulnerable_function"  # Replace with actual extraction logic
    else:
        return path.strip()  # Return sanitized path as a fallback


# ============ MAIN WORKFLOW ============ 
if __name__ == "__main__":
    # Initialize LLM
    load_dotenv()
    OpenAI.api_key = os.getenv("OPENAI_API_KEY")
    llm = OpenAI()

    # Provide source code file
    source_code_file = "example.c"
    
    # Optional: Provide a CWE ID (can be set to None to let the LLM detect)
    vulnerability_type = None  # Let LLM detect the vulnerability
    
    # Step 1: Generate LLVM IR
    llvm_ir_file = generate_llvm_ir(source_code_file)

    # Step 2: Generate CFG and prioritize paths
    prioritized_paths = generate_cfg_and_prioritize(llvm_ir_file, llm, vulnerability_type)

    # Step 3: Run KLEE on prioritized paths
    run_klee(prioritized_paths, llvm_ir_file)
