import time
import zlib
import struct
import random

class Canvas():
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
        self.data = [[[0, 0, 0] for _ in range(self.width)] for _ in range(self.height)]

    def make_RGB_PNG(self):
        def I1(value):
            return struct.pack("!B", value & (2 ** 8 - 1))

        def III(value1, value2, value3):
            return struct.pack("!B B B", value1, value2, value3)

        def III2(value1, value2, value3, value4, value5, value6):
            return struct.pack("!B B B B B B", value1, value2, value3, value4, value5, value6)

        def III3(value1, value2, value3, value4, value5, value6, value7, value8, value9):
            return struct.pack("!B B B B B B B B B", value1, value2, value3, value4, value5, value6, value7, value8, value9)

        def III4(value1, value2, value3, value4, value5, value6, value7, value8, value9, value10, value11, value12):
            return struct.pack("!B B B B B B B B B B B B", value1, value2, value3, value4, value5, value6, value7, value8, value9, value10, value11, value12)

        def III5(value1, value2, value3, value4, value5, value6, value7, value8, value9, value10, value11, value12, value13, value14, value15):
            return struct.pack("!B B B B B B B B B B B B B B B", value1, value2, value3, value4, value5, value6, value7, value8, value9, value10, value11, value12, value13, value14, value15)

        def I4(value):
            return struct.pack("!I", value & (2 ** 32 - 1))

        # compute width&height from data if not explicit
        if self.height is None:
            self.height = len(self.data) # rows

        if self.width is None:
            self.width = 0
            for row in self.data:
                if self.width < len(row):
                    self.width = len(row)

        # generate these chunks depending on image type
        makeIHDR = True
        makeIDAT = True
        makeIEND = True
        png = b"\x89" + "PNG\r\n\x1A\n".encode('ascii')

        if makeIHDR:
            colortype = 2   # 0 = true gray image (no palette) / 2 = RGB / 6 = RGBA
            bitdepth = 8   # with one byte per pixel (0..255)
            compression = 0 # zlib (no choice here)
            filtertype = 0  # adaptive (each scanline seperately)
            interlaced = 0  # no
            IHDR = I4(self.width) + I4(self.height) + I1(bitdepth)
            IHDR += I1(colortype) + I1(compression)
            IHDR += I1(filtertype) + I1(interlaced)
            block = "IHDR".encode('ascii') + IHDR
            png += I4(len(IHDR)) + block + I4(zlib.crc32(block))

        if makeIDAT:
            if self.width % 5 == 0:
                raw = bytearray()
                for y in range(self.height):
                    raw += b"\0"  # no filter for this scanline
                    for x in range(0, self.width, 5):
                        raw += III5(self.data[y][x][0], self.data[y][x][1], self.data[y][x][2],
                                    self.data[y][x + 1][0], self.data[y][x + 1][1], self.data[y][x + 1][2],
                                    self.data[y][x + 2][0], self.data[y][x + 2][1], self.data[y][x + 2][2],
                                    self.data[y][x + 3][0], self.data[y][x + 3][1], self.data[y][x + 3][2],
                                    self.data[y][x + 4][0], self.data[y][x + 4][1], self.data[y][x + 4][2])
            elif self.width % 4 == 0:
                raw = bytearray()
                for y in range(self.height):
                    raw += b"\0"  # no filter for this scanline
                    for x in range(0, self.width, 4):
                        raw += III4(self.data[y][x][0], self.data[y][x][1], self.data[y][x][2],
                                    self.data[y][x + 1][0], self.data[y][x + 1][1], self.data[y][x + 1][2],
                                    self.data[y][x + 2][0], self.data[y][x + 2][1], self.data[y][x + 2][2],
                                    self.data[y][x + 3][0], self.data[y][x + 3][1], self.data[y][x + 3][2])
            elif self.width % 3 == 0:
                raw = bytearray()
                for y in range(self.height):
                    raw += b"\0"  # no filter for this scanline
                    for x in range(0, self.width, 3):
                        raw += III3(self.data[y][x][0], self.data[y][x][1], self.data[y][x][2],
                                    self.data[y][x + 1][0], self.data[y][x + 1][1], self.data[y][x + 1][2],
                                    self.data[y][x + 2][0], self.data[y][x + 2][1], self.data[y][x + 2][2])
            elif self.width % 2 == 0:
                raw = bytearray()
                for y in range(self.height):
                    raw += b"\0"  # no filter for this scanline
                    for x in range(0, self.width, 2):
                        raw += III2(self.data[y][x][0], self.data[y][x][1], self.data[y][x][2],
                                    self.data[y][x + 1][0], self.data[y][x + 1][1], self.data[y][x + 1][2])
            else:
                raw = bytearray()
                for y in range(self.height):
                    raw += b"\0"  # no filter for this scanline
                    for x in range(self.width):
                        raw += III(self.data[y][x][0], self.data[y][x][1], self.data[y][x][2])

            compressor = zlib.compressobj()
            compressed = compressor.compress(raw)
            compressed += compressor.flush() #!!
            block = "IDAT".encode('ascii') + compressed
            png += I4(len(compressed)) + block + I4(zlib.crc32(block))


        if makeIEND:
            block = "IEND".encode('ascii')
            png += I4(0) + block + I4(zlib.crc32(block))

        return png

    def set_pixel(self, x:int, y:int, color):
        if x < 0 or x >= self.width:
            return
        if y < 0 or y >= self.height:
            return
        self.data[y][x] = color

    def save_PNG(self, filename:str):
        png = self.make_RGB_PNG()

        with open(filename, "wb") as f:
            f.write(png)

def main():

    print("Creating")
    width = 800
    height = 600
    canvas = Canvas(width, height)

    print("Drawing")
    for i in range(width):
        for j in range(height):
            canvas.set_pixel(i, j, (random.randint(0, 255), 0, 0))

    print("Saving")
    canvas.save_PNG("test.png")

if __name__ == "__main__":
    main()
