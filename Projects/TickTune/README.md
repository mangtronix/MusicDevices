# TickTune
TickTune: A Musical Clock 
By: Jason Xia, Batool Al Tameemi, Marija Tomevska,Zhaniya Korpebayeva
Project Concept and Relationship to Musical Practices
<img width="922" alt="Screenshot 2025-05-07 at 6 02 08 PM" src="https://github.com/user-attachments/assets/7fb7f5e7-e6c2-437c-a435-f378f42f2d9a" />

TickTune is an interactive installation that transforms the concept of time into a multi-sensory experience. Inspired by traditional clock mechanisms and contemporary music practices, the project invites users to explore the rhythm of time through both sound and motion. Each clock in the system represents a unique sonic identity, ranging from bell tones to synthesized chimes, creating a layered soundscape that reflects different interpretations of time.

At its core, TickTune brings together experimental sound design and mechanical sculpture. It draws on traditions in ambient and generative music where repetition and variation shape the experience. It also reflects hands-on approaches found in modular synthesizers and analog music-making tools where physical interaction is central. By synchronizing gear rotation with melodic rhythm the piece reimagines ticking as a poetic performance.

**Design and Fabrication Process**
<img width="895" alt="Screenshot 2025-05-06 at 2 26 30 PM" src="https://github.com/user-attachments/assets/4a8c10aa-6aff-4654-8303-6d8be389b1f9" />

The physical form of TickTune began as a series of hand sketches. We started by imagining how each musical clock might look and move, thinking carefully about gear sizes, button placement, and how users would physically engage with the system. These sketches were then translated into digital 3D models using Fusion 360. Once the forms were finalized, we used PLA filament to print the components using the Prusa XL, a reliable large-format 3D printer. The use of PLA allowed us to achieve lightweight but durable parts that could handle the stress of repeated mechanical movement. The result is a tactile, sculptural object that invites users to touch, listen, and observe.

**Explanation of the User Interaction**
<img width="965" alt="Screenshot 2025-05-07 at 6 01 54 PM" src="https://github.com/user-attachments/assets/560da79b-6659-4285-be28-02ada6902e8d" />

Users are invited to engage with the concept of time in a playful and hands-on way. The interface includes three buttons and a single slider. Pressing a button activates a specific clock sound and sets its gears in motion. The slider controls the overall tempo of the installation which affects both the music and the speed of gear movement.

Users can trigger sounds one at a time or layer them together. Each combination results in a different musical output. Changing the tempo adds another expressive layer letting users simulate the feeling of time accelerating or slowing down. The interaction is both intuitive and rich allowing users to experiment and improvise freely.

**Technical Explanation of How the Project Is Implemented**
<img width="826" alt="Screenshot 2025-05-07 at 6 12 10 PM" src="https://github.com/user-attachments/assets/ab4a140b-7cd9-4c35-88d1-a52801b4ead9" />
TickTune is built through a combination of software and hardware systems. The software side uses Ableton Live with four MIDI tracks. The first three tracks are instrument layers representing different clock sounds. The fourth handles the MIDI input coming from the hardware controller. Each button on the hardware is mapped to a separate MIDI channel and triggers specific sound events. The slider sends control change messages to adjust the global tempo in real time.

On the hardware side we use a CircuitPython-compatible microcontroller such as the Adafruit Feather. The inputs come from a NeoKey keypad and a slider component. Outputs go to three stepper motors connected to separate gear mechanisms. When a button is pressed the corresponding clock melody begins and the matching gears start rotating. The slider adjusts how fast or slow the motors spin based on the tempo selected. This creates a one-to-one relationship between sound and motion.

**Reflection on the Project and Directions for Future Work**
<img width="881" alt="Screenshot 2025-05-07 at 6 03 23 PM" src="https://github.com/user-attachments/assets/dd2afbc8-6c83-4e4a-9c6a-5e4d32410ec1" />

TickTune successfully brings together sound movement and user input into one coherent experience. The piece has received positive feedback for its poetic approach to time and its accessibility for users of all backgrounds. The harmony between mechanical motion and musical rhythm created a strong emotional impact that made time feel tangible.

Looking forward there are many directions we want to explore. One idea is to expand the clock collection by including timekeeping devices from different cultures such as water clocks sundials and astrolabes. Each would be paired with distinct sound environments inspired by specific musical traditions. Another goal is to add visual elements such as projection mapping or LED systems that respond to tempo or user interaction.

We are also developing an autonomous playback mode where the clocks generate music based on external conditions such as the time of day or ambient light. This would make TickTune behave like a living timepiece that evolves over time. Additionally we are exploring wireless MIDI communication and portable setups to make installation in galleries or public spaces easier.

Eventually we want to create a system that allows users to save and share their compositions. Each session would become a personal version of time that can be archived and revisited. This would extend the project from an installation to a global platform for musical timekeeping.

TickTune began with a simple question. What does time sound like. The answers have turned into a collaborative exploration filled with rhythm motion and possibility.
**Video**
[![Watch the video](https://img.youtube.com/vi/ktMJiXBjbZ0/maxresdefault.jpg)](https://youtu.be/ktMJiXBjbZ0?si=CMn4vdmY-eFbGlGG)


