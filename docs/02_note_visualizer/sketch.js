// 02 -- Note Visualizer
//
// Listens for MIDI note-on messages and spawns a coloured expanding ripple
// for each note, with velocity controlling the ring's size and speed. Notes
// are registered dynamically on first arrival -- each pitch class gets its
// own hue around the colour wheel, and positions are assigned by pitch rank
// so any controller (four buttons or a full keyboard) gets a clean layout
// with no hard-coded mapping.
//
// Written with Claude by Michael Ang for Music Devices (IM-UH 3116, NYU Abu Dhabi).
// More info: https://mangtronix.github.io/MusicDevices/p5examples.html#02-note-visualizer

// --- Shared MIDI state (written by WebMIDI, read by p5) ----------------------
const midi = {
  activeNotes: new Set(),   // set of currently held note numbers
  seenNotes:   {},          // { noteNumber: { color } } -- filled in as notes arrive
  ripples:     [],          // expanding ring animations
  deviceName:  'no device',
};

// Persistent "glow" layer on a graphics buffer so old ripples leave trails
let bg;

// --- Note registration -------------------------------------------------------
// Nothing is pre-configured. Each incoming note gets registered on its first
// NoteOn and assigned a color based on its pitch class. Positions are computed
// at draw time by sorting all seen notes by pitch so they spread evenly.

function registerNote(note) {
  if (midi.seenNotes[note]) return;
  // Hue = 12 evenly-spaced steps around the color wheel per octave
  const hue = ((note % 12) * 30 + 200) % 360;
  midi.seenNotes[note] = { color: hsvToRgb(hue, 0.75, 1.0) };
}

function sortedSeenNotes() {
  return Object.keys(midi.seenNotes).map(Number).sort((a, b) => a - b);
}

// x fraction (0-1) for a note, based on its rank among all seen notes
function noteXFrac(note) {
  const sorted = sortedSeenNotes();
  const i = sorted.indexOf(note);
  return (i + 1) / (sorted.length + 1);
}

// MIDI note number -> standard name with octave ("C4", "F#5", ...)
function noteName(n) {
  const names = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'];
  return names[n % 12] + (Math.floor(n / 12) - 1);
}

// HSV (h: 0-360, s/v: 0-1) -> [r, g, b] in 0-255
function hsvToRgb(h, s, v) {
  const c = v * s;
  const x = c * (1 - Math.abs(((h / 60) % 2) - 1));
  const m = v - c;
  let r, g, b;
  if      (h <  60) [r, g, b] = [c, x, 0];
  else if (h < 120) [r, g, b] = [x, c, 0];
  else if (h < 180) [r, g, b] = [0, c, x];
  else if (h < 240) [r, g, b] = [0, x, c];
  else if (h < 300) [r, g, b] = [x, 0, c];
  else              [r, g, b] = [c, 0, x];
  return [(r + m) * 255, (g + m) * 255, (b + m) * 255];
}

// --- WebMIDI setup -----------------------------------------------------------
WebMidi.enable()
  .then(() => {
    function attachInput(input) {
      midi.deviceName = input.name;
      document.getElementById('device-name').textContent = input.name;
      document.getElementById('device-name').classList.remove('none');

      input.addListener('noteon', e => {
        const note = e.note.number;
        const vel  = e.rawVelocity;   // 0-127

        registerNote(note);           // first time we see this note, give it a color
        midi.activeNotes.add(note);

        // Queue a ripple for p5 to draw
        midi.ripples.push({
          note,
          xFrac:  noteXFrac(note),
          color:  midi.seenNotes[note].color,
          radius: 0,
          maxR:   map(vel, 0, 127, 80, 260),  // velocity -> size
          alpha:  255,
          speed:  map(vel, 0, 127, 2, 5),     // velocity -> speed
        });
      });

      input.addListener('noteoff', e => {
        midi.activeNotes.delete(e.note.number);
      });
    }

    WebMidi.inputs.forEach(attachInput);

    WebMidi.addListener('connected', e => {
      if (e.port.type === 'input') attachInput(e.port);
    });

    WebMidi.addListener('disconnected', e => {
      if (midi.deviceName === e.port.name) {
        midi.deviceName = 'no device';
        document.getElementById('device-name').textContent = 'no device';
        document.getElementById('device-name').classList.add('none');
      }
    });
  })
  .catch(err => {
    document.getElementById('device-name').textContent = 'MIDI denied';
    console.error(err);
  });

