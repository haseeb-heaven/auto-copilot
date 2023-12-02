import os
import logging
from watchdog.events import FileSystemEventHandler
from code_runner import CodeRunner

class FileMonitor(FileSystemEventHandler):
    def __init__(self, filename, compiler):
        self.last_modified = os.path.getmtime(filename)
        self.filename = filename
        self.compiler = compiler
        self.logger = logging.getLogger('live_coding_editor')

    def on_modified(self, event):
        self.logger.info(f"Event: {event} src_path: {event.src_path} filename: {self.filename}")
        if self.filename in event.src_path:
            self.logger.info(f"File {self.filename} modified.")
            current_modified = os.path.getmtime(self.filename)
            if current_modified != self.last_modified:
                self.last_modified = current_modified
                logging.info(f"File {self.filename} modified. Compiling and running.")
                runner = CodeRunner()
                logging.info(f"Running code: {open(self.filename).read()}")
                result = runner.run_code(open(self.filename).read(), self.compiler)
                self.logger.info(f"Result: {result}")