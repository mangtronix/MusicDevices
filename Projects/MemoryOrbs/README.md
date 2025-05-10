# Memory Orbs

## Summary

**Memory Orbs** is an interactive light-and-sound music device inspired by *Pixar’s Inside Out*. Each glowing orb represents one of five core emotions—**Joy**, **Sadness**, **Anger**, **Fear**, and **Disgust**—with three orbs per emotion.

When touched, each orb lights up in its corresponding color and plays a unique musical instrument or sound that matches its emotional tone. The sounds are designed to harmonize, letting users create layered, expressive performances by activating multiple orbs.

If a user simultaneously holds five orbs representing five different emotions, the system triggers a special **core memory** sequence: all orbs glow golden, and the *Inside Out* theme plays in full—symbolizing emotional balance.

The experience combines **capacitive touch sensing**, **Neopixel lighting**, and an **Adafruit Feather microcontroller**. Orb shells were 3D printed using a **Prusa printer**, with bases made on an **Ultimaker**. A laser-cut acrylic plate supports the orbs, mounted on a hand-sawn wooden base that hides the wiring and breadboard—creating a clean, immersive design.

---

## Project Concept and Its Relationship to Musical Practices

**Memory Orbs** turns emotions into musical performance. Each orb acts as a distinct musical layer:

- **Joy** → Bright, cheerful sounds  
- **Sadness** → Soft, deep melodies  
- **Anger** → Strong, intense beats  
- **Fear** → Mysterious and echoing notes  
- **Disgust** → Wobbly, sharp sounds  

This approach mirrors **modular synthesizers** and **live looping**: users influence sound directly through touch, crafting emotional compositions in real time. The final "core memory" event unifies the layers into a complete performance.

---

## User Interaction

### Single Orb Activation

Touching an orb lights it up in its designated color:

- Joy → Yellow  
- Sadness → Blue  
- Anger → Red  
- Disgust → Green  
- Fear → Purple  

Each orb triggers a unique instrument or sound through **Ableton Live**.

### Layered Musical Performance

- Multiple orbs can be activated at once.  
- Sounds harmonize, allowing users to build personalized emotional soundscapes.

### Core Memory Sequence

- Touching five central orbs (one of each emotion) triggers a **core memory** event.  
- All orbs glow golden and play the *Inside Out* theme.

---

## Technical Implementation

The project combines physical computing, fabrication, sound design, and synchronization.

### Components

- **Capacitive Touch Sensors (MPR121):** Each orb is touch-sensitive, responding instantly to human touch.
- **Neopixel RGB LEDs (WS2812B):** Provide smooth, color-specific illumination for each emotion.
- **ESP32 Adafruit Feather:** Manages sensor input, LED control, and music synchronization.


### Fabrication

- **Orbs:** 3D printed on a *Prusa MK4* with clear PETG filament for optimal light diffusion.
- **Bases:** 3D printed on an *Ultimaker 2+* for precise structure and durability.
- **Acrylic & Wood Mount:** The orbs are mounted on a laser-cut acrylic plate that fits perfectly over a hand-sawn wooden base. This design sandwiches the wiring and breadboard underneath, providing a clean and immersive experience.


### Sound Integration

- **Ableton Liv:e** All musical elements are produced (except for a few that we downloaded from *freesound.org* and *Youtube*) and mapped in Ableton Live.  
MIDI signals from the Adafruit Feather trigger Ableton samples, allowing each orb to function as a live MIDI instrument.

---

## Reflection and Future Directions

For us, **Memory Orbs** successfully bridged emotional expression with interactive sound, allowing users to perform music through touch. In future iterations, we could:

- Integrate wireless MIDI capabilities to expand the setup and allow for broader, more immersive interactions.
- Experiment with haptic feedback to provide touch-based vibrations when an orb is activated.
- Explore multi-user capabilities, enabling collaborative performances that represent collective emotional states.
- More buttons or functionalities such as recording the mix they made, controlling the volume, rotary knobs, and sliders to add effects etc.

We think that this opens possibilities for therapeutic applications in emotional processing, live musical performance, and public interactive installations.

---

## Gallery

![Memory Orbs-MYA_1607](https://github.com/user-attachments/assets/fbe543ba-690e-4a7c-bef1-3d944a4d453c)

![Memory Orbs-MYA_1616](https://github.com/user-attachments/assets/7e52289a-7c94-4efc-b8ca-c853eaab82bf)


