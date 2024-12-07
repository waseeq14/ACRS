import clang.cindex
import openai
import os
import networkx as nx
import matplotlib.pyplot as plt
import re
from clang.cindex import Config, CursorKind, Index
import subprocess


# Set up Clang library and OpenAI API
clang.cindex.Config.set_library_file("/usr/lib/llvm-17/lib/libclang.so.1")


openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

cfg = nx.DiGraph()  # CFG graph
allocations, freed_variables = {}, {}
free_arguments = set()

def load_dangerous_functions(file_path="criticalFunc.txt"):
    dangerous_functions = []
    try:
        with open(file_path, "r") as file:
            dangerous_functions = [line.strip() for line in file if line.strip()]
        #print(f"Loaded dangerous functions: {dangerous_functions}")
    except FileNotFoundError:
        print(f"Warning: Dangerous functions file '{file_path}' not found.")
    return dangerous_functions

DANGEROUS_FUNCTIONS = load_dangerous_functions()

def analyze_file_functions(file_path):
    index = Index.create()
    translation_unit = index.parse(file_path)
    defined_functions = {}
    call_graph = {}  # Store the function call graph
    main_function = None

    # Collect all defined functions and prioritize 'main'
    for node in translation_unit.cursor.get_children():
        if node.kind == CursorKind.FUNCTION_DECL:
            call_graph[node.spelling] = []  # Initialize graph node
            if node.spelling == "main":
                main_function = node
            else:
                defined_functions[node.spelling] = node

    # Analyze 'main' function first
    if main_function:
        print("[*] Starting analysis from 'main' function:\n")
        analyze_function(main_function, defined_functions, call_graph)
    else:
        print("No 'main' function found.\n")

    # Analyze remaining functions
    print("\n[*]Analyzing remaining functions:")
    for function_name, function_node in defined_functions.items():
        analyze_function(function_node, defined_functions, call_graph)

    # Display function call graph
    print("\n[*] Function Call Graph:")
    fcg = display_call_graph(call_graph)

def analyze_function(function_node, defined_functions, call_graph):
    print(f"\nAnalyzing function '{function_node.spelling}'")
    for node in function_node.get_children():
        if node.kind == CursorKind.CALL_EXPR:
            function_name = node.spelling
            if function_name:
                # Detect critical functions
                if function_name in DANGEROUS_FUNCTIONS:
                    print(f"Critical  detected: '{function_name}' at line {node.location.line}")
                
                # Add function call to the graph
                call_graph[function_node.spelling].append(function_name)

        # Track memory allocations and deallocations
        analyze_ast_with_memory(node)

        # Recursively analyze child nodes
        analyze_function_recursive(node, call_graph, function_node.spelling)

def analyze_function_recursive(node, call_graph, current_function):
    """
    Recursive traversal to find all function calls in a given node and detect critical functions.
    """
    for child in node.get_children():
        if child.kind == CursorKind.CALL_EXPR:
            function_name = child.spelling
            if function_name:
                # Detect critical functions
                if function_name in DANGEROUS_FUNCTIONS:
                    print(f"Critical function detected: '{function_name}' at line {child.location.line}")
                # Add function call to the graph
                call_graph[current_function].append(function_name)

        # Continue recursion
        analyze_function_recursive(child, call_graph, current_function)

