import time, cv2, os, numpy, threading
from PIL import ImageGrab
from pynput.keyboard import Listener,Key
from tkinter import *
from tkinter import ttk

# Settings
time_interval=1  # in seconds
fps=30
images=[]

# Options Window
def conversionupdater():
    global fps, time_interval
    while running==True:
        try:
            time_interval=float("0"+entry.get())
            fps=float("0"+entry2.get())
            conversion.config(text=f"1 timelapse second={round(fps*time_interval*100)/100} real seconds")
        except:
            pass        

running=True
root=Tk()
window=ttk.Frame(root, padding=10)
window.grid()
ttk.Label(window, text="Options: ").grid(column=1,row=0)
ttk.Label(window, text="Time Interval (Seconds)").grid(column=1,row=1)
entry=ttk.Entry(window)
entry.grid(column=2,row=1)
entry.insert(0,time_interval)
ttk.Label(window, text="FPS:").grid(column=1,row=2)
entry2=ttk.Entry(window)
entry2.grid(column=2,row=2)
entry2.insert(0,fps)
conversion=ttk.Label(window)
conversion.grid(column=1,row=3)
ttk.Button(window, text="Sumbit", command=root.destroy).grid(column=1, row=10)

conversionupdate=threading.Thread(target=conversionupdater)
conversionupdate.daemon=True
conversionupdate.start()
root.mainloop()
running=False


# Timelapse Window
def timelapse():
    global images
    # Screenshot loop
    start=time.time()
    while running==True:
        # Take screenshot
        im=ImageGrab.grab()
        im=cv2.cvtColor(numpy.array(im), cv2.COLOR_RGB2BGR)
        images.append(im)
        time.sleep(time_interval)
        try:            
            frames.config(text=f"{len(images)} frames taken")
            seconds.config(text=f"{round((time.time()-start)*100)/100} seconds elapsed")
            timelapseseconds.config(text=f"Timelapse {round((len(images)/fps)*100)/100} seconds long")
        except:
            pass
        if not running:
            break

running=True
root=Tk()
window=ttk.Frame(root, padding=10)
window.grid()
ttk.Label(window, text="Timelapse").grid(column=1,row=0)
ttk.Button(window, text="End Timelapse",command=root.destroy).grid(column=1, row=10)
ttk.Label(window, text="Stats:").grid(column=1,row=2)
frames=ttk.Label(window, text="")
frames.grid(column=1,row=3)
seconds=ttk.Label(window, text="")
seconds.grid(column=1,row=4)
timelapseseconds=ttk.Label(window, text="")
timelapseseconds.grid(column=1,row=5)

timelapser=threading.Thread(target=timelapse)
timelapser.daemon=True
timelapser.start()
root.mainloop()
running=False


# Storage and compile images into a video
def presaving():
    global video_name, directory
    while running==True:
        try:
            video_name=str(entry.get())+".mp4"
            directory=str(entry2.get())
        except:
            pass

running=True
root=Tk()
window=ttk.Frame(root, padding=10)
window.grid()
ttk.Label(window, text="Saving").grid(column=1,row=0)
ttk.Label(window, text="Timelapse Has Ended!").grid(column=1,row=0)
ttk.Button(window, text="End Timelapse",command=root.destroy).grid(column=1, row=10)
ttk.Label(window, text="Stats:").grid(column=1,row=2)
ttk.Label(window, text=f"{len(images)} frames taken").grid(column=1,row=3)
ttk.Label(window, text=f"Timelapse {round((len(images)/fps)*100)/100} seconds long").grid(column=1,row=4)
ttk.Label(window, text="Name: (default=time)").grid(column=1,row=5)
entry=ttk.Entry(window)
entry.grid(column=1,row=6)
entry.insert(0,"timelapse")
ttk.Label(window, text="User Folder Name: (deafult=downloads)").grid(column=1,row=7)
entry2=ttk.Entry(window)
entry2.grid(column=1,row=8)
entry2.insert(0,"")

presaver=threading.Thread(target=presaving)
presaver.daemon=True
presaver.start()
root.mainloop()
running=False


# Execute Saving
if directory=="":
    home_directory=os.path.expanduser("~")
    video_directory=os.path.join(home_directory, "Downloads")
    os.makedirs(video_directory, exist_ok=True)  # Create the directory if it doesn't exist
else:
    home_directory=os.path.expanduser("~")
    video_directory=os.path.join(home_directory, directory)
    os.makedirs(video_directory, exist_ok=True)  # Create the directory if it doesn't exist
if video_name=="":
    video_name=str(time.time())

video_name=os.path.join(video_directory, video_name)


# Saving
def saving():
    global start, end, video, images
    start=time.time()
    height, width, layers=images[0].shape
    video=cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    for image in images:
        video.write(image)

    try:
        cv2.destroyAllWindows()
    except:
        pass
    video.release()
    end=time.time()

running=True
root=Tk()
window=ttk.Frame(root, padding=10)
window.grid()
ttk.Label(window, text="Saving").grid(column=1,row=0)
ttk.Label(window, text=f"Compiling {len(images)} Frames Into A Video...").grid(column=1,row=1)
savedas=ttk.Label(window, text="")
savedas.grid(column=1,row=2)


saver=threading.Thread(target=saving)
saver.daemon=True
saver.start()
root.mainloop()


savedas.config(text=f"Video saved as {video_name} as {round((len(images)/fps)*100)/100} seconds. {len(images)} frames compiled in {round((end-start)*1000)/1000} seconds at {fps} fps.")
ttk.Button(window, text="Close",command=root.destroy).grid(column=1,row=3)
running=False
