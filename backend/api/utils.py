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