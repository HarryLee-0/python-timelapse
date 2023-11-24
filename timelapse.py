import time, cv2, os, numpy
from PIL import ImageGrab
from pynput.keyboard import Listener,Key

# Settings
time_interval = 1  # in seconds
fps = 30
images = []

# Options Menu
print("Press Enter to start. Press O and Enter for options.")
if input("") in ["O","o"]:
    print("Options:")
    time_interval = float(input(" | Time Interval In Seconds (default = 1): "))
    fps = int(input(" | FPS (default = 30): "))
    print(f" | 1 timelapse second = {fps*time_interval} real seconds (default = 30)")
    print("Options Set.\n")

print("Press Page Down to stop timelapse.")

# Listener for enter press
def press(key):
    if key == Key.page_down:
        return False
listener = Listener(on_press = press)
listener.start()

# Continuously take screenshots until 'Enter' is pressed
while True:
    # Take screenshot
    im = ImageGrab.grab()
    im = cv2.cvtColor(numpy.array(im), cv2.COLOR_RGB2BGR)
    images.append(im)
    time.sleep(time_interval)
    if not listener.running:
        break


# Options and compile images into a video
print("Timelapse Ended!")
print(" | Name? (do not add .mp4)")
video_name = str(input(" | ")) + ".mp4"

print(" | User Folder Name? (type nothing for downloads)")
directory = str(input(" | "))
if directory == "":
    home_directory = os.path.expanduser("~")
    video_directory = os.path.join(home_directory, "Downloads")
    os.makedirs(video_directory, exist_ok = True)  # Create the directory if it doesn't exist
else:
    home_directory = os.path.expanduser("~")
    video_directory = os.path.join(home_directory, directory)
    os.makedirs(video_directory, exist_ok = True)  # Create the directory if it doesn't exist

video_name = os.path.join(video_directory, video_name)

print(f"Compiling {len(images)} Frames Into A Video...")
start = time.time()
height, width, layers = images[0].shape
video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

for image in images:
    video.write(image)

try:
    cv2.destroyAllWindows()
except:
    pass
video.release()
end = time.time()

print(f"Video saved as {video_name} as {round((len(images)/fps)*100)/100} seconds. {len(images)} frames compiled in {round((end-start)*1000)/1000} seconds at {fps} fps.")
