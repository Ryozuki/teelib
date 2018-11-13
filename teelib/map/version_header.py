class VersionHeader:
    def __init__(self, magic: str, version: int):
        self.magic = magic
        self.version = version

    def __str__(self):
        return str(self.version)

    def is_valid(self):
        return self.magic == "DATA" or self.magic == "ATAD"
