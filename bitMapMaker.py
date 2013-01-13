import os
import sys

FIT_BYTES = False #should we fit the number of bytes in input to a fixed size?
OUTPUT_FILE_NAME = 'outputBmp.bmp'

if len(sys.argv) == 1:#were there command line arguements?
    import Tkinter, tkFileDialog, tkMessageBox
    root = Tkinter.Tk()
    root.wm_withdraw()
    FILE_TO_ANALYSE = tkFileDialog.askopenfilename(parent=root, 
            title='Choose a file')
    #TODO check for file.
    result = tkMessageBox.askquestion("Scaling", 
            "Scale input bytes to fit 1024x768?", icon='question')
    if result == 'yes':
        FIT_BYTES = True
    myFormats = [
    ('Windows Bitmap','*.bmp'),
    ]
    OUTPUT_FILE_NAME = tkFileDialog.asksaveasfilename(parent=root, 
            filetypes=myFormats, title="Save the image as...", 
            initialfile= FILE_TO_ANALYSE+'.bmp' )

else:
    FILE_TO_ANALYSE = sys.argv[1]
    if 'True' in sys.argv[2]:
        FIT_BYTES = True 
    OUTPUT_FILE_NAME = sys.argv[3]
print "Analysing", FILE_TO_ANALYSE

#TODO flags for specifying the file.
sizeOfFile = os.path.getsize(FILE_TO_ANALYSE)

WIDTH = 1024
if FIT_BYTES: #we want pixels to be expanded
    HEIGHT = 768
else: #we can have small/large images because we wont scale to a standard size
    HEIGHT = int(round(float(sizeOfFile)/float(WIDTH)))
NUMBER_OF_PIXELS = (WIDTH*HEIGHT)

bytesReadFromFile = 1
def yieldByte():
    global bytesReadFromFile
    with open(FILE_TO_ANALYSE, "rb") as f:
        byte = f.read(1)
        while byte != "":
            # Do stuff with byte.
            yield int(ord(byte))
            byte = f.read(1)
            bytesReadFromFile += 1
    print "Run out of bytes, returning -1"
    while True:
        yield -1

def gimmeMappedBytes():
    """Works out how many pixels a byte should be worth and yields bytes"""
    pixelsPerByte = 1
    if FIT_BYTES: #integer rounding ok -> we then end up with space left at end
        pixelsPerByte = (NUMBER_OF_PIXELS) / (sizeOfFile)
    if pixelsPerByte == 0: #more bytes than pixels
        #We have to average out some of the pixels 
        howManyTimesLarger = sizeOfFile//NUMBER_OF_PIXELS
        remainderBytes = (sizeOfFile % NUMBER_OF_PIXELS)
        print "Bytes:", howManyTimesLarger, "times larger than number of pixels"
        print "Bytes left over:", remainderBytes

        if howManyTimesLarger > 1: #every pixel must be averaged at least once
            bytesBeforeAverage = (sizeOfFile / remainderBytes) -1
            print "Average:",howManyTimesLarger, "pixels together"
            gener = yieldByte()
            try:
                while True:
                    byte = gener.next()
                    #Every byte must be averaged a few times:
                    for x in xrange(howManyTimesLarger):
                        byte += gener.next()
                    byte = byte/(howManyTimesLarger+1)
                    yield byte
                pass
            except:
                pass
        else: # less than twice as big, every now and again we average
            bytesBeforeAverage = (sizeOfFile / remainderBytes) -1
            print "Average pixels every: ", bytesBeforeAverage, "bytes"
            #print "Average:", howManyTimesLarger, "pixels together"
            gener = yieldByte()
            try:
                numBytes = 1 
                while True:
                    byte = gener.next()
                    #At a certain point we must average the byte with next one 
                    #so that we fit all the bytes in.
                    if ((numBytes % bytesBeforeAverage) == 0): 
                        byte += gener.next()
                        byte /= 2
                    yield byte
                    numBytes += 1
                pass
            except Exception as e:
                print e
                pass

    else: #fewer bytes than pixels, re use some of the bytes:
        print "Pixels per byte:", pixelsPerByte
        for byte in yieldByte():
            timesUsed = 0
            while timesUsed < pixelsPerByte:
                timesUsed +=1
                yield byte

