import sys
import time
from watchdog.observers import Observer
from libs.file_monitor import FileMonitor
from libs.compiler_manager import CompilerManager
from libs.logger import setup_logger

def main(filename, interval):
    logger = setup_logger()

    compiler_manager = CompilerManager()
    file_extension = compiler_manager.get_extension(filename)
    compiler = compiler_manager.get_compiler(file_extension)

    if not compiler:
        logger.error("Compiler not found for file extension: %s", file_extension)
        return

    logger.info("Using compiler: %s", compiler)
    event_handler = FileMonitor(filename, compiler)
    logger.info("Watching file: %s", filename)
    
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    logger.info("Started watching file: %s", filename)

    try:
        while True:
            time.sleep(interval)
    except KeyboardInterrupt:
        observer.stop()
    except Exception as e:
        logger.error("An error occurred: %s", str(e))
    finally:
        observer.join()

if __name__ == "__main__":
    try:
        if len(sys.argv) != 3:
            print("Usage: live_coding_editor.py <filename> <time_interval>")
            sys.exit(1)

        filename = sys.argv[1]
        interval = int(sys.argv[2])
        main(filename, interval)
    except Exception as exception:
        # add the stack trace to the log
        import traceback
        traceback.print_exc()
        print("An error occurred: %s" % str(exception))
