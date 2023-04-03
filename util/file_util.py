import os

from config import constants


def put_cache_data(file_path, text):
    _, file_full_name = os.path.split(file_path)
    file_name, _ = os.path.splitext(file_full_name)
    with open(constants.path_text_list, "a", encoding="utf-8") as file_object:
        content = text.strip().replace("\n", " ")
        file_object.write(file_name + " | " + content + " | " + file_path)
        file_object.write("\n")


def get_cache_data():
    result = []
    # index = 1
    if os.path.exists(constants.path_text_list):
        with open(constants.path_text_list, "r", encoding="utf-8") as file_object:
            lines = file_object.readlines()
            for line in lines:
                lis = line.strip().split(" | ")
                # lis.insert(0, str(index))
                result.append(lis)
                # index += 1
    return result


def delete_row(index):
    with open(constants.path_text_list, 'r+') as file_object:
        lines = file_object.readlines()
        file_object.seek(0)
        file_object.truncate()
        for number, line in enumerate(lines):
            if number is not index:
                file_object.write(line)
