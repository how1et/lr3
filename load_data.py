import json

# взятие данных их data.json
class DataLoader:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data = None

    def load(self) -> dict:
        with open(self.filepath, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        return self.data