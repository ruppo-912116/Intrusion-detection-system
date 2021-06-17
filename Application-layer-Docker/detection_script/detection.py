import sys
import json
import re
import time
import smtplib
from datetime import datetime
from Mailing import sendingMail

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


# sys.argv[1] defines the file to be monitored
# sys.argv[2] defines the sender's gmail 
# sys.argv[3] defines the app-specific password of the sender's gmail account

sender_email = sys.argv[2]
rec_email = "rupanchaulagain.rc@gmail.com"

password = sys.argv[3]




# result and result1 are dictionaries storing info from two regex patterns
# last_result to combine those two dictionaries
# adding only the relevant information for the client
result = {}
result1 = {}
last_result= {}
prevMsgTime = datetime(2020,1, 1, 1, 1, 1, 1)

# first pattern regex extractions
main_info = ["Date","Time","msg","hostname"]
# second pattern regex extractions
main_info1 = ["client","request","server"]

# for reading files
old_line = 0 # the variable stores the length of the unmodified text document
new_line = 0 # the variable stores the length of the modified text document


# event handling functions
def on_created(event):
    print("created")

def on_deleted(event):
    print("deleted")

def on_modified(event):
    readingFiles()

def on_moved(event):
    print("moved")

# this function returns the total lines in the file
def file_len():
    with open(sys.argv[1]) as fptr:
        for i,l in enumerate(fptr):
            pass
    return i+1
    
# firstly, the file is opened
# then checks whether the new_line matches the old_line, if not, this means the file is modified
# then all the lines of the file is read and stored in a list named all_lines
# then loop is implemented from the old_line to the new_line which basically checks the new_line added 
# checking the error logs and extracting information inside the square brackets
# the informations are stored in dictionary named result

def readingFiles():
    global old_line
    global new_line
    global result
    global last_result
    global prevMsgTime


    with open(sys.argv[1]) as f:
        new_line = file_len()

        if(new_line != old_line):
            all_lines = f.readlines()
            for i in range(old_line,new_line):
                if "[error]" in all_lines[i]:
                    r = re.compile("""\[(?P<key>[^\]\[\s]+)(?:\s+"(?P<value>[^"]+)")?\]""")
                    r1 = re.compile("""(?P<key>[a-zA-Z]+)(:\s+(?P<value>[^,]+))""")

                    result = {m.group('key'): m.group('value') for m in r.finditer(all_lines[i])}
                    result1 = {m.group('key'): m.group('value') for m in r1.finditer(all_lines[i])}

                    result['Date'] = all_lines[i][0:10]
                    result['Time'] = all_lines[i][11:19]

                    last_result = {my_key:result[my_key] for my_key in main_info}
                    for k in main_info1:
                        last_result[k] = result1[k]

                    currentTime = datetime.utcnow()
                    timeInMinutes = abs(currentTime - prevMsgTime).total_seconds()/60.0

                    if (timeInMinutes >= 25.0):
                        prevMsgTime = datetime.utcnow()
                        sendingMail(sender_email, rec_email,password,last_result)
                        
            old_line = new_line  

    return

        



    
if __name__ == "__main__":
    old_line = file_len()

    # adding event handler for checking the file system
    patterns = "*/error.log" # monitoring only the Error text document
    ignore_patterns = None
    ignore_directories = True
    case_sensitive = False
    my_event_handler = PatternMatchingEventHandler(patterns,ignore_patterns,ignore_directories,case_sensitive)
    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved


    # we need another object known as the observer
    # that will monitor our filesystem looking for changes
    # that will be handled by the event handler
    path = "."
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler,path,recursive=go_recursively)
    my_observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()

    


