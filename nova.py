import client
import time
import sys
import win32com.client
import winsound

from Tkinter import Tk
from tkFileDialog import askopenfilename

# uncomment line 14 and comment line 13 to do actual alignment of our celestron Telescope
# replace the line 29 api key to your account if you want to

tel = win32com.client.Dispatch("ASCOM.Simulator.Telescope")
#tel = win32com.client.Dispatch("ASCOM.Celestron.Telescope")
tel.Connected = True


Tk().withdraw()                 # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename()    # show an "Open" dialog box and return the path to the selected file

nova = client.Client()          # Rename 'client.Client()' class to make code clutter free

approx_ra = tel.RightAscension  # The current approximate Right Ascension of centre of telescope
approx_dec = tel.Declination    # The current approximate Declination of centre of telescope


# Attempt login using the api key for 5 times
# If login fails consecutively for fifth time, exit with an error message
print("Logging in...")
for i in xrange(5):
    log_result = nova.login("kmhjxpnvsmeycapf")     # Login using api key
    if log_result["status"] == "success":           # If login succeeds, continue to obtaining session_id
        break
if (i == 5):
    print("Login failed.\n")                        # Login failed consecutively for five times.
    tel.Connected = False
    sys.exit()
else:
    session_id = log_result["session"]              # Session id for current login session
    print("Login succeeded.")
    print("Session ID: %s\n" %(session_id, ))


# Obtain all the previous job ids. Job ID is assigned to each image uploaded using our api key on nova.astrometry.net
# Job ID of last image uploaded (not the one we will upload now.) is stored in last_job_id.
jobs = nova.myjobs()
last_job_id = jobs[0]

# Attempt uploading image for 5 times.
# If image upload fails consecutively for fifth time, exit with an error message
print("Uploading image...")
for i in xrange(5):
    sub_result = nova.upload(filename)              # Upload image
    if sub_result["status"] == "success":
        break
if (i == 5):
    print("Image upload failed.\n")                 # Image upload failed consecutively for five times.
    tel.Connected = False
    sys.exit()
else:
    subid = sub_result["subid"]
    print("Image upload succeeded.")
    print("Submission ID: %d\n" %(subid, ))         # Submission ID of current image uploadedu

# Once image is uploaded, nova.astrometry.net starts solving it for RA and Dec of its center.
# Once the image is solved (or failed to solve), the image gets a specific Job ID different from Job IDs of all previous images.
# Since solving image takes time, we check after every 5 seconds if a new Job ID has been updated in the list.
print("Solving image...")
while (jobs[0] == last_job_id):                     # Check if last Job ID is different from that of previous image uploaded
    time.sleep(5)
    jobs = nova.myjobs()

job_id = str(jobs[0])                               # Job ID of current image
job_result = nova.job_status(job_id)                # Job status: success or failure

if (job_result["status"] == "failure"):             # If image is failed to solve, exit with error message
    print("Solving image failed.\n")
    tel.Connected = False
    sys.exit()
elif (job_result["status"] == "success"):           # If image is solved, print relevant info about image.
    print("Image solved for RA and Dec.\n")
    print ("RA = %f, Dec = %f" %(job_result["calibration"]["ra"], job_result["calibration"]["dec"]))
    
    print("Objects in field: ")
    no_of_objects = len(job_result["objects_in_field"])
    for i in xrange(no_of_objects):
        print ("%d. %s" %(i+1, job_result["objects_in_field"][i])) 


tel.SyncToCoordinates(job_result["calibration"]["ra"]/15.0,job_result["calibration"]["dec"])   # Calibrate the telescope directly using the RA and Dec received.

Freq = 500                          # Set Frequency To 500 Hertz
Dur = 1000                          # Set Duration To 1000 ms == 1 second
winsound.Beep(Freq,Dur)             # Beeping sound indicates roughly the duration while telescope is repositioning itself.


tel.Connected = False               # Disconnect the telescope
