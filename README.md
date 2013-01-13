Bytes-To-Bitmap
===============

Visualise the bytes of any file as a bitmap. Useful for visually inspecting for
corrupt files.

# Why?

Sometime files may be corrupt, containing large runs of _0'd_ bytes. 
Maybe you do not know whether files are corrupt, and would like to be able to
quickly inspect the files for said corrupt blocks.

Maybe you just want to view your PhD thesis as raw bytes?

Reference bitmap header implementation code found at:
<http://pseentertainmentcorp.com/smf/index.php?topic=2034.0>

* No external libraries, pure python 2.7 <http://www.python.org/getit/> _Please don't use Python 3._

## Usage

Assuming that Python is correctly installed, you can simply click on the python 
file. A dialogue should pop up asking you to select a file to process.

If you prefer to run in a Terminal so that you can use the script to process a 
large number of files, run the script like this:
```bash
python bitMapMaker.py Desert.jpg True outPutFile.bmp
```

The second argument indicates whether the image should be scaled to 1024*768. 
If the user does not provide arguments then the gui will prompt the user for 
file selection.

A corrupt jpg is included for demonstration purposes.
