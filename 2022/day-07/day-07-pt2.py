# Based on https://medium.com/@datasciencedisciple/advent-of-code-2022-in-python-day-7-47a94b090949 fpr part 1, part2 independent


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
    return {"part1": sum(final_list_task_1), "part2": directories_size}


with open('input.txt', 'r')as f:
    result = file_system(f)
    print("part 1 solution is: %d " % result["part1"])
    storage_in_use = result["part2"]["/"]
    free_space = 70000000 - storage_in_use
    shortfall = 30000000 - free_space

    sorted_file_system = sorted((result["part2"]).items(), key=lambda x: x[1])

    for key, value in sorted_file_system:
        if value < shortfall:
            continue
        else:
            target_dir = key, value
            break
    print("part 2 solution is: %s %d " % (target_dir[0], target_dir[1]))
