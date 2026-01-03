from pathlib import Path

class CodeScanner:
    def __init__(self, root_dir: str, ignore_list=None):
        self.root_dir = Path(root_dir)
        self.ignore_list = ignore_list or {'.git', '__pycache__', "node_modules", '.venv', '.pytest_cache', '.codelens_db'}
        
    def get_all_files(self):
        found_files = []
        for file_path in self.root_dir.rglob("*"):
            if any(part in self.ignore_list for part in file_path.parts):
                continue
            if file_path.is_file():
                found_files.append(file_path)
        return found_files