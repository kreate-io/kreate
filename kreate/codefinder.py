import copy
import os


class CodeFinder(object):

    def __init__(self, path, file_extensions, ignore_folders):
        self.path = path
        self.file_extensions = file_extensions
        self.ignore_folders = ignore_folders

    # Returns the list of files with the given extension in the directory and are not ignored by git.
    def get_code_files(self):

        files = []
        for extension in self.file_extensions:
            files += self.__get_files_with_extension_in_dir(
                self.path, extension)

        git_ignore_file_array = self.__get_files_with_extension_in_dir(
            self.path, ".gitignore")

        # if the repo is not a git repo, return all the files.
        if not git_ignore_file_array:
            return files

        git_ignore_file = git_ignore_file_array[0]

        result = copy.deepcopy(files)

        # Remove ignored files from the list
        for file in files:
            if self.__is_git_ignored(file, git_ignore_file):
                result.remove(file)

        return result

    # Checks if the given file is included in gitignore. Returns true if the file is ignore, false otherwise
    def __is_git_ignored(self, filepath, gitignorepath):

        file_extension = os.path.splitext(filepath)[1]

        filename = os.path.split(filepath)[1]

        if not file_extension or not filename:
            print("Provide full path and file name with extension")
            return False

        foldername = os.path.dirname(filepath)
        foldername = os.path.basename(foldername)

        with open(gitignorepath) as f:
            git_ignore_lines = f.readlines()

        for line in git_ignore_lines:
            if line.startswith("#"):
                continue
            if line.rstrip() == filename or foldername in line or file_extension in line.rstrip() == file_extension:
                return True

        return False

    # Returns the list of files that have the given extension in the given directory.
    # Traverses the folders under the given directory.
    def __get_files_with_extension_in_dir(self, path, file_extension):

        if file_extension.startswith(".") is False:
            file_extension = "." + file_extension

        list_of_files = []

        for root, dirs, files in os.walk(path, topdown=True):
            dirs[:] = [d for d in dirs if d not in self.ignore_folders]
            for file in files:
                if file.endswith(file_extension):
                    list_of_files.append(os.path.join(root, file))

        return list_of_files
