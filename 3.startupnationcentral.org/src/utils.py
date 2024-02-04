import json


def get_file_name(url):
    return url.replace("/", "_").replace(":", "_").replace("-", "_").replace(".", "_")


def write_json(data, target_file_path):
    with open(target_file_path, "w", encoding="utf-8") as jw:
        json.dump(data, jw, indent=2, ensure_ascii=False)


def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as jr:
        return json.load(jr)


def write_lines_txt(data_lines, target_file_path):
    with open(target_file_path, "w", encoding="utf-8") as fw:
        fw.writelines([item + "\n" if idx != len(data_lines) - 1 else item for idx, item in enumerate(data_lines)])


def read_lines_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as fr:
        return [item.strip("\n") for item in fr.readlines()]
