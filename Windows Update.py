from tkinter import *
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import *
import time, random, os, sys
import webbrowser
from win10toast_click import ToastNotifier
from datetime import datetime
from PIL import ImageTk, Image

has_been_clicked = False

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def open():
    def update_status_text():
        return f" Downloading & Installing: {round(pb1_var.get(), 1)}%"

    def update_component():
        if round(pb1_var.get(), 1) <= 30:
            msg = "Downloading an update package"
        elif round(pb1_var.get(), 1)<= 60:
            msg = "Installing the downloaded update package"
        elif round(pb1_var.get(), 1) <= 75:
            msg = "Applying Microsoft Edge updates"
        elif round(pb1_var.get(), 1) < 100:
            msg = "Applying security updates"
        return msg

    def update_progress_bar():
        x = pb1_var.get()
        # Do not check x < 600 (length) because pb1_var is the percentage (0 <= pb1_var <= 100)
        if x < 100:
            pb1_var.set(x+0.1)
            # The larger the variable is, the longer it takes to finish the progress
            ws.after(500, update_progress_bar)
            lbl3['text'] = update_status_text()
            lbl4['text'] = f" Status: {update_component()}"
            btn['state'] = 'disable'
        else:
            showerror("Windows Update Center", f"Exception at 0x0{random.randint(111112, 999998)}\nPlease try to download & install again\nDo not close this window or shutdown your computer")
            # Reset
            pb1_var.set(0)
            lbl3['text'] = ""
            lbl4['text'] = ""
            btn['state'] = 'enable'

    def on_closing():
        webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        showinfo("Windows Update Center", "You can not close this window HAHA\nTHERE IS NO ESCAPE")

    def insert_description():
        current_month = datetime.now().month
        current_year = datetime.now().year
        kb = random.randint(1000001, 9999998)
        string = f"""Critical {current_month}/{current_year} update–KB{kb}
    Highlights
    Updates to improve your PC security against ransomware and PUP.
    • Improvements and fixes
    This security update indudes quality improvements. Key changes indlude:
     - Security updates to Internet Explorer and Microsoft Edge.
     - Security patches against the latest exploits.
     - Small bugfixes.
    If you installed earlier updates, only the new fixes contained in this package will be
    downloaded and installed on your device.
    For more information about the resolved security vulnerabilities, please refer to the
    Security Update Guide."""
        description.insert(1.0, string)

    ws = Tk()
    ws.title('Windows Update Center')
    ws.iconbitmap(os.path.join(resource_path("assets"), "win.ico"))
    ws.protocol("WM_DELETE_WINDOW", on_closing)
    ws.resizable(height = None, width = None)
    ws.attributes('-alpha', 0.85)

    logo_frame = Frame(ws)
    logo_frame.pack()

    microsoft_img = ImageTk.PhotoImage(Image.open(os.path.join(resource_path("assets"), "microsoft.png")).resize((45, 45), Image.ANTIALIAS))
    microsoft_lbl = Label(logo_frame, image = microsoft_img)
    microsoft_lbl.grid(row = 0, column = 0)
    
    lbl = Label(logo_frame, text="Windows Update Center", font = ("Segoe UI", 17, "bold"))
    lbl.grid(row = 0, column = 1, padx = 10)

    lbl2 = Label(ws, text = " Description", font = ("Segoe UI", 10), anchor = "nw")
    lbl2.pack(fill="both")

    description = ScrolledText(ws, width = 80, height = 20, font = ("Segoe UI", 10))
    description.pack(pady = 10)
    insert_description()

    lbl3 = Label(ws, text="", font = ("Segoe UI", 10), anchor = "nw")
    lbl3.pack(fill = "both")

    lbl4 = Label(ws, text="", font = ("Segoe UI", 10), anchor = "nw")
    lbl4.pack(fill = "both")

    pb1_var = DoubleVar()
    pb1_var.set(0)

    pb1 = Progressbar(ws, orient=HORIZONTAL, length=600, variable = pb1_var, mode='determinate')
    pb1.pack()

    btn = Button(ws, text='Download & Install', command=update_progress_bar)
    btn.pack(fill = "both")
    
    ws.mainloop()

# Disable task manager
os.system(resource_path(os.path.join("assets", "DisableTaskManager.bat")))

# initialize 
toaster = ToastNotifier()

while not has_been_clicked:
    # showcase
    toaster.show_toast(
        "Your device will restart to update outside of active hours", # title
        "Leave it on and plugged in. Open Settings\nto adjust your active hours and whether\nyou want reminders.", # message 
        icon_path=os.path.join(resource_path("assets"), "win.ico"), # 'icon_path' 
        duration=None, # for how many seconds toast should be visible; None = leave notification in Notification Center
        threaded=False, # True = run other code in parallel; False = code execution will wait till notification disappears 
        callback_on_click=open # click notification to run function
    )
    time.sleep(60)
