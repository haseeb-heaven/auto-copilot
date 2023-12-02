import os
import libs.logger
from watchdog.events import FileSystemEventHandler
from libs.code_runner import CodeRunner

class FileMonitor(FileSystemEventHandler):
    def __init__(self, filename, compiler):
        self.last_modified = os.path.getmtime(filename)
        self.filename = filename
        self.compiler = compiler
        self.logger = libs.logger.setup_logger()

    def on_modified(self, event):
        self.logger.info(f"Event: {event} src_path: {event.src_path} filename: {self.filename}")
        if self.filename in event.src_path:
            self.logger.info(f"File {self.filename} modified.")
            current_modified = os.path.getmtime(self.filename)
            if current_modified != self.last_modified:
                self.last_modified = current_modified
                self.logger.info(f"File {self.filename} modified. Compiling and running.")
                runner = CodeRunner()
                self.logger.info(f"Running code: {open(self.filename).read()}")
                result = runner.run_code(open(self.filename).read(), self.compiler)
                
                # Print the compiler output to the console
                print(result)