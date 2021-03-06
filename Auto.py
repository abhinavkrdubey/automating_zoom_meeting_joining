import  datetime, time, subprocess, csv, os, webbrowser

try:
    import pyautogui
    import openpyxl
    from PIL import Image
except ModuleNotFoundError as err:
    print("not installed modules please go through the read me files, press anything to exit")
    input()
#enabling mouse fail safe
pyautogui.FAILSAFE = True

#copying data from excel sheet to the program
meetings = []
wb = openpyxl.load_workbook('List.xlsx')
sheet = wb['Sheet1']

for i in sheet.iter_rows(values_only = True):
    if i[0] != None:   
        meetings.append(i)
meetings.pop(0)
meetings.sort()


#function to manualy join if no link is provided
def manualjoin(id, password = ""):
    
    time.sleep(3)

    #locating the zoom app
    while True:
        var = pyautogui.locateOnScreen('joining.png', confidence=0.9)
        if var != None:
            pyautogui.click(var)
            break
        elif (time.time() - cur) >= 120:
            print("App Not opened")
            break
        #check every 30 secs
        time.sleep(30)

    time.sleep(3)

    #entering the meeting id
    pyautogui.typewrite(id)

    #disabling video source
    var = pyautogui.locateOnScreen('videooff.png', confidence=0.9)
    pyautogui.click(var)

    #clicking the join button
    var = pyautogui.locateOnScreen('joins.png', confidence=0.9)
    pyautogui.click(var)

    time.sleep(3)

    #checking and entering if meeting password is enabled
    if pyautogui.locateOnScreen('password.png', confidence=0.9) != None :
        pyautogui.typewrite(password)
        var = pyautogui.locateOnScreen('joinmeeting.png', confidence=0.9)
        pyautogui.click(var)

    return



def linkjoin(link):
    #open the given link in web browser
    webbrowser.open(link)
    start = time.time()
    time.sleep(3)
    while True:
        var = pyautogui.locateOnScreen('openlink.png', confidence=0.9)
        if var != None:
            pyautogui.click(var)
            break
        var = pyautogui.locateOnScreen('openzoom.png', confidence=0.9)
        if var != None:
            pyautogui.click(var)
            break
        var = pyautogui.locateOnScreen('open.png', confidence=0.9)
        if var != None:
            pyautogui.click(var)
            break
        elif (time.time() - start) >= 120:
            print("link " + link + " not opened")
            break
        var = pyautogui.locateOnScreen('signin.png', confidence=0.9)
        pyautogui.click(var)
        time.sleep(3)
    return


#Iterating through the meeting list to jointate the specified time
for i in range(len(meetings)):
    curmeeting = meetings[i]

    #Setting the meeting Times
    cur = round(time.time(), 0)
    temp = curmeeting[0].timestamp()

    #join a minute early for later scheduled class
    if(cur < temp - 60):
        print("next class in ", end ="")
        print(datetime.timedelta(seconds = (temp - cur) - 60))
        time.sleep(temp - cur - 60)
    #if more than 5 minutes have passed already
    elif (cur - temp) > 300:
        print("skipped meeting " + str(i + 1))
        continue
        
    var = os.system("taskkill /f /im Zoom.exe")
    
    
    #check if link is provided
    if curmeeting[1] != None:
        linkjoin(str(curmeeting[1]))
    #check if 
    if curmeeting[2] != None:
        subfolders = [ f.path for f in os.scandir("C:\\Users") if f.is_dir() ]
        #opening the zoom app, if you are running on a different OS or the path is different
        #change the path here 
        for i in subfolders:
            if os.path.isfile(i + "\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe"):
                subprocess.Popen(i + "\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe")  
        manualjoin(str(curmeeting[2]), str(curmeeting[3]))
    
    else:
        print("data insufficient, press anything to exit")
        input()
        exit()

    time.sleep(5)
    #check whether the class has started and enabling audio
    while True:
        if pyautogui.locateOnScreen('audioenable.png', confidence=0.9) != None :
            var = pyautogui.locateOnScreen('audioenable.png', confidence=0.9)
            pyautogui.click(var)
            break
        elif pyautogui.locateOnScreen('leave.png', confidence=0.9) != None :
            var = pyautogui.locateOnScreen('leave.png', confidence=0.9)
            pyautogui.click(var)
            break
        elif (time.time() - cur) >= 30 * 60:
            os.system("taskkill /f /im Zoom.exe")
            break
        time.sleep(5)

    #check whether the mic is muted, if not muted
    pyautogui.moveTo(x = 900, y = 900, duration = 0.25)
    if pyautogui.locateOnScreen('mute.png', confidence=0.9) != None :
        var = pyautogui.locateOnScreen('mute.png', confidence=0.9)
        pyautogui.click(var)


#program has finished all classes and exits
print("Done, press anything to exit")
input()
var = os.system("taskkill /f /im Zoom.exe")
