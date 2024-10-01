# Ableton Tuning with VSTs and external synths

- Right-click device and "Enable MPE"
    - Only works with MPE-enabled VSTs
    - Individual notes are preceded by pitch bend messages
    - VST pitch bend range must be set to 48 semitones (+/- 2 octaves)
- Using Ableton tuning with MPE-enabled hardware synths
    - Use External Instrument device and select MPE as the output MIDI channel
    - See [MPE/Multi-channel Settings (Ableton)](https://www.ableton.com/en/live-manual/11/editing-mpe/#mpe-in-external-plug-ins)
    - synthesizer pitch bend range must be set to 48 semitones (+/- 2 octaves)


Example log sending from Ableton to Protokol with tuning and MPE enabled. Note ```PITCHBEND``` sent before each ```NOTE_ON``` so that each note is played at the desired pitch. A value of 8192 corresponds to 
```
14:29:14.817 | RECEIVE    | ENDPOINT(Protokol) TYPE(PITCHBEND) CHANNEL(12) DATA(8260)
14:29:14.817 | RECEIVE    | ENDPOINT(Protokol) TYPE(NOTE_ON) CHANNEL(12) DATA1(39) DATA2(62)
14:29:15.262 | RECEIVE    | ENDPOINT(Protokol) TYPE(PITCHBEND) CHANNEL(13) DATA(8192)
14:29:15.262 | RECEIVE    | ENDPOINT(Protokol) TYPE(NOTE_ON) CHANNEL(13) DATA1(43) DATA2(46)
14:29:15.672 | RECEIVE    | ENDPOINT(Protokol) TYPE(PITCHBEND) CHANNEL(14) DATA(8354)
14:29:15.672 | RECEIVE    | ENDPOINT(Protokol) TYPE(NOTE_ON) CHANNEL(14) DATA1(45) DATA2(86)
14:29:16.081 | RECEIVE    | ENDPOINT(Protokol) TYPE(PITCHBEND) CHANNEL(4) DATA(8192)
14:29:16.081 | RECEIVE    | ENDPOINT(Protokol) TYPE(NOTE_ON) CHANNEL(4) DATA1(48) DATA2(36)
14:29:16.487 | RECEIVE    | ENDPOINT(Protokol) TYPE(PITCHBEND) CHANNEL(6) DATA(8260)
14:29:16.487 | RECEIVE    | ENDPOINT(Protokol) TYPE(NOTE_ON) CHANNEL(6) DATA1(51) DATA2(29)
```

### Example of using Ableton tuning with popular [Repro-5](https://u-he.com/products/repro/) VST synthesizer

![Repro-5 manual for pitch bend](../Media/Repro_Manual_Pitchbend.png?raw=true "Repro-5 manual pitch bend")
Pitch bend information from [Repro-5 user guide](https://uhe-dl.b-cdn.net/manuals/plugins/repro/Repro-5-user-guide.pdf)

![Repro-5 tweaks page](../Media/Repro_Pitchbend_Tweak.png?raw=true "Repro-5 tweaks page")
Repro-5 pitch bend setting

![VST with custom tuning](../Media/Repro_Tuning.png?raw=true "VST with custom tuning")
Overall Live setup - VST with Ableton tuning - playing "E" on MIDI controller
