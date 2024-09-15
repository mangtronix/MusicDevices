# Weekly Schedule - Weeks 1-7

[Weekly Schedule Spreadsheet](https://docs.google.com/spreadsheets/d/14s9f2PLqj50BRLKKCZjZiCTpdnHFVN-IBkaVPIkFLVE/edit?usp=sharing)

- [Week 1](#week-1) – Introduction / NIME, Music Devices, and Sound Installations
- [Week 2](#week-2) – Applied music theory, Western and beyond
- [Week 3](#week-3) – Arduino for NIME
- [Week 4](#week-4) – Musical interface design, MIDI
- [Week 5](#week-5) – Musical sensors
- [Week 6](#week-6) – Rapid prototyping
- [Week 7](#week-7) – Idea Lab
- SPRING BREAK
- [Week 8](WeeklySchedule2.md#week-8) – Project proposal development
- [Week 9](WeeklySchedule2.md#week-9) – Project proposal presentation, implementation starts!
- [Week 10](WeeklySchedule2.md#week-10) – Telling your story / documenting your work
- [Week 11](WeeklySchedule2.md#week-11) – Guest Speaker, project production
- [Week 12](WeeklySchedule2.md#week-12) – Music performance, project feedback
- [Week 13](WeeklySchedule2.md#week-13) – User testing
- [Week 14](WeeklySchedule2.md#week-14) – Final project presentations
- [IM SHOW](WeeklySchedule2.md#im-show) – Show final project / Update final documentation

Note: Exact due dates for assignments and readings are indicated in Brightspace

---

# Week 1

## Week 1.1

Introduction
- Class introductions
- Review syllabus
- Textbook at bookstore
- Class kits will be distributed in class

## Week 1.2

Music Devices, NIME and Sound Installations
- [New Interfaces for Musical Expression (nime.org)](https://www.nime.org/)
- [Push Turn Move (Bjooks)](https://bjooks.com/products/push-turn-move-the-book)
- [10 Sound Installations that Inspire and Create Connection (Medium)](https://medium.com/@oskarlindskog/10-sound-installations-that-inspire-and-create-connection-73eabd5ce075)

### Homework - Week 1.2

Due before start of next class

- **Read** {music theory}
  - For details on the reading see Brightspace->Discussions->Reading 1
  - **Post** your response in the discussion forum
  - **Be ready** to discuss the topic in class

---
# Week 2

## Week 2.1
Applied music theory, Western and beyond
- [Learn music theory in half an hour (Andrew Huang / YouTube)](https://youtu.be/rgaTLrZGlk0?si=n52AtMMm5wVyZF4t)
- [Music Theory For Beginners (Taetro / YouTube)](https://www.youtube.com/watch?v=CluuHrr7HG4&list=PLoO2tOP2r-XvoFc7cnfYcomf1X0XcQvDC)
- [Arabic maqam (Wikipedia)](https://en.wikipedia.org/wiki/Arabic_maqam)
- [Pitch is political: learning Arabic maqams and decolonizing music](https://cdm.link/2024/08/pitch-is-political/)
- [tuning.ableton.com](https://tuning.ableton.com/)
    - "A tuning system is a way to organize musical pitch, by narrowing down from the infinite number of possible pitches to a usable subset."
    - [Listen (tuning.ableton.com)](https://tuning.ableton.com/introduction/listen/)
        - Different scales

## Week 2.2
Workshop: Ableton, software synthesizers
- Introduction to Ableton Live
- Ableton Live editions
    - [Intro, Standard, Suite](https://www.ableton.com/en/live/compare-editions/)
    - Live 11 Suite is available in C3-116
    - Live Lite (free license) comes with many hardware controllers and some apps
        - iOS apps with free Live Lite license
          - [Koala Sampler](https://www.koalasampler.com/)
            - Settings -> Get Live Lite
          - [Ableton Note](https://www.ableton.com/en/note/)
            - Settings -> Get Ableton Live Lite
- Ableton Live Tutorials
    - [Getting started with Live (Ableton)](https://www.ableton.com/en/live/learn-live/)
    - [Ableton Live for Beginners (Taetro / YouTube)](https://www.youtube.com/watch?v=RSnjD6xe5bM&list=PLoO2tOP2r-XsXH0lybWl9zMvYp3lpLF46)
- Default scale / tuning
    - [tuning.ableton.com](https://tuning.ableton.com/)
- Using alternative scales
    - [A Guide to the Maqam Tuning Presets for Ableton Live 12 (Ableton)](https://tuning.ableton.com/arabic-maqam/maqam-guide/)
- 

### Homework - Week 2.2

Due before start of next class

- **Task:**  
---

# Week 3

## Week 3.1
Arduino for NIME
- [Arduino in 100 Seconds (YouTube)](https://www.youtube.com/watch?v=1ENiVwk8idM)

Hardware kit
- [Adafruit ESP32-S3 Reverse TFT Feather (Adafruit)](https://learn.adafruit.com/esp32-s3-reverse-tft-feather/overview)
    - Uses Adafruit [Feather](https://learn.adafruit.com/adafruit-feather/overview) form factor
    - FeatherWings are similar to Arduino Shields - stackable add-on boards
    - QT connector allows connection to QT breakout boards
- STEMMA / QT / I2C breakout boards
    - I2C is a digital communication protocol for connecting different integrated circuits (ICs)
    - Uses 4 wires (Power, Ground, Data, Clock)
    - STEMMA / QT is a standard connector for the I2C bus
        - Convenient connection without soldering
    - [Working with I2C Devices (Adafruit)](https://learn.adafruit.com/working-with-i2c-devices/overview)
    - Reading/writing over I2C is slower than connecting directly to hardware like buttons and knobs
        - Can cause issues with e.g. missing incoming MIDI messages
- [Adafruit NeoKey 1x4 QT I2C Breakout (Adafruit)](https://learn.adafruit.com/neokey-1x4-qt-i2c)
- [Adafruit NeoSlider (Adafruit)](https://learn.adafruit.com/adafruit-neoslider)
- Many more sensors / boards available for checkout from IM Lab / Connect2
  - [https://www.nyuadim.com/resources/]

## Week 3.2
Workshop: Arduino for NIME
- [Arduino IDE Setup for ESP32-S3 Reverse TFT Feather(Adafruit)](https://learn.adafruit.com/esp32-s3-reverse-tft-feather/arduino-ide-setup-2)
    - Install Arduino IDE
    - The board we are using is the Adafruit Feather ESP32-S3 Reverse TFT
    - We need to get the latest board support for ESP32 provided by the manufacturer (Espressif)
    - Add third-party board URL in Arduino IDE->Settings
        - `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
    - Install Board Support Package via Tools->Board->Board Manager->Search for 'esp32 espressif'
    - To verify look for Tools->Board->ESP32 Arduino->Adafruit Feather ESP32-S3 Reverse TFT
    - We need to manually reset the board by pressing the reset button after uploading new code
- Verify that your software / hardware is working
    - [Load classic 'Blink' sketch (Adafruit)](https://learn.adafruit.com/esp32-s3-reverse-tft-feather/using-with-arduino-ide)
    - The first time we load the blink sketch can be a bit tricky because we need to overwrite the CircuitPython firmware that is pre-loaded on the board
- Run the factory shipped demo
    - Demonstrates using the TFT display, buttons, battery monitor, etc
    - Requires us to install several Arduino libraries into the Arduino IDE
    - [ESP32-S3 Reverse TFT Factory Shipped Demo (Adafruit)](https://learn.adafruit.com/esp32-s3-reverse-tft-feather/factory-shipped-demo-2)

- [Installing Libraries (Arduino)](https://docs.arduino.cc/software/ide-v1/tutorials/installing-libraries/)

### Homework - Week 3.2

Due before start of next class

- **Task:**  
---

# Week 4

## Week 4.1
Musical interface design, MIDI
- [DIY USB Midi Controller With Arduino: a Beginner's Guide
(Instructables)](https://www.instructables.com/DIY-USB-Midi-Controller-With-Arduino-a-Beginners-G/)
- [Create a MIDI Device
 (Arduino tutorials)](https://docs.arduino.cc/tutorials/generic/midi-device/)
- [How to Build Arduino MIDI Controllers - The Complete Guide (Nerd Musician / YouTube)](https://www.youtube.com/watch?v=IwfycC8rLos)
- [MIDIUSB Library for Arduino
 (GitHub)](https://github.com/arduino-libraries/MIDIUSB)

## Week 4.2
Workshop: MIDI controllers, wired and wireless
- Create our first MIDI controller using ESP32-S3 Feather
- Run sample code for sending our first note
    - [MIDIUSB_write.ino (GitHub)](https://github.com/arduino-libraries/MIDIUSB/blob/master/examples/MIDIUSB_write/MIDIUSB_write.ino)
    - Sends note on/off in simple loop with blocking delay

- Latency in audio systems
    - What is latency?
        - Time between something being triggered (e.g. pushing a button) and sound being received by listener
        - [How Latency Works (Ableton)](https://help.ableton.com/hc/en-us/articles/360010545559-How-Latency-Works)
        - [How to reduce latency (Ableton)](https://help.ableton.com/hc/en-us/articles/209072289-How-to-reduce-latency)
    - Audio buffer size is a primary source of latency in software systems
        - Larger buffers allow CPU to process audio in larger chunks (more efficient) but increase latency
        - To minimize latency choose the smallest buffer size that does not cause CPU overloading
    - Tools for measuring latency
        - Play your device and see if it feels laggy
        - Record events / audio in Ableton
        - [Is It Snappy? (iOS app)](https://isitsnappy.com/)
            - Visually measure latency using high framerate video
    - Musicians can adapt to a *fixed* latency by playing notes earlier
    - Wireless connections can add a variable latency
        - Interference and transmission loss can cause packets to be retransmitted
    - The operating system and i/o system also adds latency
        - [Why is there so much latency on my android device?
 (Koala Sampler)](https://www.koalasampler.com/help/android/why-is-there-so-much-latency-on-my-android-device/)


### Homework - Week 4.2

Due before start of next class

- **Task:**  
---

# Week 5

## Week 5.1
Musical sensors


## Week 5.2
Workshop: Musical sensors

### Homework - Week 5.2

Due before start of next class

- **Task:**  
---

# Week 6

## Week 6.1
Group project overview, work examples, rapid prototyping

## Week 6.2
Workshop: 2D / 3D design with Autodesk Fusion

### Homework - Week 6.2

Due before start of next class

- **Task:**  
---

# Week 7

## Week 7.1
Idea Lab

## Week 7.2
Project group formation, start project proposal, initial project feedback

### Homework - Week 7.2

Due before start of next class

- **Task:**  
---
# SPRING BREAK

