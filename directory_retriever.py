import os

class DirectoryRetriever:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def get_file_info(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return {
                "type": "file",
                "content": content
            }
        except UnicodeDecodeError:
            # If UTF-8 fails, try reading as binary
            try:
                with open(file_path, 'rb') as file:
                    content = file.read()
                return {
                    "type": "file",
                    "content": content.hex(),  # Represent binary content as hex
                    "encoding": "binary"
                }
            except Exception as e:
                return {
                    "type": "file",
                    "error": str(e)
                }
        except Exception as e:
            return {
                "type": "file",
                "error": str(e)
            }

    def get_dir_info(self, dir_path):
        return {
            "type": "directory"
        }

    def retrieve_all(self, current_path=None):
        if current_path is None:
            current_path = self.folder_path

        result = {}
        try:
            with os.scandir(current_path) as it:
                for entry in it:
                    if entry.is_dir():
                        result[entry.name] = self.get_dir_info(entry.path)
                        result[entry.name]['content'] = self.retrieve_all(entry.path)
                    elif entry.is_file():
                        result[entry.name] = self.get_file_info(entry.path)
        except Exception as e:
            result['error'] = str(e)
        
        return result