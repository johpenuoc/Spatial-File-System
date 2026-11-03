import os

class FileSys:
    def __init__(self, drive):
        self.base = drive

        self.prev = drive
        self.curr = None
        self.tree = {}

    def search(self, folder):
        contents = os.listdir(folder)

        self.tree[folder] = contents

        keys = list(self.tree.keys())
        self.prev = self.tree[keys[len(keys) - 1 - 1]]

        self.curr = folder

        return contents

    def retreat(self):
        del self.tree[-1]

        self.curr = self.prev
        try:
            keys = list(self.tree.keys())
            self.prev = self.tree[keys[len(keys) - 1 - 1]]
        except:
            self.curr = None
            self.prev = self.base