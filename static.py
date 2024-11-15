import clang.cindex
import openai
import os
import networkx as nx
import matplotlib.pyplot as plt
from dotenv import load_dotenv


# Set up Clang library and OpenAI API
clang.cindex.Config.set_library_file("/usr/lib/llvm-10/lib/libclang.so.1")

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

cfg = nx.DiGraph()  # CFG graph
allocations, freed_variables = {}, {}

def load_dangerous_functions(file_path="criticalFunc.txt"):
    dangerous_functions = []
    try:
        with open(file_path, "r") as file:
            dangerous_functions = [line.strip() for line in file if line.strip()]
        print(f"Loaded dangerous functions: {dangerous_functions}")
    except FileNotFoundError:
        print(f"Warning: Dangerous functions file '{file_path}' not found.")
    return dangerous_functions

DANGEROUS_FUNCTIONS = load_dangerous_functions()

def analyze_code(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    analyze_ast(translation_unit.cursor)

def analyze_ast(node):
    if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
        if node.spelling in DANGEROUS_FUNCTIONS:
            context_code = get_context_code(node)
            gpt_response = analyze_with_llm(node.spelling, context_code)
            print(f"LLM Analysis for {node.spelling}:\n{gpt_response}")
    for child in node.get_children():
        analyze_ast(child)

def get_context_code(node, context_radius=3):
    start_line, end_line = max(0, node.location.line - context_radius), node.location.line + context_radius
    with open(node.location.file.name, 'r') as f:
        return ''.join(f.readlines()[start_line:end_line])

def analyze_with_llm(function_name, context_code):
    prompt = f"Analyze the following code:\n\nFunction: {function_name}\n\nCode:\n{context_code}"
    try:
        response = openai.Completion.create(engine="gpt-4", prompt=prompt, max_tokens=150, temperature=0.3)
        return response.choices[0].text.strip()
    except Exception as e:
        print("Error calling GPT API:", e)
        return "Analysis could not be performed."

def analyze_code_with_memory_checks(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    analyze_ast_with_memory(translation_unit.cursor)

def analyze_ast_with_memory(node):
    global allocations, freed_variables
    if node.kind == clang.cindex.CursorKind.CALL_EXPR:
        function_name = node.spelling
        if function_name in ["malloc", "calloc", "realloc"]:
            variable_name = get_assigned_variable(node)
            if variable_name:
                allocations[variable_name] = node.location.line
                freed_variables.pop(variable_name, None)
        elif function_name == "free":
            variable_name = get_argument_variable(node)
            if variable_name in allocations:
                if variable_name in freed_variables:
                    print(f"Double-Free Warning: '{variable_name}' freed again at line {node.location.line}")
                else:
                    freed_variables[variable_name] = node.location.line
                    del allocations[variable_name]
            else:
                print(f"Warning: Attempt to free unallocated variable '{variable_name}' at line {node.location.line}")
    elif node.kind == clang.cindex.CursorKind.DECL_REF_EXPR:
        if node.spelling in freed_variables:
            print(f"Use-After-Free detected: '{node.spelling}' at line {freed_variables[node.spelling]}")
    for child in node.get_children():
        analyze_ast_with_memory(child)

def get_assigned_variable(node):
    parent = node.semantic_parent
    return parent.spelling if parent and parent.kind == clang.cindex.CursorKind.VAR_DECL else None

def get_argument_variable(node):
    for arg in node.get_arguments():
        if arg.kind == clang.cindex.CursorKind.DECL_REF_EXPR:
            return arg.spelling
    return None

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

file_path = "vuln.c"
analyze_code(file_path)
analyze_code_with_memory_checks(file_path)
analyze_code_with_cfg(file_path)
plot_cfg()
