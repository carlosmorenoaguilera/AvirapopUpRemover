import sys
import pywinauto
from pywinauto import Desktop, Application
import time
import os
import pythoncom
from threading import *
import time
import wmi
import keyboard



"""Name	PID	Status	User name	CPU	Memory (active private working set)	Architecture	Description
Avira.Spotlight.UI.Application.exe	13192	Running	Carlos Moreno	00 	69,136 K	x86	Avira Security
"""
def closeAvira():
    try:
        app = Application(backend="uia").connect(path="Avira.Spotlight.UI.Application.exe")
        print("conected to avira")
        print(app.windows())
        
        if app.window(title = "Avira Security"):
            Desktop(backend="uia").window(title="Avira Security").close()
            print("Dispachet")

        # dlg = app["Avira Security"]
        # print(dlg.print_control_identifiers()) #btnWindowClose or btnOverLayClose
        # window = dlg.window(auto_id="AppWindow")
        # window.click(auto_id="btnWindowClose")
    except pywinauto.application.ProcessNotFoundError:
        print("Process not found")


def listener():
    pythoncom.CoInitialize()
    print(pythoncom)
    c = wmi.WMI()
    print(c)
    process_watcher = c.Win32_Process.watch_for("creation")
    while True:
        new_process = process_watcher()
        print(new_process)
        if new_process.Caption == "Avira.Spotlight.UI.Application.exe":
            print("send to close")
            time.sleep(3)
            closeAvira()
 

def keyboardShortcut():
    while True:
        if keyboard.is_pressed("q"):
            print("ending program")
            sys.exit()
            

if __name__ == '__main__':    
    t = Thread(target=listener)
    keyboardWatcher = Thread(target=keyboardShortcut)
    # t.setDaemon(True)
    t.daemon = True
    keyboardWatcher.start()
    t.start()
