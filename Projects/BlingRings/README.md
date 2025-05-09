# Bling Rings

# Project concept and its relationship to musical practices
Bling Rings is an interactive wearable MIDI controller system that draws on and explores the fusion of hip-hop sound culture and jewelry aesthetics, and fuses it with music production technology. The project consists of two knuckle-duster-style bases worn on the hands, each embedded with MIDI controls, allowing the user to remix and trigger components of hip-hop songs through buttons and a rotary knob.

We worked on three primary songs:
* “Not Like Us” – Kendrick Lamar
* “Check the Rhime” – A Tribe Called Quest
* “The Way I Are” – Timbaland
  
These songs were chosen for their distinct sonic identities and remix potential.

# Technical explanation of how the project is implemented
Each component on the knuckle duster bases houses a control/ trigger.

Knuckle duster base #1:
* Circuitpython Adafruit ESP32-S3 LCD screen: visuals that display what song is playing (also simultaneously acts as central control)
(add image)
* Rotary knob: mapped to delay on Ableton, allowing for live manipulation
* Battery (wireless)

Knuckle duster base #2:
- NeoKey 1x4 QT I2C that contains— 
* Main Trigger Button: cycles through the three songs. Each press loads the corresponding BPM and track assignments into Ableton.
* 3 buttons: each mapped to a specific track of either vocals, bass/ drums, and keys for the respective song (e.g. song 1 = this behavior, song 2 = another). Pressing a button toggles its corresponding track on/off.
* ESP32-S3 hidden underneath as the central control: handles MIDI messaging and communication with Ableton

We first had to isolate all the components of the songs into:
1. Vocals
2. Bass/ drums (together)
3. Keys
For each of the 3 buttons

Then we had to sync all of these song components to the beats by cutting the clips into the exact time frame we needed, and then putting those edited tracks into Ableton Live. Warp mode was turned off to preserve timing integrity, and each song was assigned a fixed tempo/ BPM:
* “Not Like Us” – Kendrick Lamar (101 BPM)
* “Check the Rhime” – A Tribe Called Quest (96 BPM)
* “The Way I Are” – Timbaland (115 BPM)

 The system automatically adjusts tempo when switching between songs.

We made it more user-friendly by making it so that there is some kind of visual indicator that a track (bass/ drums, keys, or vocals) is playing when you click on its respective button:
- Clicking a button the first time —> trigger/ play the track —> LED lights up to a certain color and ‘pulsates’: active mode
- Click a button the second time —> switch off/ stop playing the track —>LED switches off: standby mode

This way, users can more intuitively tell whether a track is on or off.

The knuckle duster base and button keycaps were all modeled on Fusion and 3D-printed with clear PETG. 

Each keycap is visually distinct and inspired by hip-hop iconography: (add images)
- “DRIP” lettering
- Ice cube symbol
- Dollar sign ($) motif
- Dome shape

These transparent designs allow dynamic LED colors to shine through, allowing for color customizability via the color-changing NeoPixel LEDs.

2 knuckle dusters (add images) with different hole diameters to fit the average female hand:

The single rotary knob cap was similarly modeled on Fusion but instead 3D printed with White PLA and painted to look like a stack of records—a visual nod to DJ culture and analog roots within hip-hop. (add images)

# Explanation of the user interaction and instructions to user
1. The user wears both rings, one on each hand.
2. Click on main trigger button on knuckle duster base #2 to cycle through songs, choose 1 (first song: red, second song: blue, third song: green)
3. Click the three playback buttons to trigger or mute specific components/ stems (vocals, bass/drums, keys) as desired
4. Use the rotary knob to adjust the delay FX in real-time as desired

# 2-3 minute video demonstrating the project

# Reflection on the project and directions for future work
For future iterations, we hope to:
- Add more controls other than just delay (scratch effect, low-pass filter sweeps, beat repeat, or reverb toggles—to allow users to experiment with a wider range of live manipulation techniques)
- Expand the library of songs and allow for custom song uploads
- Implement wireless communication for the second knuckle duster
- Refine ring sizing and ergonomics for broader wearability
- More expressive visual interface on the LCD screen (GIFs, video)
