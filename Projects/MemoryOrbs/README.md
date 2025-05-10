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

- **Capacitive Touch Sensors (MPR121):** Detect user touch per orb.
- **Neopixel RGB LEDs (WS2812B):** Provide color illumination.
- **ESP32 Adafruit Feather:** Handles touch input, lighting, and MIDI output.

### Fabrication

- **Orbs:** 3D printed on a *Prusa MK4* with clear PETG filament for light diffusion.
- **Bases:** 3D printed on an *Ultimaker 2+* for structure and durability.
- **Acrylic & Wood Mount:** Acrylic plate laser-cut; wooden base hand-sawn and designed to hide circuitry for a polished look.

### Sound Integration

- **Ableton Live** handles audio playback and sound layering.
- MIDI signals from the Feather trigger sounds.
- Some effects and samples are from *freesound.org* and *YouTube*.

---

## Reflection and Future Directions

**Memory Orbs** successfully merged emotional storytelling with interactive sound. Future improvements could include:

- Wireless MIDI integration  
- Haptic feedback for tactile response  
- Multi-user support for collaborative performance  
- Extra features: recording, volume control, knobs/sliders for effects  

This concept has potential applications in:

- **Therapy**
- **Live performance**
- **Public interactive art**

---

## Gallery

![Memory Orbs-MYA_1607](https://github.com/user-attachments/assets/fbe543ba-690e-4a7c-bef1-3d944a4d453c)

![Memory Orbs-MYA_1616](https://github.com/user-attachments/assets/7e52289a-7c94-4efc-b8ca-c853eaab82bf)


