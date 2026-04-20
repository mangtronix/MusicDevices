# WebMIDI + p5.js Examples

Class examples for IM-UH 3116 (Music Devices, NYUAD).

Open `index.html` (served over HTTP — see instructions there) for the full
landing page, which includes setup instructions, per-example descriptions with
expandable technique notes, and tips on using AI to generate similar projects.

## Quick start

```
cd docs && python3 -m http.server 8000
```

Then open http://localhost:8000 in Chrome or Edge.

## Files

| File | Description |
|------|-------------|
| `index.html` | Main Music Devices landing page |
| `p5examples.html` | WebMIDI + p5.js examples index |
| `01_midi_monitor.html` | Live log of all incoming MIDI messages |
| `02_note_visualizer.html` | Ripple visualizer — one ripple per note, auto-detected |
| `03_cc_visualizer.html` | Dial + waveform + grid for all incoming CC values |
| `04_notes_and_cc.html` | Particle system — notes spawn bursts, CC controls gravity |
