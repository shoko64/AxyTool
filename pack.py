import struct
import mmap

from axybmp import axybmp

class pack:

    size = 0 # Size of the file
    file = None # The actual file
    entries = [] # All of the BMP entries

    def __init__(self, file, size):
        self.reset()
        self.file = file 
        self.size = size 
        self.parseFile()


    def reset(self):
        self.size = 0 
        self.file = None 
        self.entries.clear()


    def parseFile(self):

        # Parsing the actual file

        index = 0 # Index
        dataOffset = 0x10 # Where the data actually starts
        totalSize = 0 # Total size of header + data  
        name = "" # BMP Name
        width = 0 # BMP Width
        height = 0 # BMP Height
        data = None # Raw BMP data
        bmpSize = None # Raw BMP data total size

        while (index + 0x10 < self.size): # Loop until file size is reached
            totalSize = struct.unpack('<i', self.__readRange(index, index + 0x04))[0] # Gets the totalSize
            name = bytes.decode(struct.unpack('4s', self.__readRange(index + 0x04, index + 0x08))[0]) # Gets the name
            width = struct.unpack('<i', self.__readRange(index + 0x08, index + 0x0C))[0] # Gets the width
            height = struct.unpack('<i', self.__readRange(index + 0x0C, index + 0x10))[0] # Gets the height
            
            bmpSize = width*height*2 # Gets the raw BMP size
            
            data = self.__readRange(index + dataOffset, index + bmpSize + dataOffset) # Gets the raw BMP data

            index += totalSize  # Incrementing the index

            self.entries.append(axybmp(totalSize=totalSize, name=name, width=width, height=height, data=data, bmpSize=bmpSize)) # Pushes the data to the entries list


    def constructFile(self):

        # Adding up all of the BMP's in the entries list and returns it to construct a pack file

        constructed = b''
        for x in self.entries:
            constructed += x.file
        return constructed


    def __readRange(self, start, end):

        # Reading data from specified offset range

        with mmap.mmap(self.file.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
            mmapped_file.seek(start)
            data = mmapped_file.read(end - start)
        return data