// --- p5.js sketch (global mode) ----------------------------------------------

function setup() {
  createCanvas(windowWidth, windowHeight);
  colorMode(RGB, 255, 255, 255, 255);

  bg = createGraphics(width, height);
  bg.background(10, 10, 18);
}

function draw() {
  // Slowly fade the background layer -- creates the trail effect
  bg.noStroke();
  bg.fill(10, 10, 18, 18);       // low alpha = long trail
  bg.rect(0, 0, width, height);

  // Draw background layer onto canvas
  image(bg, 0, 0);

  // -- Ripples --------------------------------------------------------------
  for (const r of midi.ripples) {
    r.radius += r.speed;
    r.alpha  -= 255 / (r.maxR / r.speed);   // fade as it expands

    const x = r.xFrac * width;
    const y = height * 0.5;

    // Outer ring
    noFill();
    stroke(r.color[0], r.color[1], r.color[2], Math.max(0, r.alpha));
    strokeWeight(2.5);
    circle(x, y, r.radius * 2);

    // Inner softer ring
    stroke(r.color[0], r.color[1], r.color[2], Math.max(0, r.alpha * 0.4));
    strokeWeight(6);
    circle(x, y, r.radius * 1.6);

    // Also paint onto the persistent bg layer (dimly) for the glow trail
    bg.noFill();
    bg.stroke(r.color[0], r.color[1], r.color[2], Math.max(0, r.alpha * 0.12));
    bg.strokeWeight(3);
    bg.circle(x, y, r.radius * 2);
  }

  // Remove fully faded ripples
  midi.ripples = midi.ripples.filter(r => r.alpha > 0);

  // -- Button indicators at bottom (only for notes we've seen) --------------
  const sorted = sortedSeenNotes();
  if (sorted.length === 0) {
    drawHint();
  } else {
    drawButtonRow(sorted);
  }
}

function drawHint() {
  noStroke();
  fill(80, 80, 110, 200);
  textFont('Courier New');
  textAlign(CENTER, CENTER);
  textSize(14);
  text('press a key on your controller', width / 2, height / 2);
}

function drawButtonRow(sorted) {
  const y      = height - 80;
  const dotR   = 16;
  const labelY = y + 40;

  for (let i = 0; i < sorted.length; i++) {
    const note      = sorted[i];
    const cfg       = midi.seenNotes[note];
    const x         = ((i + 1) / (sorted.length + 1)) * width;
    const active    = midi.activeNotes.has(note);
    const [r, g, b] = cfg.color;

    // Ring
    noFill();
    stroke(r, g, b, active ? 200 : 50);
    strokeWeight(active ? 2 : 1);
    circle(x, y, dotR * 2);

    // Fill when active
    if (active) {
      fill(r, g, b, 180);
      noStroke();
      circle(x, y, dotR * 2);
    }

    // Label: note name on top line, MIDI number below in a dimmer color
    noStroke();
    textFont('Courier New');
    textAlign(CENTER, CENTER);

    fill(r, g, b, active ? 240 : 150);
    textStyle(BOLD);
    textSize(20);
    text(noteName(note), x, labelY);

    fill(r, g, b, active ? 190 : 110);
    textStyle(NORMAL);
    textSize(14);
    text(note, x, labelY + 22);
  }
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
  bg.resizeCanvas(width, height);
  bg.background(10, 10, 18);
}
