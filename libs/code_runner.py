import subprocess
import tempfile
import libs.logger as logger

class CodeRunner:
    def __init__(self):
        self.logger = logger.Logger.setup_logger()
        self.logger.info("CodeRunner initialized.")
        
    def run_code(self,code, language):
        self.logger.info(f"Running code: {code[:100]} in language: {language}")

        # Check for code and language validity
        if not code or len(code.strip()) == 0:
            return "Code is empty. Cannot execute an empty code.",None
        
        # Check for compilers on the system
        compilers_status = self.check_compilers(language)
        if not compilers_status:
            return "Compilers not found. Please install compilers on your system.",None
        
        if language == "Python":
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=True) as file:
                file.write(code)
                file.flush()

                self.logger.info(f"Input file: {file.name}")
                output = subprocess.run(
                    ["python", file.name], capture_output=True, text=True)
                self.logger.info(f"Runner Output execution: {output.stdout + output.stderr}")
                return output.stdout,output.stderr

        elif language == "C" or language == "C++":
            ext = ".c" if language == "C" else ".cpp"
            with tempfile.NamedTemporaryFile(mode="w", suffix=ext, delete=True) as src_file:
                src_file.write(code)
                src_file.flush()

                self.logger.info(f"Input file: {src_file.name}")

                with tempfile.NamedTemporaryFile(mode="w", suffix="", delete=True) as exec_file:
                    compile_output = subprocess.run(
                        ["gcc" if language == "C" else "g++", "-std=c++17", "-o", exec_file.name, src_file.name], capture_output=True, text=True)

                    if compile_output.returncode != 0:
                        return None,compile_output.stderr

                    self.logger.info(f"Output file: {exec_file.name}")
                    run_output = subprocess.run(
                        [exec_file.name], capture_output=True, text=True)
                    self.logger.info(f"Runner Output execution: {run_output.stdout , run_output.stderr}")
                    return run_output.stdout,run_output.stderr

        elif language == "JavaScript":
            with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=True) as file:
                file.write(code)
                file.flush()

                self.logger.info(f"Input file: {file.name}")
                output = subprocess.run(
                    ["node", file.name], capture_output=True, text=True)
                self.logger.info(f"Runner Output execution: {output.stdout + output.stderr}")
                return output.stdout,output.stderr
            
        elif language == "Java":
                with tempfile.NamedTemporaryFile(mode="w", suffix=".java", delete=True) as file:
                    file.write(code)
                    file.flush()
                    classname = "Main"  # Assuming the class name is Main, adjust if needed
                    compile_output = subprocess.run(["javac", file.name], capture_output=True, text=True)
                    if compile_output.returncode != 0:
                        return None,compile_output.stderr
                    run_output = subprocess.run(["java", "-cp", tempfile.gettempdir(), classname], capture_output=True, text=True)
                    return run_output.stdout,run_output.stderr

        elif language == "Swift":
                with tempfile.NamedTemporaryFile(mode="w", suffix=".swift", delete=True) as file:
                    file.write(code)
                    file.flush()
                    output = subprocess.run(["swift", file.name], capture_output=True, text=True)
                    return output.stdout,output.stderr

        elif language == "C#":
                with tempfile.NamedTemporaryFile(mode="w", suffix=".cs", delete=True) as file:
                    file.write(code)
                    file.flush()
                    compile_output = subprocess.run(["csc", file.name], capture_output=True, text=True)
                    if compile_output.returncode != 0:
                        return compile_output.stderr
                    exe_name = file.name.replace(".cs", ".exe")
                    run_output = subprocess.run([exe_name], capture_output=True, text=True)
                    return run_output.stdout,run_output.stderr

        elif language == "Scala":
                with tempfile.NamedTemporaryFile(mode="w", suffix=".scala", delete=True) as file:
                    file.write(code)
                    file.flush()
                    output = subprocess.run(["scala", file.name], capture_output=True, text=True)
                    return output.stdout,output.stderr

        elif language == "Ruby":
                with tempfile.NamedTemporaryFile(mode="w", suffix=".rb", delete=True) as file:
                    file.write(code)
                    file.flush()
                    output = subprocess.run(["ruby", file.name], capture_output=True, text=True)
                    return output.stdout,output.stderr

        elif language == "Kotlin":
                with tempfile.NamedTemporaryFile(mode="w", suffix=".kt", delete=True) as file:
                    file.write(code)
                    file.flush()
                    compile_output = subprocess.run(["kotlinc", file.name, "-include-runtime", "-d", "output.jar"], capture_output=True, text=True)
                    if compile_output.returncode != 0:
                        return compile_output.stderr
                    run_output = subprocess.run(["java", "-jar", "output.jar"], capture_output=True, text=True)
                    return run_output.stdout,run_output.stderr

        elif language == "Go":
                with tempfile.NamedTemporaryFile(mode="w", suffix=".go", delete=True) as file:
                    file.write(code)
                    file.flush()
                    compile_output = subprocess.run(["go", "build", "-o", "output.exe", file.name], capture_output=True, text=True)
                    if compile_output.returncode != 0:
                        return None,compile_output.stderr
                    run_output = subprocess.run(["./output.exe"], capture_output=True, text=True)
                    return run_output.stdout,run_output.stderr
        else:
            return "Unsupported language.",None
        
    def check_compilers(self, language):
        language = language.lower().strip()
        
        compilers = {
            "python": ["python", "--version"],
            "nodejs": ["node", "--version"],
            "c": ["gcc", "--version"],
            "c++": ["g++", "--version"],
            "csharp": ["csc", "--version"],
            "go": ["go", "version"],
            "ruby": ["ruby", "--version"],
            "java": ["java", "--version"],
            "kotlin": ["kotlinc", "--version"],
            "scala": ["scala", "--version"],
            "swift": ["swift", "--version"]
        }

        if language not in compilers:
            logger.error("Invalid language selected.")
            return False

        compiler = subprocess.run(compilers[language], capture_output=True, text=True)
        if compiler.returncode != 0:
            logger.error(f"{language.capitalize()} compiler not found.")
            return False

        return True