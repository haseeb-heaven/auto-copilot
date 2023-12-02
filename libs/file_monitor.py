import os
import time
import libs.logger
from watchdog.events import FileSystemEventHandler
from libs.code_runner import CodeRunner
import pyautogui
import pyperclip

class FileMonitor(FileSystemEventHandler):
    def __init__(self, filename, compiler):
        self.last_modified = os.path.getmtime(filename)
        self.filename = filename
        self.compiler = compiler
        self.logger = libs.logger.setup_logger()

    def self_fix_error(self, result:str):

        # show the UI error window 
        print("Fixing the auto error")
        #pyautogui.alert(result, "Error", button="OK")

        self.logger.info("Trying to copy the error to the clipboard")
        
        result = "This is the error in the code \n" + result + "\n Please try to fix it and only give relevant code thats it"
        if result:
            pyperclip.copy(result)
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
        
        
        time.sleep(20)
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
                code_output = runner.run_code(open(self.filename).read(), self.compiler)
                
                # Print the compiler output to the console
                # clear the previous output
                print("\033c")
                print(code_output)

                try:
                    # check if result is an error
                    if "error" in code_output.lower():
                        result = self.self_fix_error(code_output)
                        if result:
                            print("Error fixed")
                            code_output = ""
                        
                except Exception as exception:
                    self.logger.error(f"Error in code: {exception}")
                    print("Exception: ", exception)