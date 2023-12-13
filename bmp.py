import struct
import mmap

# BMP structure
bmpHeader = "<2sIHHIIIIHHIIIIII4s4s4s4s68x"

sig = b'BM'

reserved1 = 0
reserved2 = 0

colorPaneNum = 1
bits = 16
compression = 3

printResolution1 = 0x2E23
printResolution2 = 0x2E23
colorUsed = 0
importantColors = 0
redChannelBitMask = b'\x00\xF8\x00\x00'
greenChannelBitMask = b'\xE0\x07\x00\x00'
blueChannelBitMask = b'\x1F\x00\x00\x00'
alphaChannelBitMask = b'\x00\x00\x00\x00'

class bmp:

    def __init__(self, rawDataSize=None, width=None, height=None, data=None, file=None):
        headerSize = 0x8A # Header size should always be 0x8A
        if file == None: # If the object is being constructed with raw data
            self.width = width
            self.height = height
            self.data = data

            headerTotalSize = headerSize + rawDataSize
            fileSize = headerTotalSize
            dataOffset = headerSize
            dibSize = headerSize - 0xE

            header = struct.pack(bmpHeader,
                                sig, 
                                fileSize, 
                                reserved1, 
                                reserved2, 
                                dataOffset,
                                dibSize,
                                width,
                                height,
                                colorPaneNum,
                                bits,
                                compression,
                                rawDataSize,
                                printResolution1,
                                printResolution2,
                                colorUsed,
                                importantColors,
                                redChannelBitMask,
                                greenChannelBitMask,
                                blueChannelBitMask,
                                alphaChannelBitMask,
                                )
        
            self.file = header + data
        else: # If the object is being constructed with a bmp file
            try:
                unpacked = struct.unpack(bmpHeader, file.read(headerSize))

                # Checking if the header size is correct
                if unpacked[4] != headerSize:
                    print("WARNING: Wrong BMP header, please make sure that you have exported it correctly")
                    sys.exit()
                
                # Checking if the file is 16 bit
                if unpacked[9] != 16:
                    print("WARNING: The image that you are trying to import is not formatted as a 16 bit BMP file, please export it with the correct format.")
                    sys.exit()

                self.file = file
                self.width = unpacked[6]
                self.height = unpacked[7]
                rawDataSize = unpacked[11]
                dataOffset = unpacked[4]
                fileSize = unpacked[1]
                self.data = self.__readRange(file, dataOffset, fileSize)
            except:
                print("Invalid BMP file")
                sys.exit()


    def __readRange(self, file, start, end):

        # Reading data from specified offset range

        with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
            mmapped_file.seek(start)
            data = mmapped_file.read(end - start)
        return data