# Soundboard app for Windows
Made with love from Kivy and Python.

## Versions

### Version 2.0.0
+ Early stage face recognition to suggest identity. OpenCV!
+ Fluid manual tab.
+ Dynamic tab structure for adding faces (not for board).

### Version 1.0.0
+ Standalone App that's manual
+ Stable soundboard with fixed number of entries for a single tab.

## Important Information

#### Structure
Training data is contained in the data/training/ folder. The structure comes from this specific approach"
+ Name_From_<songs.dat>
    + #.png
    + #.png
    + #.png
    + #.png
    ...

#### To Run (Use)
Click on the desired version under the <code>Tags</code>. A zip file containing all the necessary files should be in there, with the executable.

1. Go into the <dist> folder
2. Go into the <run> folder
3. Look for the LADSoundboard Application (LADSoundboard.exe)
4. Double click -- ready to go!
Optional: Pin to taskbar or make shortcut, so you do not have to enter the folder each time.
Optional: Put into Programs folder, as a real program.

#### To Build (Development)
Must have a working kivy version. I've managed to build the <code>.spec</code> by using the <code>KivyInstaller.bat</code> file in my Python27 folder. Note the spec file won't build properly off of Anaconda python because of gstream. It will compile fine, however running the program yields errors. The only external modules you will need to have are:
+ Kivy
+ Pandas
+ NumPy
+ OpenCV (cv2)

Simply run the following command in a folder that you desire the application to have:

<code>python -m PyInstaller runApp.spec </code>

This should create a build and dist folder for you, where the executable is in the dist folder. More information can be found: https://kivy.org/docs/guide/packaging-windows.html

## How to update the Songs:
Fill in the songs.dat by Name, YouTube URL, and Start time
Run the extract_music.py file.
Songs are automatically cut into 10 second clips.
Any clips longer will need to be individually selected and trimmed.

#### Icon
To Vin Scully, the best announcer that ever lived. Live. Breathe. Blue.
