import os
import copy

class CodeFinder(object):

    def __init__(self, path, fileExtensions):
        self.path = path
        self.fileExtensions = fileExtensions

    # Returns the list of files with the given extension in the directory and are not ignored by git.
    def getCodeFiles(self):

        files = []
        for extension in self.fileExtensions:
          files += self.getFilesWithExtensionInDir(self.path, extension)

        gitignorefilearray = self.getFilesWithExtensionInDir(self.path, ".gitignore")

        # if the repo is not a git repo, return all the files.
        if not gitignorefilearray:
            return files

        gitignorefile = gitignorefilearray[0]

        result = copy.deepcopy(files)

        # Remove ignored files from the list
        for file in files:
            if self.isGitIgnored(file, gitignorefile):
                result.remove(file)

        return result

    # Checks if the given file is included in gitignore. Returns true if the file is ignore, false otherwise
    def isGitIgnored(self, filepath, gitignorepath):
        
        file_extension = os.path.splitext(filepath)[1]

        filename = os.path.split(filepath)[1]

        if not file_extension or not filename:
            print("Provide full path and file name with extension")
            return False
        
        foldername = os.path.dirname(filepath)
        foldername = os.path.basename(foldername)

        with open(gitignorepath) as f:
            gitignorelines = f.readlines()

        for line in gitignorelines:
            if line.startswith("#"): continue
            if line.rstrip() == filename or foldername in line or file_extension in line.rstrip() == file_extension:
                return True
        
        return False

    # Returns the list of files that have the given extension in the given directory.
    # Traverses the folders under the given directory.
    def getFilesWithExtensionInDir(self, path, fileExtension):
        
        if (fileExtension.startswith(".") is False):
            fileExtension = "." + fileExtension

        listOfFiles = []

        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(fileExtension):
                    listOfFiles.append(os.path.join(root, file))
        
        return listOfFiles