import sys
import time
from watchdog.observers import Observer
from libs.file_monitor import FileMonitor
from libs.compiler_manager import CompilerManager
import libs.logger

def auto_copilot(filename, interval_time, monitor_time):
    logger = libs.logger.Logger.setup_logger()  # Setting up the logger

    compiler_manager = CompilerManager()  # Creating an instance of CompilerManager class
    file_extension = compiler_manager.get_extension(filename)  
    compiler = compiler_manager.get_compiler(file_extension) 

    if not compiler:
        logger.error("Compiler not found for file extension: %s", file_extension) 
        return

    logger.info("Using compiler: %s", compiler) 
    event_handler = FileMonitor(filename, compiler, monitor_time)  # Creating an instance of FileMonitor class
    logger.info("Watching file: %s", filename)  
    
    observer = Observer()  # Creating an instance of Observer class
    observer.schedule(event_handler, path='.', recursive=False)  # Scheduling the event handler for file monitoring
    observer.start()  # Starting the observer
    logger.info("Started watching file: %s", filename) 

    print(f"Auto Copilot is running.\n")
    print(f"Watching file:'{filename}' for every {interval_time} seconds. Auto fix error after {monitor_time} seconds")
    try:
        while True:
            time.sleep(interval_time)  
    except KeyboardInterrupt:
        observer.stop()  # Stopping the observer on keyboard interrupt
    except Exception as e:
        logger.error("An error occurred: %s", str(e))  # Logging any other exceptions
    finally:
        observer.join()  # Joining the observer thread
        print("Auto Copilot stopped.")

if __name__ == "__main__":
    try:
        # Getting arguments from command line
        filename = sys.argv[1]  

        # Set the default values for the arguments
        interval_time = 5
        monitor_time = 15

        # Check if optional arguments are provided
        if len(sys.argv) > 2:
            interval_time = int(sys.argv[2])
        if len(sys.argv) > 3:
            monitor_time = int(sys.argv[3])
        
        auto_copilot(filename, interval_time, monitor_time)  # Calling the auto_copilot function with provided arguments
    except Exception as exception:
        # add the stack trace to the log
        import traceback
        traceback.print_exc() 
        print("An error occurred: %s" % str(exception)) 
