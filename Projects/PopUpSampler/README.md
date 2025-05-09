# Pop-Up Pirate Sampler

<img src="https://github.com/d7uzm/md-proj-repo/blob/main/00.jpg?raw=true" width="600"/>  

## Overview

The **Pop-Up Pirate Sampler** is a modified USB MIDI controller inspired by the classic *Pop-Up Pirate* toy. The project repurposes the toy’s sword-insertion mechanics to trigger audio samples through a digital audio workstation (DAW). Users interact by inserting swords into designated slots to activate sounds; however, inserting a sword into a "booby-trapped" slot triggers the pirate to pop up, triggering a "game over" state.

This project explores intersections of experimental instrument design and digital audio production. Its design goal is to provide an approachable yet innovative interface for sample-based music creation.

---

## Files (Non-media)

```
.
├── README.md
└── resources
    ├── support v2.f3d
    ├── project.py
    └── project.als
```

---

## Interaction Design

### Physical Interface

* **Device**: Adapted Pop-Up Pirate toy.
* **Inputs**: Six sword slots (original dimensions: 21.59 x 15.24 x 26.67 cm).
* **Outputs**: USB MIDI notes compatible with standard DAWs.
* **Feedback**:

  * **Audio**: Samples triggered within DAW (Ableton Live).
  * **Physical**: Pirate figure popping (along with music termination) indicates a triggered "game over" event.

### User Interaction

* **Insert Sword into active slot** → Triggers corresponding audio sample.
* **Insertion into booby-trapped slot** → Activates pirate figure and all the samples deactivate ("game over").

This design approach combines intuitive physical interaction with audio control.

---

## Technical Implementation

### Hardware Components

* **Microcontroller**: Adafruit Feather TFT (CircuitPython-compatible).
* **Sensors**:

  * **6 Light Dependent Resistors (LDRs)** positioned within sword slots for detection.
  * **1 LDR positioned beneath pirate figure** to detect pop-up event.
  * Consistent internal illumination (stable ambient source).
* **Housing**: Modified Pop-Up Pirate toy; unused slots are sealed to maintain controlled setting.
* **Internal Mounting**: Custom 3D-printed supports secure electronics and sensors.

### Input Logic

* **Sword Slot LDRs**:

  * Detect sword insertion by changes in ambient light.
  * Mapped directly to discrete MIDI notes.
* **Pirate Pop-up LDR**:

  * Detects light change indicating the pirate’s release.
  * Sends a designated MIDI signal indicating "game over".

<img src="https://github.com/d7uzm/md-proj-repo/blob/main/design.png?raw=true" width="600"/>  
<img src="https://github.com/d7uzm/md-proj-repo/blob/main/02.jpg?raw=true" width="600"/>  

### Software Stack

* **Firmware**: CircuitPython running on the Feather board.
* **MIDI Communication**: Standard USB MIDI protocol.
* **Sound Management**: Audio samples managed externally within DAW software.
* **Development**: Internal TFT display utilized for debugging purposes only.

(Used `SINEE - ABLETON LIVE RACKS + TEMPLATES` for the working template)

<img src="https://github.com/d7uzm/md-proj-repo/blob/main/ableton.png?raw=true" width="600"/>  


---

## Reflection

Adapting the Pop-Up Pirate toy into a functional MIDI controller presented both conceptual and practical challenges. While the game mechanics translated well into a musical interface, the internal layout of the toy was not designed for electronics. Fitting sensors, wires, and mounting hardware into a small, curved, and irregular interior required significant iteration. Managing light consistency for the LDRs also proved difficult, as minor leaks or alignment issues led to unreliable readings. These constraints demanded creative routing and tight tolerances, often pushing the physical design to its limits. Despite these challenges, the end result maintained mechanical stability and offered a clear, responsive interaction model.

### Potential Extensions

* **Wireless MIDI (Bluetooth LE)** and portable power options.
* **Modular sensor designs** using alternative interaction methods (smaller / modular sensors, etc.).

---

## User Response

Feedback highlighted that the core mechanic may feel overly simple. This is a fair observation; balancing accessible, intuitive interaction with deeper complexity posed a significant design challenge. While the current implementation prioritizes immediate playability, future iterations could explore layered interactions or adaptive sample behaviors to enrich the experience.

---

## Video
<a href="https://drive.google.com/file/d/1Mq3DcEKVP2tnj3s6g0Kzz7IYL-1Sl8cR/view?usp=drive_link">
  <img src="https://github.com/d7uzm/md-proj-repo/blob/main/video-preview.png?raw=true" width="600"/>
</a>

* **Video List**:

  * [Interaction](https://drive.google.com/file/d/1Mq3DcEKVP2tnj3s6g0Kzz7IYL-1Sl8cR/view?usp=drive_link)
  * [Full Play](https://drive.google.com/file/d/1aA__ZOl866Iy8DeEIS-lafFVclON6xh8/view?usp=drive_link)
  * [Pop Up](https://drive.google.com/file/d/16vZod2d-lNpjqyxCRXXbTY3Cx8Fr2LW9/view?usp=drive_link)

