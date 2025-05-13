def read_file_content(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def read_segments(project_folder, language):
    index = 1
    segments = []

    while True:
        try:
            with open(f'{project_folder}/segment_{index}_klee.{language}', 'r') as f:
                segments.append(f.read())
            index += 1
        except Exception:
            break

    return segments

def read_seeds(project_folder):
    index = 0
    seeds = ''

    while True:
        try:
            with open(f'{project_folder}/in/seed_{index}.txt', 'r') as f:
                newStr = []
                for line in f.readlines():
                    newStr.append(line.strip())
                seeds += '###'.join(newStr) + '\n'
            index += 1
        except Exception:
            break

    return seeds

def extract_vuln_names(description):
    if description[0] == '[':
        description_list = eval(description)
        
        vulnerabilities = []
        
        for desc in description_list:
            lines = desc.splitlines()
            start_extracting = False

            for line in lines:
                if "Vulnerability Names:" in line or "Vulnerability Types:" in line:
                    start_extracting = True
                    continue
                if start_extracting:
                    line = line.strip()
                    if line.startswith("- "):
                        vuln = line[2:].strip()
                        if vuln not in vulnerabilities:
                            vulnerabilities.append(vuln)
                    elif line == "":
                        break

        return vulnerabilities
    else:  
        lines = description.splitlines()
        vulnerabilities = []
        start_extracting = False

        for line in lines:
            if "Vulnerability Names:" in line or "Vulnerability Types:" in line:
                start_extracting = True
                continue
            if start_extracting:
                line = line.strip()
                if line.startswith("- "):
                    vulnerabilities.append(line[2:].strip())
                elif line == "":
                    break

        return vulnerabilities