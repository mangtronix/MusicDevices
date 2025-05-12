# Music Devices Final Project - EchoTerrarium
### Meera AlKhazraji, Akif Rattu, Ahmed Bilal, Khalifa

## Concept:

EchoTerrarium is a musical device that represents humans’ connection to nature, their interactions, and the consequences of these interactions. By allowing users to touch and feel around the flowerbed part of the device, there is a tangible connection built between the presence of a person and the audio as it changes with each movement. This project is intended to give plants the ability to communicate using sounds and express their dissent or satisfaction. The project employs sound and lights to show the plants’ supposed feelings; loud, grainy sounds for intrusions with flashing lights, and calm pulsating greens for when it is being watered. 

## User interaction

Users are invited to observe the EchoTerrarium in its idle state. It seems peaceful and calm and undisturbed with an ambient synthesizer sound rising and falling as it ‘breathes’ calmly. Then the users are allowed to touch the green plants that are minding their own business. Suddenly, users can hear the music start to distort, get louder, and even have multiple different sounds fade in and out. As users move their hands around, the sounds change, which shows them that their actions are the reason for the music becoming noisier. 

Then the users are prompted to the watering can resting on its platform next to the terrarium. They are asked to pick it up and observe the effects as they water the plants. They are able to see the lights switch to a calm, soothing green to show that their action of watering the plant has made it healthier. 

## Technical Implementation

The project can be broken down into 3 main interactions.

#### The Hands:

The hands are the main way to interact with the project. Using a Logitech Webcam, the computer is able to pick up users’ hands as they come into frame while interacting with the project. In the browser, HandmateMIDI (built with Google’s MediaPipe framework) by Monica Lim is activated to detect the hands and track multiple points along the fingers. This program is also able to differentiate between the left and right hands. This information is then transmitted as MIDI signals through virtualMIDI to Ableton 12 Lite where it is pegged to many different effects and loops, like the right index finger’s y position was matched to the level of the drum loop; higher the value (i.e., cloer the hand to the plants) louder the sound. 

#### The Watering Can:

The watering can was also attached to a simple on/off switch to the microcontroller. This circuit was built with 2 pieces of copper tape glued to the top of a base several centimeters apart. When the can was set, it closed the circuit as it was made of steel. Once lifted, it would break the circuit, triggering a change in the state of the project.

#### The Lights:

Using 54 Neopixels on a strip, we managed to light up the whole project on the inside of the arc, creating a bright and inviting feel. In the idle state, the lights are white and rise from either side in a flowing manner and meet in the middle at the top. When triggered by the can being lifted by the users, the lights are turned into a green hue, which signifies growth and life. 

### Construction:

For the construction, we used the Prusa XL to create a hollow plastic cylinder that had a ledge on the inside to hold the base upon which the plants rested. The base was made from wood so that we could add holes easily for the wires and plants. The bottom half of the base was made with bendable plywood that was cut to size and rolled into a cylinder. It was glued to the plastic to hide the electronics. We also added an arch that rose over the top and connected both sides like a basket handle. The Neopixel strip was attached to the inside of this arch.

## Reflection and Future Considerations:

In the future, we hope to have several changes:

1. A camera with a wider FoV: We felt that the camera we used was not able to detect hands instantly because it couldn't see the hands unless they were positioned just right. A wider FoV camera would have more room to ‘see’ the hands

2. Change the HandmateMIDI source code to allow more interactions: HandmateMIDI is limited to 5 channels with limited detection points. MediaPipe is powerful enough to support many more points, so by editing the source code (which is available on Lim’s Github), we can make this project more interesting

3. Make the watering can interact with the music: due to limited time, we could not enable communication between the Adafruit microcontroller and the watering can circuit. It would help our concept of “watering the plant to give it birth” if there was a peaceful change in music in addition to the lights

## Video documentation:

[Video]([url](https://youtu.be/uhQBqstSYw0?si=OlXjtFgWrZcZWgMi))
