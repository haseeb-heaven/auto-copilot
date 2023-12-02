import json
import os
import platform

class KeybindingsParser:
    def __init__(self):
        self.os_name = platform.system()
        self.keybindings_path = self._get_keybindings_path()
        self.keybindings = []
        self.parsed_keybindings = []
        
    def _get_keybindings_path(self):
        # Set the path to the keybindings.json file based on the operating system
        if self.os_name == "Windows":
            keybindings_path = os.path.expanduser("%APPDATA%\\Code\\User\\keybindings.json")
        elif self.os_name == "Darwin":
            keybindings_path = os.path.expanduser("~/Library/Application Support/Code/User/keybindings.json")
        else:  # Linux and other Unix-like systems
            keybindings_path = os.path.expanduser("~/.config/Code/User/keybindings.json")
        return keybindings_path
    
    def parse_keybindings(self):
        for keybinding in self.keybindings:
            parsed_keybinding = {
                'key': keybinding.get('key'),
                'command': keybinding.get('command'),
                'when': keybinding.get('when')
            }
            self.parsed_keybindings.append(parsed_keybinding)

    def find_key_for_command(self, command):
        for keybinding in self.parsed_keybindings:
            if command in keybinding['command']:
                return keybinding['key']
        return None

    def load_keybindings(self):
        try:
            with open(self.keybindings_path, 'r') as file:
                self.keybindings = json.load(file)
        except FileNotFoundError:
            print("Error: keybindings.json file not found.")
            return
        except json.JSONDecodeError:
            print("Error: Unable to parse keybindings.json file.")
            return

        self.parse_keybindings()

def main():
    # Initialize the parser
    parser = KeybindingsParser()
    parser.load_keybindings()

    # List of commands
    commands = ["inlineChat.start","interactive.acceptChanges"]
    keys = []
    
    # Find the key for each command
    for command in commands:
        key = parser.find_key_for_command(command)
        if key is not None:
            parts = key.split('+')
            keys.append(parts)
        else:
            print(f"No key found for the command '{command}'")

    return keys

if __name__ == "__main__":
    keys = main()
    print(keys)