import os

class DirectorySynchronizer:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def create_file(self, file_path, content):
        try:
            with open(file_path, 'w') as file:
                file.write(content)
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def create_directory(self, dir_path):
        try:
            os.makedirs(dir_path, exist_ok=True)
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def synchronize(self, data: dict, current_path=None):
        if current_path is None:
            current_path = self.folder_path

        # Check if directory exists and create it if it doesn't
        if not os.path.exists(current_path):
            os.makedirs(current_path)

        for name, info in data.items():
            if info["type"] == "directory":
                dir_path = os.path.join(current_path, name)
                self.create_directory(dir_path)
                if 'content' in info:
                    self.synchronize(info['content'], dir_path)
            elif info["type"] == "file":
                file_path = os.path.join(current_path, name)
                self.create_file(file_path, info.get("content", ""))