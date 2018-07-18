Astrometry deals with position and motion of heavenly bodies. Astrometry is a tool used to calibrate astronomical images by matching the star patterns in the image with known patterns in a standard database.

Here, we have used services of <a href="nova.astrometry.net">nova.astrometry.net</a> to calibrate our images. We have two python files for this purpose. The nova.py is the main code file authored by me, while client.py is an API client code file obtained from nova.astrometry.net. However, I have made slight changes to the original API client code. The original file can be found here:  https://github.com/dstndstn/astrometry.net/blob/master/net/client/client.py.

Changes that I have made in original client.py file include removing uncessary print statements, returning certain variable from functions I wanted to use in nova.py, and adding a while loop in the function job_status, so that the function returns only after the image has been solved for.

The code will require two softwares to run: Python 2 and ASCOM Platform. ASCOM (Astronomy Common Object Model) is a compatibility platform between astronomical softwares and astronomical tools. You can download ASCOM from here: http://ascom-standards.org/index.htm. Since ASCOM provides platform only for Windows, the code will run only on Windows. In order to run the code on other OS, just comment out any line containing the word 'tel' or using a python library made for Windows (like winsound, win32.client).

To use the code, first download a good image of any part of the sky. Then run the nova.py file. It will ask you to select the image file (from an 'Open' dialog box) you want to solve for RA and Dec. After selecting the image, wait for two to three minutes until RA and Dec are printed.
