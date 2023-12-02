import os

class CompilerManager:
    def __init__(self):
        self.extensions_to_language = {
            ".py": "Python",
            ".c": "C",
            ".cpp": "C++",
            ".java": "Java",
            ".swift": "Swift",
            ".js": "JavaScript",
            ".scala": "Scala",
            ".rb": "Ruby",
            ".cs": "C#", # C Sharp
            ".go": "Go",
            ".rs": "Rust",
            ".kt": "Kotlin",
        }

    def get_extension(self, filename):
        return os.path.splitext(filename)[1]

    def get_compiler(self, extension):
        return self.extensions_to_language.get(extension)