def analyze_code(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    
    analyze_ast(translation_unit.cursor)

def analyze_ast(node):
    if node.kind == clang.cindex.CursorKind.CALL_EXPR:
        if node.spelling in DANGEROUS_FUNCTIONS:
            context_code = get_context_code(node)
            gpt_response = analyze_with_llm(node.spelling, context_code)
            print(f"\nLLM Analysis for {node.spelling}:\n{gpt_response}")
    for child in node.get_children():
        analyze_ast(child)

def get_context_code(node, context_radius=2):
    start_line, end_line = max(0, node.location.line - context_radius), node.location.line + context_radius
    with open(node.location.file.name, 'r') as f:
        return ''.join(f.readlines()[start_line:end_line])

def analyze_with_llm(function_name, context_code):
    prompt = f"""
    Analyze the following code excerpt with a focus on the specific use of the function '{function_name}' in its immediate context. Provide a concise output that addresses:

    1. *Contextual Issues*: Identify any specific bugs, security risks, or vulnerabilities associated with the current use of '{function_name}' here. Do not include general issues unless directly relevant to this use, and avoid giving corrected code.
    2. *Context-Based Recommendations*: Give a brief recommendation only if improvements or safety checks are necessary. If the usage is potentially safe in this context, indicate it as 'potentially safe' without further explanation.

    Function Name: {function_name}

    Code Context:
    {context_code}
    """
    try:
        response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}], max_tokens=150, temperature=0.3)
        return response.choices[0].message.content
    except Exception as e:
        print("Error calling GPT API:", e)
        return "Analysis could not be performed."


