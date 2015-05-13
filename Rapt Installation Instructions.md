# Rapt Installation Instructions
Just installing rapt using "[sudo] pip install rapt" will not be enough to be able to do "import rapt" or "from rapt import *". You need to follow these steps:
1. Edit the file rapt/rapt.py, wherever it is. Normally it's under /usr/local/lib/python2.7/dist-packages/rapt/rapt.py, or with your version of Python as the number. You will have to edit the file as administrator (i.e. "sudo vim" vs "vim")
2. Change the two "from" lines that start with "from rapt.treebird..." to "from .treebrd..."
3. Install the enum package. This is most easily done with "[sudo] pip install enum" but any other way works
