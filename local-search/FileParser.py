class FileParser():
    def __init__(self, path):
        self.path = path
        
    def file_format(self):
        return self.path.split('.')[-1]
    
    def valid_file_format(self):
        return self.file_format() in ['txt']

    def parse(self):
        if not self.valid_file_format():
            return None
        with open(self.path, 'r') as file:
            content = file.read()
            return content
        return None