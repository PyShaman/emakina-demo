import filecmp


class DirectoryComparison:
    def __init__(self):
        pass

    @staticmethod
    def return_common_files_list(directory_1, directory_2):
        return filecmp.dircmp(directory_1, directory_2).common_files
