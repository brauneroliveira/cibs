from XMLFile import XMLFile

class HospitalBed:

    def __init__(self, xmlfile):

        headernode = list(xmlfile.content.find('header'))
        self.header = {}
        for el in headernode:
            self.header[el.tag] = el.text
        self.id = xmlfile.content.attrib['id']
        self.area = xmlfile.content.find('area').text
        self.type = xmlfile.content.find('tipo').text
        self.status = xmlfile.content.find('estado').text

    def getHeader(self):
        return self.header

    def getHeaderField(self, field):
        return self.header[field]
    
    def getId(self):
        return self.id
    
    def setId(self, identifier):
        self.id = identifier
    
    def getArea(self):
        return self.area
    
    def getType(self):
        return self.type
    
    def getStatus(self):
        return self.status