def analyze_code_with_memory_checks(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    analyze_ast_with_memory(translation_unit.cursor)

def analyze_ast_with_memory(node):
    global allocations, freed_variables, free_arguments
    if node.kind == clang.cindex.CursorKind.CALL_EXPR:
        function_name = node.spelling
        if function_name in ["malloc", "calloc", "realloc"]:
            variable_name = get_assigned_variable(node)
            if variable_name:
                if variable_name not in allocations:
                    allocations[variable_name] = node.location.line
                else:
                    result = f"Double Allocations of variable '{variable_name}' at line {node.location.line}"
                    print(result)
                    return result
                if variable_name in freed_variables:
                    del freed_variables[variable_name]
        elif function_name == "free":
            variable_name = get_argument_variable(node)
            if variable_name in allocations:
                freed_variables[variable_name] = node.location.line
                del allocations[variable_name]
            elif variable_name in freed_variables:
                result = f"Double-Free Warning: '{variable_name}' freed again at line {node.location.line}"
                print(result)
                return result
            else:
                result = f"Warning: Attempt to free unallocated variable '{variable_name}' at line {node.location.line}"
                print(result)
                return result
    elif node.kind == clang.cindex.CursorKind.DECL_REF_EXPR:
        variable_name = node.spelling 
        line = get_exact_line(node)
        if variable_name in freed_variables and "free(" not in line:
            result = f"Use-After-Free detected: '{variable_name}' at line {node.location.line}, originally freed at line {freed_variables[variable_name]}"
            print(result)
            return result
    for child in node.get_children():
        analyze_ast_with_memory(child)

def get_assigned_variable(node):
    file_path = node.location.file.name
    line_number = node.location.line
    
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            code_line = lines[line_number - 1].strip()  # line_number is 1-based index

            match = re.match(r'''
                ^\s*                                  # Optional leading whitespace
                (?:[a-zA-Z_][a-zA-Z0-9_]*\s+)?        # Optional data type (e.g., "int")
                (?:\*+)?                              # Optional pointer asterisk(s) (e.g., "*")
                ([a-zA-Z_][a-zA-Z0-9_]*)              # Variable name
                \s*=\s*                               # Assignment operator with optional spaces
                .+;                                   # Rest of the statement ending with a semicolon
            ''', code_line, re.VERBOSE)

            if match:
                variable_name = match.group(1)  
                print(f"Assigned variable: {variable_name}")
                return variable_name
            else:
                print("No variable assignment found.")
                return None

    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def get_exact_line(node):
    file_path = node.location.file.name
    line_number = node.location.line
    
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            code_line = lines[line_number - 1].strip()  # line_number is 1-based index
            return code_line

    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def get_argument_variable(node):
    arguments = list(node.get_arguments()) 
    if not arguments:
        return None

    arg = arguments[0]  
    if arg.type.kind != clang.cindex.TypeKind.POINTER:
        print(f"Incompatible type: {arg.type.kind}. Expected a pointer.")
        return None

    return arg.spelling 

def analyze_code_with_cfg(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    analyze_ast_with_cfg(translation_unit.cursor)

def analyze_ast_with_cfg(node):
    if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
        current_node = node.spelling
        cfg.add_node(current_node, label=node.spelling)
        traverse_cfg_blocks(node, current_node)

def traverse_cfg_blocks(node, current_node):
    for child in node.get_children():
        if child.kind in [clang.cindex.CursorKind.IF_STMT, clang.cindex.CursorKind.FOR_STMT, clang.cindex.CursorKind.WHILE_STMT]:
            block_node = f"{child.kind.spelling}_{child.location.line}"
            cfg.add_node(block_node, label=child.kind.spelling)
            cfg.add_edge(current_node, block_node)
            traverse_cfg_blocks(child, block_node)
        elif child.kind == clang.cindex.CursorKind.RETURN_STMT:
            return_node = f"return_{child.location.line}"
            cfg.add_node(return_node, label="RETURN")
            cfg.add_edge(current_node, return_node)
        else:
            traverse_cfg_blocks(child, current_node)

def plot_cfg():
    pos = nx.spring_layout(cfg)
    labels = nx.get_node_attributes(cfg, 'label')
    nx.draw(cfg, pos, with_labels=True, labels=labels, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold')
    plt.show()
    
    
def display_call_graph(call_graph):
    """
    Display the function call graph in a simple textual format.
    """
    for function, calls in call_graph.items():
        result = f"{function} -> {', '.join(calls) if calls else 'None'}"
        print(result)
        return result


def remove_include_statements(file_path):
    
    with open(file_path, 'r') as read_file:
        with open('temp.c', 'w') as temp_file:
            pattern = re.compile(r'#include\s?<')
            lines = read_file.readlines()

            for line in lines:
                if not pattern.match(line):
                    temp_file.write(line)


def sanitizer(file_path):
    """
    Compiles and runs a C file with Clang's Address Sanitizer (ASan) enabled,
    then displays the output to the user.

    :param file_path: Path to the C program file
    """
    # Temporary executable file name
    

    try:
        # Compile the file with ASan enabled
        compile_command = [
            "clang", "-fsanitize=address", "-O1", "-fno-omit-frame-pointer","-g" ,file_path
        ]
        print(f"Compiling {file_path} with Address Sanitizer...")
        subprocess.run(compile_command, check=True)

        # Run the compiled program
        print(f"Running {file_path} with Address Sanitizer...")
        run_command = ["./a.out"]
        sans = subprocess.run(run_command, check=True)
        return sans

    except subprocess.CalledProcessError as e:
        print(f"Error during compilation or execution: {e}")
        return

    finally:
        # Cleanup: Remove the compiled executable
        print("HABSHI")
        return

def final_analysis(file_path,memory,functions,sanitizer):
    
    with open(file_path, 'r') as file:
        # Read the contents of the file
        file_contents = file.read()
        print(file_contents)

    prompt = f"""
    Analyze the given source code\n {file_contents} \n
    To identify vulnerabilities related to memory management and potential privilege escalation risks:
    You're given the following details
    1.memory details: \n{memory}\n
    2.function call graph details: \n{functions}\n
    3.memory sanitizer info: \n{sanitizer}\n

    based on this information
    Identity:

    1.Name of Vulnerability or Vulnerabilities in form e.g (bufferoverflow, read after write) etc
    2.How can each lead to privledge escalation
    3.Remediation techniques

    Give very breif answers and be direct
    
    """
    try:
        response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}], max_tokens=150, temperature=0.3)
        print(response.choices[0].message.content)
        
    except Exception as e:
        print("Error calling GPT API:", e)
        return "Analysis could not be performed."

file_path = "doublefree.c"
#analyze_code(file_path)

remove_include_statements(file_path)
mem = analyze_code_with_memory_checks("temp.c")
fcg = analyze_file_functions("temp.c")
sani = sanitizer(file_path)
final_analysis(file_path,mem,fcg,sani)

#analyze_code_with_cfg(file_path)
#plot_cfg()
