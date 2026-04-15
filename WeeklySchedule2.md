# Class Notes - Weeks 8-14

[Weekly Overview / Dates (Spreadsheet)](https://docs.google.com/spreadsheets/d/14s9f2PLqj50BRLKKCZjZiCTpdnHFVN-IBkaVPIkFLVE/edit?usp=sharing)

- [Week 1](WeeklySchedule.md#week-1) – Introduction / NIME, Music Devices, and Sound Installations
- [Week 2](WeeklySchedule.md#week-2) – Applied music theory, Western and beyond
- [Week 3](WeeklySchedule.md#week-3) – CircuitPython / Physical computing for NIME
- [Week 4](WeeklySchedule.md#week-4) – Musical interface design, MIDI
- [Week 5](WeeklySchedule.md#week-5) – Musical sensors
- [Week 6](WeeklySchedule.md#week-6) – Rapid prototyping
- [Week 7](WeeklySchedule.md#week-7) – Inspiration day / 3D Printing Workshop
- SPRING BREAK
- [Week 8](#week-8) – Idea Lab / Project proposal development
- [Week 9](#week-9) – Project proposal presentation, implementation starts!
- [Week 10](#week-10) – Telling your story / documenting your work
- [Week 11](#week-11) – Guest Speaker, project production
- [Week 12](#week-12) – Music performance, project feedback, user testing
- [Week 13](#week-13) – Final project production / polish
- [Week 14](#week-14) – Final project presentations
- [IM SHOW](#im-show) Friday May 8 – Show final project / Update final documentation

Note: Exact due dates for assignments and readings are indicated in Brightspace

# Week 8

## Week 8.1
Announcements
- Check-in
- Classes online
  - Timezones
  - Cameras
  - Recordings
- Midterm
- Rest of semester

## Homework - Week 8.1
- *Record* five sounds from your environment

- *Download* and try Fusion

- *Work* on your Midterm project. The midterm is due Monday March 30 _before_ class

<!--
**Think** of a project idea

**Post** your idea to the [Brightspace Discussions -> Individual Exercises -> Initial Project Idea](https://brightspace.nyu.edu/d2l/le/435258/discussions/topics/538217/View)

**Be ready** to discuss your idea in the next class
-->

## Week 8.2
Announcements
- Let me know when there's a sound issue (now on Ethernet)

3D printing example

Sampling with Ableton Live demo

Midterm progress feedback

Zoom sound sharing test
- Enable sound when sharing screen, can try "Stereo (high-fidelity)"
- Check that Ableton is using Zoom sound device
<img width="649" height="638" alt="Screenshot 2026-03-25 at 7 36 09 AM" src="https://github.com/user-attachments/assets/55d8c2a9-e151-4523-b650-b72eae6b7cb6" />
<img width="560" height="615" alt="Screenshot 2026-03-25 at 7 34 07 AM" src="https://github.com/user-attachments/assets/0f997562-9599-4ac8-80c2-8a37bfaed1f4" />




### Homework - Week 8.2

Due before start of next class
*Complete* your midterm assignment and submit it via Brightspace->Discussions

---

# Week 9

## Week 9.1
Midterm sharing

Tips on using AI
- When generating code, generate small functions that do one thing
- Don't just accept the generated code - make sure it works!
- Generate a function that you can use to test the generated code
- You can test pure Python functions using the built in python interpreter on your laptop or in an IDE
- Credit the generated code in your source code with a link to the conversation with AI

Improving latency in CircuitPython
- Our python code typically executes synchronously, line by line
- Avoid functions that take a long time, such as serial prints
- Make your serial debugging conditional on a variable so they're easy to turn on for debugging, and off for speed

Example
```
serial_debug = True # on for debugging
#serial_debug = False # off for speed

while True:
  if serial_debug:
    print("This will slow things down")

  do_something()
```

Using multiple instruments in Ableton
- Refer to today's Zoom recording for details
- Ableton Live set [Week 9 - Multiple instruments](https://github.com/mangtronix/MusicDevices/tree/main/Ableton/Week%209%20-%20Multiple%20instruments%20Project)

<!--
- Debouncing buttons
    - Often want to react to **changes** in button state rather than whether button is currently pressed
    - Can keep previous state of button and compare to current state to react to transitions 
    - [CircuitPython debouncer library](https://learn.adafruit.com/debouncer-library-python-circuitpython-buttons-sensors/basic-debouncing)
-->

### Week 9.1 Homework
3D Design with Tinkercad
- Sign up for [Tinkercad](https://www.tinkercad.com/)
- Join the Music Devices S2026 classroom - check your email or Brightspace->Announcements for the link
- Complete the tutorials in the "Tutorials" activivity (Let's Learn Tinkercad, Introduction to Primitive Shapes, Creating Holes, Monogrammed Ring)
- Your progress in the tutorials is tracked through Tinkercad Classrooms. Make sure to complete the final tutorial of making a custom ring
<img width="1332" height="391" alt="Screenshot 2026-03-30 at 3 52 56 PM" src="https://github.com/user-attachments/assets/76d60112-d98d-48b8-a014-0918eab1e298" />




## Week 9.2

Introduce Final Project

3D Design workshop
- [Design custom 3D printed parts (YouTube)](https://youtu.be/ub5NFpyP8wk?si=j-Nbh7sWbeWTdjs0)
  
### Homework - Week 9.2

Due before start of next class
- **Complete** 3D design exercise
  - Progress is automatically tracked in Tinkercad classroom, no separate submission
- **Prepare** a project idea


---

# Week 10

## Week 10.1
Announcements
- Class materials stipend of $120 will be loaded to your FAB cards
- Should be credited April 15
- Can be used to buy electronic components, small tools like soldering irons, 3D printing, laser cutting

3D Design / Printing


## Week 10.2

Discuss Final Project

3D Design / Printing

### Week 10.2 Homework

3D Design

Final Project Idea

# Week 11

## Week 11.1
- Review homework


### Idea Lab
Round Table of Project Ideas

Project concept development
- What type of expression does your project enable? How does this relate to existing musical practices?
- Who is the intended user / community for your device? Are they underserved by currently available devices? How does your design serve those users?
- How does your project extend what's been done before? How does your project use the technology we've learned to enhance musical expression?
- What is your creative vision for your device? What is your dream performance / installation / application?

Project lifecycle
- How to create a project proposal
- Creating a production plan
- Project production
- User testing
- Presentations
- Documentation


- Review implementation plans
- Update week-by-week plans
- What is the most challenging part of your project?
- What can you do next class to resolve your greatest challenge?
  
Telling your story / Documenting your work / Performance / Exhibition installation
- What's the story of your project?
- Refining your concept / story in advance helps to focus your project
- Documenting your work
    - Hero image - one image that tells whole story of your project
    - Short video
    - One paragraph description
    - One paragraph background
    - 3-4 other photos
 - Video storyboards
    - Tell the story of your video with one comic-style panel per shot
    - Used to communicate with production team while shooting video
    - Storyboard is chronological (follows story arc)
        - Shot list is list of all shots, which are usually filmed out of order
    - [Storyboarding (Comm Lab)](https://owenroberts.github.io/commlab/video-storyboards.html)
- Presenting final project
    - Performance
    - Installation
    - IM End of Semester Show
        - Everyone must participate
     
- Productizing
    - Many boutique MIDI controllers exist for sale
    - [Etsy](https://www.etsy.com/)
        - Small shop equivalent to Ebay / Amazon
        - Mostly small designers
        - [Etsy->Midi controllers (Etsy)](https://www.etsy.com/market/midi_controller)
    - [Kickstarter](https://www.kickstarter.com/)
        - [Kickstarter MIDI controller projects (Kickstarter)](https://www.kickstarter.com/discover/advanced?ref=nav_search&term=midi%20controller)
        - [Chorda (Kickstarter)](https://www.kickstarter.com/projects/artiphon/chorda-a-musical-instrument-for-everyday-life)
            - By an established company with professional promotion
        - Typically horror story is you underestimate the cost and project is successfully funded
            - Imagine you pre-sell 1,000 at $150 / unit and eventually it costs you one year of work and $200 / unit to produce
    - Notable commercial controllers
        - [Yaeltex](https://yaeltex.com/)
            - Design your own MIDI controller and have fabricated
            - User designs give insight into what people can't find elsewhere
        - [Midi Fighters (DJ Techtools)](https://store.djtechtools.com/collections/midi-fighters-midi-fighter-accessories)
            - All buttons or all knobs

 ### Homework

Due before start of next class

- **Update** your project implementation plan
- **Make** a plan for your in-class production next class

- **Work** on your implementation plan
    - Identify most difficult / uncertain parts of project
    - What technologies you will use
- **Find** example music that matches what you are trying to create
- **Post** a link to your implementation plan and music examples on [Brightspace Discussion](https://brightspace.nyu.edu/d2l/le/435258/discussions/topics/538992/View)


## Week 10.2

Project proposal work session and feedback
- Individual group consultations on project proposal and implementation plan
- Group work session for project proposal

Project proposal presentations
- Each group get 7 minutes to present
- Feedback from class and professor
- Collect technical topics from proposed projects
- 
Project production
- Work towards resolving your largest challenge

Project-related resources
- [Photocells (Adafruit)](https://learn.adafruit.com/photocells/circuitpython)
- [Stepper + DC Motor Featherwing](https://learn.adafruit.com/adafruit-stepper-dc-motor-featherwing/overview)
- Search for 12V in the IM equipment checkout for 12V power supplies suitable for using with the 12V stepper motors
    - e.g. [12V 2A power supply](https://nyuad-artsbooking.nyu.edu/wizard/resourcedetail.aspx?id=14163), [12V 3.5A power supply](https://nyuad-artsbooking.nyu.edu/wizard/resourcedetail.aspx?id=17032)

Capacitive touch
- [Capacitive Touch on ESP32-S3 Reverse TFT](https://learn.adafruit.com/esp32-s3-reverse-tft-feather/capacitive-touch)
- [12-Key Cap Touch Sensor QT board](https://learn.adafruit.com/adafruit-mpr121-12-key-capacitive-touch-sensor-breakout-tutorial)
- [Tutorial for built-in touch inputs on M4 CircuitPython board](https://desert.nyuadim.com/2022/04/07/tutorial-for-touch-on-m4-express/)
    - Note use of 1 megaohm pulldown resistor
- Try printing the [raw_value](https://docs.circuitpython.org/en/latest/shared-bindings/touchio/#touchio.TouchIn.raw_value) to see how the value changes in different conditions


### Homework - Week 10.2
#### Due Monday April 14 - 12pm

- **Post** your group progress report to [Brightspace->Discussions->Group Projects->Project Progress](https://brightspace.nyu.edu/d2l/le/435258/discussions/topics/540524/View)
 
- **Read** [Live Performance in the Age of Supercomputing
 (Robert Henke)](https://roberthenke.com/interviews/supercomputing.html)
    - What, to you, makes for a good live performance of electronic music?
    - How will you connect with your music and your audience?
- **Post** your individual response to [Brightspace->Discussions->Readings->Reading 3](https://brightspace.nyu.edu/d2l/le/435258/discussions/topics/540526/View)

---

# Week 11

## Week 11.1
## Meet in IM Lab from now on
Musical inspiration
- [FKJ: Tiny Desk (Home) Concert (YouTube)](https://www.youtube.com/watch?v=PwV1-wZzT1Y)
    - Live looping using Ableton Live and Akai APC40 controller

Plan for today
- Discuss reading
- Review project progress
- Plan for IM End of Semester show
- Discuss User Testing / Progress Demo

- IM End of Semester show
    - Collect project requirements
    - Table or pedestal? What size?
    - Performance, installation, or demo?
    - TV / monitor display?
        - A few large TVs are available (ask now)
    - Equipment available from IM Lab should be booked in Connect2
        - Small speakers
        - Laptops
        - Sensor boards
        - Monitors
    - Make floor plan

Music performance and documentation
- [Hands-On: Foundations of Live Electronic Music Performance (Roland)](https://articles.roland.com/hands-on-foundations-of-live-electronic-music-performance/)
- [Jeff Mills Exhibitionist Mix 3 with Roland TR-909
 (YouTube)](https://www.youtube.com/watch?v=sLtnbR9H48I)
- Demonstrating your device
    - What's your story?
    - How does the audience understand what your device does?
    - What gestures do you need to show?
    - [Guthman Musical Instrument Competition](https://guthman.gatech.edu/) has many good demo videos
        - [Ten Instruments That Will Change How You Think About Music
 (Georgia Tech)](https://guthman.gatech.edu/feature/guthman-instruments-change-music)



User experience design
- What types of users are you designing for? What are their "personas"?
    - [Persona (Wikipedia)](https://en.wikipedia.org/wiki/Persona_(user_experience))
    - [Types of Personas in User Experience Design (Medium)](https://medium.com/@hazlazuardi/types-of-personas-in-user-experience-design-81bedc4aa261)
    - Are you designing for a musician? A rapper? The general public?
    - How does your design meet the needs / desires of your users?

User testing
- [The complete guide to usability testing (UserTesting)](https://www.usertesting.com/resources/guides/usability-testing)
- [Usability Testing 101
 (NN/g)](https://www.nngroup.com/articles/usability-testing-101/)
- Identify areas of your design that you want to test
- Have user try to complete a set of tasks with minimal prompting
- Record user interaction
- Ask users questions after the test
- Identify areas where users were confused
- Collect qualitative experience of users
- Analyze results and write summary
- Make plan for resolving pain points and improving user experience

### Homework

Due before start of next class
- **Revise** your project concept and implementation plan

## Week 11.2
Musical Inspiration
- [Laurie Spiegel interview offers a way of thinking about community, imagination (CDM)](https://cdm.link/laurie-spiegel-interview-offers-a-way-of-thinking-about-community-imagination/)
- [Laurie Spiegel (Wikipedia)](https://en.wikipedia.org/wiki/Laurie_Spiegel)
- Voyager Golden Record
    - [Golden Record (Wikipedia)](https://en.wikipedia.org/wiki/Voyager_Golden_Record)
    - [Carl Sagan on the Voyager Golden record (YouTube)](https://www.youtube.com/watch?v=iVysAQVPCAY)
    - [goldenrecord.org](https://goldenrecord.org/)
    - [Where are Voyager 1 and Voyager 2 Now? (NASA)](https://science.nasa.gov/mission/voyager/where-are-voyager-1-and-voyager-2-now/)
    - [The Voyager Golden Record: A reminder that we are all connected (United Nations)](https://www.youtube.com/watch?v=l5BG5nGmGFQ)

Web MIDI
- [About Web MIDI (midi.org)](https://midi.org/about-web-midi)
- [Web MIDI API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/Web_MIDI_API)
- [WEBMIDI.js](https://webmidijs.org/)
  - JavaScript library for accessing MIDI
  - Examples
    - [Raaga](https://raaga.riteshkr.com/)
    - [Chromatone](https://chromatone.center/)
- Example sketches
  - [midi tester (editor.p5js.org)](https://editor.p5js.org/sandpills/sketches/ckEr2thWV)
  - [p5js_webmidi](https://github.com/FSUdigitalmedia/p5js_webmidi)

Using Web MIDI with p5.js
- [midi tester (p5 sketch)](https://editor.p5js.org/mangtronix/sketches/ZiNpPVMyM)
  - Shows and plays notes sent from MIDI controller
  - Uses browser MIDI functionality directly


Workshop: Project production
- Share your project progress
- Get feedback from other groups
- Individual consultations with each group
- 

Project topics
- Fusion
    - [Making tapped holes](https://help.autodesk.com/view/fusion360/ENU/?guid=SLD-HOLE-THREAD) 
- Soldering
    - [Adafruit Guide to Soldering](https://learn.adafruit.com/adafruit-guide-excellent-soldering)  
    - [Picture of good / bad solder joints](https://learn.adafruit.com/adafruit-guide-excellent-soldering/common-problems)
- NeoPixels
    - [NeoPixel Uberguide](https://learn.adafruit.com/adafruit-neopixel-uberguide/the-magic-of-neopixels)
    - [Powering NeoPixels](https://learn.adafruit.com/adafruit-neopixel-uberguide/powering-neopixels)
- Battery power
    - [ESP32 Reverse TFT Power Management](https://learn.adafruit.com/esp32-s3-reverse-tft-feather/power-management)     

### Homework - Week 11.2

Due before start of next class

<!--
- **Conduct user testing** of your project
    - Test your project with multiple users
- **Post** the results of your user testing
    - See [Syllabus->Project User Test](https://docs.google.com/document/d/1NaQrfuxLaoMKMixZ_BOIEzCix7Gx2jokPu_qFPAmvVw/edit#heading=h.nptms79n6zl8) for details
-->

# Week 12

## Week 12.1
Project check-in
- What did you get working?
- What do you still need to do?

Project Production

## Week 12.2

### Production Mode - GO!


IM End of Semester Show preparation
- Space allocations
- Technical needs

### Homework
Conduct your user testing
- Post your results to [Brightspace->Discussions->Project User Test](https://brightspace.nyu.edu/d2l/le/435258/discussions/topics/541989/View)

Prepare to share your results and show your working project in class on Monday

---

# Week 13

## Week 13.1
Share user testing results
Final project dress rehearsal
- Present your project at 95% completion
- Does your project feel right?
- Once your project technical implementation is complete (feature complete) there is much work to be done to dial in the feel / experience 
- We will identify areas for "final polish" / tweaking that will make the most impact on the user experience

## Week 13.2
Announcements
- **Book** any equipment needed, e.g. speakers, now [Arts Booking](https://nyuad-artsbooking.nyu.edu/)
- You're responsible for getting the equipment from the IM Lab and returning it immediately after the show
- 
Workshop: Final project production
- Set up project directories in MusicDevices GitHub
    - e.g. [https://github.com/mangtronix/MusicDevices/tree/main/Projects/TickTune](https://github.com/mangtronix/MusicDevices/tree/main/Projects/TickTune)
- Final push to bring projects to being not just "done" but having an excellent user experience

Class references
- Changing bpm in Ableton Live
    - By changing scenes - [Learn Live: Automating Tempo Changes (YouTube)](https://www.youtube.com/watch?v=iI06kTUtNDg)
- [ESP32-S3 Reverse TFT Feather Power Management](https://learn.adafruit.com/esp32-s3-reverse-tft-feather/power-management)
    - How to use a battery with the Feather
    - Wire a switch between EN and GND to turn off power but still allow charging
- Exporting a Fusion sketch to DXF for lasercutting
    - Create a sketch with just the shapes you want to cut
    - [Export your sketch as DXF](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/How-to-Save-Sketch-as-DXF-in-Fusion-360.html)
    - Book lasercutter on Connect2
    - Bring DXF file to appointment with lab assistant
    - Lab assistant will load DXF file into Adobe Illustrator and cut your material
    - Recommend to do a test cut in cardboard to verify dimensions etc are correct (it's very fast to cut cardboard) before cutting in the final material

### Homework - Week 13.2

Due before start of next class

- **Start** your public project page on the class website with your project documentation
    - See [Syllabus->Project Documentation](https://docs.google.com/document/d/1NaQrfuxLaoMKMixZ_BOIEzCix7Gx2jokPu_qFPAmvVw/edit#heading=h.vksuuzysxkk4) for details
    - Your project page does not need to be 100% complete but should include the project description and a representative image
    - This is the *public facing* project page that will be shared externally
        - Your "behind the scenes" technical documentation will be a separate post
    - You can create the photos / videos now or at the IM End of Semester Show
    - Your project page should be suitable for public viewing as a "teaser" / promo for the End of Semester Show
    - Your project page will have a static URL that you can use to promote your project (e.g. print postcards, email NYUAD community)
---

# Week 14

## Week 14.1
- Project check-in
- Course review
- Review final timeline / deliverables
    - Project documentation
    - Project web page / video
    - Show setup
    - Show
- Resolve final project issues

- Class resources
    - [How to Transfer Ableton Projects Between Computers](https://www.soundalgorithm.io/ableton-guides/how-to-transfer-ableton-projects-between-computers/)

### Homework

Due before start of next class

- **Finish** your project
- **Be ready** to set up your project in class on Wednesday including having all the equipment ready that you need

## Week 14.2
Show setup - **come directly to the Black Box at 3:35pm for setup**
- Bring everything you need, including speakers, etc
- **You have 30 minutes to set up** then everyone must stop for the presentations
- Can start setting up at 3:00pm

In-class project presentations
- Presentations start at 4:15pm
- Each group get 15 minutes to show their work and take questions

---
# IM End of Semester Show
- Each group must show their project
- Come to Black Box and have project running at 4:45pm
- Show time is 5-7pm in Black Box

### Homework - Final Documentation
- **Submission due Wednesday May 13 (no extension possible)**
- **Post** your project documentation to the class website in your project directory in [MusicDevices/Projects](https://github.com/mangtronix/MusicDevices/tree/main/Projects)
    - See [Syllabus->Final Project](https://docs.google.com/document/d/1NaQrfuxLaoMKMixZ_BOIEzCix7Gx2jokPu_qFPAmvVw/edit#heading=h.2noy7dxf6pp6) and [Syllabus->Project Web Page / Video](https://docs.google.com/document/d/1NaQrfuxLaoMKMixZ_BOIEzCix7Gx2jokPu_qFPAmvVw/edit#heading=h.vksuuzysxkk4) for details


# Congratulations, you've made a musical device!
