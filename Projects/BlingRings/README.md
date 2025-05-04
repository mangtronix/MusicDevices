# Bling Rings

# Project concept and its relationship to musical practices
Our project explores a fusion of hip-hop sound culture and jewelry aesthetics by designing a set of wearable MIDI controller rings, inspired by the stylistically chunky, flashy jewelry commonly worn by its pioneers. 

We worked on three primary songs:
* “Not Like Us” – Kendrick Lamar
* “Check the Rhime” – A Tribe Called Quest
* “The Way I Are” – Timbaland

# Technical explanation of how the project is implemented
Each component on the knuckle duster bases houses a control/ trigger.

Knuckle duster base #1:
* Circuitpython Adafruit ESP32-S3 LCD screen: visuals (ex. lyrics, music, data visualization, etc.) but also as central control
* Rotary knob: mapped to delay on Ableton
* Battery

Knuckle duster base #2:
- NeoKey 1x4 QT I2C that contains— 
* ⁠Button that triggers each of the respective songs: cycles through song 1, 2 and 3 and then matches its designated parameters (ex. BPM) to each of the 3 buttons
* 3 buttons: each mapped to a specific track of either vocals, bass/ drums, and keys for the respective song (e.g. song 1 = this behavior, song 2 = another).
* 1 button with an array of ad libs
* ESP32-S3 hidden underneath as the central control
* Battery

We first had to isolate all the components of the songs into:
1. Vocals
2. Bass/ drums (together)
3. Keys
For each of the 3 buttons

Then we had to sync all of these song components to the beats by cutting the clips into the exact time frame we needed, and then putting those edited tracks into Ableton Live (removing warp).

Each song is mapped to a BPM:
* “Not Like Us” – Kendrick Lamar (101 BPM)
* “Check the Rhime” – A Tribe Called Quest (96 BPM)
* “The Way I Are” – Timbaland (115 BPM)

We made it more user-friendly by making it so that there is some kind of visual indicator that a track (bass/ drums, keys, or vocals) is playing when you click on its respective button:
- Clicking a button the first time —> trigger/ play the track —> LED lights up to a certain color and ‘pulsates’: active mode
- Click a button the second time —> switch off/ stop playing the track —>LED switches off: standby mode

This way, users can more intuitively tell whether a track is on or off.

The knuckle duster base and button keycaps were all modeled on Fusion and 3D-printed with clear PETG. 

4 keycaps (add images):
- DRIP 
- ‘Ice’ cube
- Dollar sign
- Dome
To allow for color customizability via the color-changing NeoPixel LEDs

2 knuckle dusters (add images) with different hole diameters to fit the average female hand:

The single rotary knob cap was similarly modeled on Fusion but instead 3D printed with White PLA and painted to look like a stack of records (add images):

# Explanation of the user interaction and instructions to user

# 2-3 minute video demonstrating the project

# Reflection on the project and directions for future work
