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

1. Go into the <code>dist</code> folder
2. Go into the <code>run</code> folder
3. Look for the LADSoundboard Application (<code>LADSoundboard.exe</code>)
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

#### Algorithm
I use an LBPH (local binary pattern histogram) algorithm, provided by OpenCV, to determine identifies and respective faces.
For more information on local binary patterns, check out:

https://towardsdatascience.com/face-recognition-how-lbph-works-90ec258c3d6b


## How to update the songs:
The songs get updated and referenced through <code>songs.data</code>. The data structure is used when generating the soundboard values and faces, but the music doesn't come from this table and respective URLs. Rather, this data structure is used to extract music from youtube through the <code>extract_music.py</code> file.

To update songs (and add or remove people), do the following:
1. Fill in the songs.dat with your Name, groupid, YouTube URL, Start Time, and End Time
 ⋅⋅⋅ + note that the name will be reflective on the soundboard, so I recommend you keep it short (like an office or team nickname)
 ⋅⋅⋅ + groupid pertains to which tab the row belongs to. In a future update, there will be capabilities for 2 groups, so this will apply there. For now, you should put down 1 to show up on the first group, and any number for otherwise (hidden).
 + YouTube URLs do not have to be the shortened version like I have put as example. It just seems easier to look that way.
 + Start time is not necessary -- default is 0:00.
 + End time is also not necessary -- default is 10 seconds after start time.
 + Combinations apply for start and end times (ie. start time of 1:23 with no end time is esssentially [1:23, 1:33].
2. Run the <code>extract_music.py</code> file.

Now, you should expect to find songs appropriately named with the correct length / section in the <code>audio</code> folder.

#### Icon
To Vin Scully, the best announcer that ever lived. Live. Breathe. Blue.
