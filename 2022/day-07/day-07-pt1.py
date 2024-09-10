# Based on https://medium.com/@datasciencedisciple/advent-of-code-2022-in-python-day-7-47a94b090949


def add_path_to_directories(path, directories):
    if path not in directories.keys():
        directories[path] = 0
    return directories


def file_system(f):
    directories_size = {}
    current_stack = []
    current_path = ""
    for line in f:
        if not line:
            continue
        if line.startswith("$ cd"):
            if not line.startswith("$ cd ..") and not line.startswith("$ cd /"):
                current_path += f"/{line.split()[-1]}" if current_path != "/" else line.split(
                )[-1]
                current_stack.append(current_path)
                directories_size = add_path_to_directories(
                    current_path, directories_size)

            elif line.strip() == "$ cd /":
                current_path = "/"
                current_stack = ["/"]
                directories_size = add_path_to_directories(
                    current_path, directories_size)

            elif line.strip() == "$ cd ..":
                current_path = "/".join(current_path.split("/")[:-1])
                current_stack.pop()

        if line[0].isdigit():
            file_size = int(line.split()[0])
            for directory in current_stack:
                directories_size[directory] = directories_size.get(
                    directory, 0) + file_size

    final_list_task_1 = [
        el for el in directories_size.values() if el <= 100000]
    return sum(final_list_task_1)


with open('input.txt', 'r')as f:
    print(file_system(f))
