import os
import time
import libs.logger
from watchdog.events import FileSystemEventHandler
from libs.code_runner import CodeRunner
import pyautogui
import pyperclip

class FileMonitor(FileSystemEventHandler):
    monitor_time = 15 # 15 seconds
    
    def __init__(self, filename, compiler):
        self.last_modified = os.path.getmtime(filename)
        self.filename = filename
        self.compiler = compiler
        self.logger = libs.logger.setup_logger()

    def self_fix_error(self,code_error):

        # show the UI error window 
        print("Fixing the auto error")

        self.logger.info("Trying to copy the error to the clipboard")
        
        result = "This is the error in the code \n" + code_error + "\n Please try to fix it and only give relevant code and dont change everything \n"
        if result:
            pyperclip.copy(code_error)
        else:
            self.logger.info("Error is empty")
            print("Error is empty")
            return False
        
        self.logger.info("Copied the error to the clipboard")
        print("Copied the error to the clipboard")
        
        # selecting all code
        self.logger.info("Trying to select all code")
        print("Trying to select all code")
        pyautogui.hotkey('command', 'a')
        time.sleep(1)
        
        self.logger.info("Trying to open the interactive window")
        print("Trying to open the interactive window")
        # using pyautgui click these keys to open the interactive window
        pyautogui.hotkey('alt', 'k')
        self.logger.info("Opened the interactive window")
        time.sleep(3)
        self.logger.info("Trying to paste the error in the interactive window")
        print("Trying to paste the error in the interactive window")
        # paste the error in the interactive window
        pyautogui.hotkey('command', 'v')
        self.logger.info("Pasted the error in the interactive window")
        print("Pasted the error in the interactive window")
        pyautogui.press('enter')
        
        
        time.sleep(self.monitor_time)
        print("Trying accepting the solution")
        pyautogui.hotkey('alt', 'enter')
        print("Fixed the error with the solution")
        
        # save the file
        self.logger.info("Trying to save the file")
        print("Trying to save the file")
        pyautogui.hotkey('command', 's')
        self.logger.info("Saved the file")
        
        return True
                    
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
                code_output,code_error = runner.run_code(open(self.filename).read(), self.compiler)
                
                # Print the compiler output to the console
                # clear the previous output
                print("\033c")
                print(f"Output: {code_output}")
                print(f"Error: {code_error}")

                try:
                    # check if result is an error
                    if code_error:
                        result = self.self_fix_error(code_error)
                        if result:
                            print("Error fixed")
                            code_error = None # Clear the error
                        
                except Exception as exception:
                    raise exception