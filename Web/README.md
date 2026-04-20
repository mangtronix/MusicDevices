# WebMIDI + p5.js Examples — How They Were Made

Class notes for IM-UH 3116 (Music Devices, NYUAD). This is a high-level tour
of the techniques each example uses — so you can pick the right one to start
from when you build your own. The landing page (`index.html`) covers the
shared setup and tips on using AI to generate similar projects.

---

## 01 — MIDI Monitor

A debugging tool. Lists every connected device and logs every incoming
message in real time.

### Techniques

- **Listen broadly.** Subscribes to named events (note on/off, control
  change, pitch bend) *and* a catch-all that fires on every raw MIDI byte —
  so messages the library doesn't have a convenience event for still show up.
- **Cap the log.** The message list is trimmed to the most recent 200 entries
  so a long session doesn't slow the page down.
- **Colour-coded types.** Notes, CCs, and everything else each get their own
  colour — so at a glance you can see which kinds of messages your controller
  is actually sending.
- **Filter dropdown.** Narrow the view to one message type when you're
  hunting a specific bug.

### Why start here

Before you build any visualiser, you need to see what your controller is
actually sending. Half the bugs in a later example are really surprises in
the MIDI stream — a duplicated note-on, a CC on channel 2 when you expected
channel 1. This page is your oscilloscope.

---

## 02 — Note Visualizer

Press keys, get ripples. Starts blank and learns notes as they arrive.

### Techniques

- **Dynamic registration.** No pre-configured mapping of note to colour or
  screen position. The first time a note is received, it's given a hue and a
  slot on the screen.
- **Pitch-based colour.** Each pitch class (C, C#, D, …) gets its own hue,
  rotating around the colour wheel by semitone. Two notes an octave apart
  share a colour; neighbouring notes look similar.
- **Layout computed at draw time.** The currently-seen notes are sorted by
  pitch and spread evenly across the canvas every frame. A 3-note song and a
  12-note song both get a clean layout with no hard-coded positions.
- **Velocity-scaled ripples.** A harder hit produces a larger, longer-lived
  ring. Velocity is free expressive data — use it.
- **Readable labels.** Note name in bold and MIDI number underneath, large
  enough to read from across the room.

### Why this shape

The temptation with a "four-button visualiser" is to hard-code four
positions. Resist it. If the same code handles 1 note or 20 with no config,
you can reuse it with a keyboard, a drum pad, or a wind controller — whatever
happens to be plugged in.

---

## 03 — CC Visualizer

Auto-detects every CC that arrives. Shows a live dial plus a scrolling
waveform for the most recent one, and a grid of all CCs ever seen with their
current values.

### Techniques

- **Keyed by channel + CC number.** Channel 1 CC 74 and channel 2 CC 74 are
  tracked as separate streams, since they often come from different
  controllers or different knobs.
- **Named CCs.** A small lookup table turns the raw number into a friendly
  label — CC 74 becomes "Filter Cutoff", CC 1 becomes "Mod Wheel", and so on.
  Unknown numbers just show as "CC 42".
- **Two views of the same data.** The dial is the instantaneous value
  ("where is it now?"); the waveform is history ("how has it been moving?").
  Each answers a different question, so both earn their place on screen.
- **Grid of live chips.** Every CC ever received is kept as a small card with
  an in-place value bar. Wiggle three knobs and you see three bars update
  simultaneously — no "select which one to watch" dropdown.

### Why it works this way

Controllers rarely send a single CC. A synth knob bank, a mod wheel, a foot
pedal, and a breath controller all at once is normal. A visualiser that
assumes one-CC-at-a-time breaks the moment you plug in real gear. Build for
many from the start.

---

## 04 — Notes + CC (particles)

A particle system where notes spawn coloured bursts and a CC controls
gravity. The most elaborate of the four — combines notes, CC, p5 physics,
Web Audio synthesis, and particle-to-particle interaction.

### Techniques

- **Gravity from CC.** The continuous CC value is mapped to a gravity value
  that goes from strongly negative (float upward) through zero (weightless)
  to positive (fall). One knob, the whole behaviour range.
- **Chromatically tuned explosion sounds.** Every note press fires a short
  synthesised burst whose pitch matches the MIDI note. The sound is built
  from three stacked layers — a pitched "thump" that drops in frequency, a
  sub-octave body, and filtered noise for sparkle. All three fade together.
- **Particle interactions between different notes.** Particles from the same
  note ignore each other. Particles from *different* notes push apart at
  close range and pull together at medium range, which creates swirling
  orbits when multiple notes are held.
- **Connection sparks.** When particles from different notes get very close,
  a short glowing arc is drawn between them — the system "notices" that the
  clouds are interacting, and the interaction becomes visible.
- **Fast enough at N particles.** With many particles on screen, checking
  every pair against every other pair gets very slow. The example uses a
  spatial grid to only check nearby neighbours, which keeps the frame rate
  smooth even with hundreds of particles.

### Matching CircuitPython

The accompanying CircuitPython controller (`../CircuitPython/midi_particles.py`)
sends the same notes (E minor pentatonic) and the same CC number that this
page expects. Button and sprite colours on the hardware mirror the
on-screen particle hues, so the physical device and the web visualiser feel
like the same instrument.

---

For building your own: pick the example closest to your idea, copy it, and
modify your way to the new thing. The full cycle — idea to running page — is
usually an evening's work if you keep steps small and test often.
