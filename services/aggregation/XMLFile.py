import xml.etree.ElementTree as ET

class XMLFile:

    def __init__(self, fromstring=True, string=None, path=None):
        if fromstring:
            self.content = self.fromString(string)
        else:
            self.content = self.fromPath(path)
    
    def fromString(self, string):
        return ET.fromstring(string)
    
    def fromPath(self, path):
        return ET.parse(path).getroot()