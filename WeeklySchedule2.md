# Class Notes - Weeks 8-14

[Weekly Overview / Dates (Spreadsheet)](https://docs.google.com/spreadsheets/d/14s9f2PLqj50BRLKKCZjZiCTpdnHFVN-IBkaVPIkFLVE/edit?usp=sharing)

- [Week 1](WeeklySchedule.md#week-1) – Introduction / NIME, Music Devices, and Sound Installations
- [Week 2](WeeklySchedule.md#week-2) – Applied music theory, Western and beyond
- [Week 3](WeeklySchedule.md#week-3) – CircuitPython / Physical computing for NIME
- [Week 4](WeeklySchedule.md#week-4) – Musical interface design, MIDI
- [Week 5](WeeklySchedule.md#week-5) – Musical sensors
- [Week 6](WeeklySchedule.md#week-6) – Rapid prototyping
- [Week 7](WeeklySchedule.md#week-7) – Inspiration day / 3D Printing Workshop
- 7-Week Finals Break
- [Week 8](#week-8) – Idea Lab / Project proposal development
- [Week 9](#week-9) – Project proposal presentation, implementation starts!
- SPRING BREAK
- [Week 10](#week-10) – Telling your story / documenting your work
- [Week 11](#week-11) – Guest Speaker, project production
- [Week 12](#week-12) – Music performance, project feedback, user testing
- [Week 13](#week-13) – Final project production / polish
- [Week 14](#week-14) – Final project presentations
- [IM SHOW](#im-show) – Show final project / Update final documentation

Note: Exact due dates for assignments and readings are indicated in Brightspace

# Week 8

## Week 8.1
Announcements
- Working on tutorials for generating sound directly on the CircuitPython board
    - [Basic tone demo on CircuitPython (MusicDevices GitHub)](https://github.com/mangtronix/MusicDevices/blob/main/Tutorials/Speaker_Hardware_Software.md)

String Thing Demo

## Homework - Week 8.1
**Think** of a project idea

**Post** your idea to the [Brightspace Discussions -> Individual Exercises -> Initial Project Idea](https://brightspace.nyu.edu/d2l/le/435258/discussions/topics/538217/View)

**Be ready** to discuss your idea in the next class


## Week 8.2
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


### Homework - Week 8.2

Due before start of next class

- **Form** groups of 2-4 students
- **Finish** your Project Proposal
    - See [Syllabus->Project Proposal](https://docs.google.com/document/d/1NaQrfuxLaoMKMixZ_BOIEzCix7Gx2jokPu_qFPAmvVw/edit#heading=h.disn06hi3v03) for details
- **Prepare** to present your Project Proposal in class
---

# Week 9

## Week 9.1
Project proposal work session and feedback
- Individual group consultations on project proposal and implementation plan
- Group work session for project proposal

## Week 9.2
Project proposal presentations
- Each group get 7 minutes to present
- Feedback from class and professor
- Collect technical topics from proposed projects

- Debouncing buttons
    - Often want to react to **changes** in button state rather than whether button is currently pressed
    - Can keep previous state of button and compare to current state to react to transitions 
    - [CircuitPython debouncer library](https://learn.adafruit.com/debouncer-library-python-circuitpython-buttons-sensors/basic-debouncing)

  
### Homework - Week 9.2

Due before start of next class

- **Work** on your implementation plan
    - Identify most difficult / uncertain parts of project
    - What technologies you will use
- **Find** example music that matches what you are trying to create
- **Post** a link to your implementation plan and music examples on [Brightspace Discussion](https://brightspace.nyu.edu/d2l/le/435258/discussions/topics/538992/View)
---
# SPRING BREAK / SPRING BREAK / SPRING BREAK #
---

# Week 10

## Week 10.1
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

## Week 10.2
## Meet in IM Lab
Announcements
- Prusa XL - need prior permission for prints that go into next day, can email Mang with .3mf export file from PrusaSlicer showing time and slicer options

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
Announcements
- [Magnesynth debut in Dubai Saturday](https://www.instagram.com/p/DIxnV0NJDhV/?img_index=1)


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
  
Workshop: Final project production
- Final push to bring projects to being not just "done" but having an excellent user experience

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
- Review project web pages
- Course review

### Homework

Due before start of next class

- **Finish** your project
- **Post** your "behind the scenes" project documentation to the class website
    - See [Syllabus->Final Project](https://docs.google.com/document/d/1NaQrfuxLaoMKMixZ_BOIEzCix7Gx2jokPu_qFPAmvVw/edit#heading=h.2noy7dxf6pp6) for details

## Week 14.2
In-class project presentations

IM End of Semester Show setup
- Space allocations
- Technical needs

---
# IM End of Semester Show
- Each group must show their project
- Setup time TBD
- Show time TBD

### Homework

- **Update** your project web page with the final video and photos
    - See [Syllabus->Project Web Page](https://docs.google.com/document/d/1NaQrfuxLaoMKMixZ_BOIEzCix7Gx2jokPu_qFPAmvVw/edit#heading=h.vksuuzysxkk4) for details

# Congratulations, you've made a musical device!
- Now go play it!
