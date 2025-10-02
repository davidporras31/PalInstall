from abc import ABC, abstractmethod
import zipfile
import rarfile
import py7zr

def makeArchive(path: str):
    if zipfile.is_zipfile(path):
        return ZipArchiver(path)
    elif rarfile.is_rarfile(path):
        return RarArchiver(path)
    elif py7zr.is_7zfile(path):
        return SevenZArchiver(path)
    
    # Add other archive types here if needed
    raise ValueError("Unsupported archive format")

class Archiver(ABC):
    def __init__(self, path: str):
        self.path = path

    @abstractmethod
    def namelist(self):
        pass

    @abstractmethod
    def extract(self, path: str):
        pass

class ZipArchiver(Archiver):
    def __init__(self, path: str):
        super().__init__(path)
        self.archive = zipfile.ZipFile(path, 'r')

    def namelist(self):
        return self.archive.namelist()
    
    def extract(self, member: str, path: str):
        self.archive.extract(member, path)
    
class RarArchiver(Archiver):
    def __init__(self, path: str):
        super().__init__(path)
        self.archive = rarfile.RarFile(path, 'r')

    def namelist(self):
        return self.archive.namelist()
    def extract(self, member: str, path: str):
        self.archive.extract(member, path)

class SevenZArchiver(Archiver):
    def __init__(self, path: str):
        super().__init__(path)
        self.archive = py7zr.SevenZipFile(path, 'r')

    def namelist(self):
        return self.archive.getnames()
    def extract(self, member: str, path: str):
        self.archive.extract(targets=[member], path=path)