import os
import re


class ValidationCounter:
    def __init__(self):
        pass

    @staticmethod
    def get_file_list(directory):
        file_list = []
        for files in os.listdir(directory):
            file_list.append(files)
        return file_list

    @staticmethod
    def count_validations(file_list, directory):
        validations = 0
        for file in file_list:
            with open(directory + file, "r") as f:
                count = int(re.findall("(?<=Found ).*?(?= accessibility violations:)", f.read())[0])
                validations += count
        return validations

    @staticmethod
    def get_url_from_file_list(file_list, directory):
        url_list = []
        for file in file_list:
            with open(directory + file, "r") as f:
                url = re.match("https://[a-z./-]*", f.readline())[0]
                url_list.append(url)
        return url_list

    @staticmethod
    def return_common_files(list_1, list_2):
        return list(set(list_1) & set(list_2))