#Some key imports.
#Struct is used to create the actual bytes.
#It is super handy for this type of thing.
import struct, random

#Function to write a bmp file.  It takes a dictionary (d) of
#header values and the pixel data (bytes) and writes them
#to a file.  This function is called at the bottom of the code.
def bmp_write(d, the_bytes):
    mn1 = struct.pack('<B',d['mn1'])
    mn2 = struct.pack('<B',d['mn2'])
    filesize = struct.pack('<L',d['filesize'])
    undef1 = struct.pack('<H',d['undef1'])
    undef2 = struct.pack('<H',d['undef2'])
    offset = struct.pack('<L',d['offset'])
    headerlength = struct.pack('<L',d['headerlength'])
    width = struct.pack('<L',d['width'])
    height = struct.pack('<L',d['height'])
    colorplanes = struct.pack('<H',d['colorplanes'])
    colordepth = struct.pack('<H',d['colordepth'])
    compression = struct.pack('<L',d['compression'])
    imagesize = struct.pack('<L',d['imagesize'])
    res_hor = struct.pack('<L',d['res_hor'])
    res_vert = struct.pack('<L',d['res_vert'])
    palette = struct.pack('<L',d['palette'])
    importantcolors = struct.pack('<L',d['importantcolors'])
    #Create the outfile
    outfile = open(OUTPUT_FILE_NAME,'wb')
    #Write the header + the_bytes
    outfile.write(mn1+mn2+filesize+undef1+undef2+offset+headerlength+width+
            height+colorplanes+colordepth+compression+imagesize+res_hor+
            res_vert+palette+importantcolors+the_bytes)
    outfile.close()

###################################    
# http://pseentertainmentcorp.com/smf/index.php?topic=2034.0
def main():
    global num
    #Here is a minimal dictionary with header values.
    #Of importance is the offset, headerlength, width,
    #height and colordepth.
    #Edit the width and height to your liking.
    #These header values are described in the bmp format spec.
    #You can find it on the internet. This is for a Windows
    #Version 3 DIB header.
    d = {
        'mn1':66,
        'mn2':77,
        'filesize':0,
        'undef1':0,
        'undef2':0,
        'offset':54,
        'headerlength':40,
        'width': WIDTH,
        'height': HEIGHT,
        'colorplanes':0,
        'colordepth':24,
        'compression':0,
        'imagesize':0,
        'res_hor':0,
        'res_vert':0,
        'palette':0,
        'importantcolors':0
        }

    #Function to generate a random number between 0 and 255
    def rand_color():
        x = random.randint(0,255)
        return x

    #Build the byte array.  This code takes the height
    #and width values from the dictionary above and
    #generates the pixels row by row.  The row_mod and padding
    #stuff is necessary to ensure that the byte count for each
    #row is divisible by 4.  This is part of the specification.
    the_bytes = ''
    gener = gimmeMappedBytes()
    #(BMPs are L to R from the bottom L row)
    for row in range(d['height']-1,-1,-1):
        for column in range(d['width']):
            b = gener.next()
            g = b
            r = b
            if (b == -1): # if there are no more bytes
                b = 255
                g = 0
                r = 0
            pixel = struct.pack('<BBB',b,g,r)
            the_bytes = the_bytes + pixel
        row_mod = (d['width']*d['colordepth']/8) % 4
        if row_mod == 0:
            padding = 0
        else:
            padding = (4 - row_mod)
        padbytes = ''
        for i in range(padding):
            x = struct.pack('<B',0)
            padbytes = padbytes + x
        the_bytes = the_bytes + padbytes

    #Call the bmp_write function with the
    #dictionary of header values and the
    #bytes created above.
    bmp_write(d,the_bytes)

if __name__ == '__main__':
    main()
    print "Bytes in File:", sizeOfFile, "Pixels:", NUMBER_OF_PIXELS, \
            "Bytes used:", bytesReadFromFile

