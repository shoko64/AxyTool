import struct

class axybmp:

    def __init__(self, totalSize=None, name=None, width=None, height=None, data=None, bmpSize=None, bmpFile=None):

        if bmpFile == None: # Constructing from raw data
            self.totalSize = totalSize
            self.name = name
            self.width = width
            self.height = height
            self.data = data
            self.size = bmpSize
            self.file = self.constructFile()
        else: # Constructing from an existing BMP file
            self.totalSize = len(bmpFile.data) + 0x10 # 0x10 = the header size
            self.name = name
            self.width = bmpFile.width
            self.height = bmpFile.height
            self.data = bmpFile.data
            self.size = len(bmpFile.data)
            self.file = self.constructFile()


    def constructFile(self):
        
        # Building up the raw BMP file and returns it

        print("Importing: " + self.name)
        file = bytearray()
        file.extend(self.totalSize.to_bytes(4, byteorder="little"))
        file.extend(str.encode(self.name))
        file.extend(self.width.to_bytes(4, byteorder="little"))
        file.extend(self.height.to_bytes(4, byteorder="little"))
        file.extend(self.data)
        return file