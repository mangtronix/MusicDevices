// --- Shared MIDI state -------------------------------------------------------
// Written by WebMIDI listeners, read by the p5 draw loop.
const midi = {
  activeNotes: new Set(),    // notes currently held down
  seenNotes:   {},           // { note: { color:[r,g,b] } } -- registered on first NoteOn
  particles:   [],           // active particle objects
  ccData:      {},           // { "ch:cc": { channel, cc, value } }
  activeCcKey: null,         // most recently received CC
};

// Unicode glyphs expressed as escapes so this file stays ASCII-safe.
const SEP   = '\u00b7';   // middle dot
const UPDN  = '\u2195';   // up-down arrow

// --- Note helpers ------------------------------------------------------------
function registerNote(note) {
  if (midi.seenNotes[note]) return;
  const hue = ((note % 12) * 30 + 200) % 360;
  midi.seenNotes[note] = { color: hsvToRgb(hue, 0.8, 1.0) };
}

function sortedSeenNotes() {
  return Object.keys(midi.seenNotes).map(Number).sort((a, b) => a - b);
}

function noteXFrac(note) {
  const sorted = sortedSeenNotes();
  const i = sorted.indexOf(note);
  return (i + 1) / (sorted.length + 1);
}

function noteName(n) {
  return ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][n % 12] +
         (Math.floor(n / 12) - 1);
}

function hsvToRgb(h, s, v) {
  const c = v * s, x = c * (1 - Math.abs(((h / 60) % 2) - 1)), m = v - c;
  let r, g, b;
  if      (h <  60) [r,g,b] = [c,x,0];
  else if (h < 120) [r,g,b] = [x,c,0];
  else if (h < 180) [r,g,b] = [0,c,x];
  else if (h < 240) [r,g,b] = [0,x,c];
  else if (h < 300) [r,g,b] = [x,0,c];
  else              [r,g,b] = [c,0,x];
  return [(r+m)*255, (g+m)*255, (b+m)*255];
}

// --- CC helpers --------------------------------------------------------------
const CC_NAMES = {
  0:'Bank Select', 1:'Modulation', 2:'Breath', 4:'Foot Ctrl',
  7:'Volume', 10:'Pan', 11:'Expression', 64:'Sustain',
  71:'Resonance', 72:'Release', 73:'Attack', 74:'Filter Cutoff',
  91:'Reverb', 93:'Chorus',
};

function ccLabel(cc) { return CC_NAMES[cc] || ('CC ' + cc); }

// Gravity: active CC maps 0 -> float up, 64 -> weightless, 127 -> fall down
function gravityAccel() {
  if (!midi.activeCcKey) return 0.06;
  const val = midi.ccData[midi.activeCcKey].value;
  return (val / 127) * 0.65 - 0.30;
}

// --- Particle spawning (called from WebMIDI callbacks, outside p5) -----------
const MAX_PARTICLES = 400;

function spawnBurst(note, vel) {
  const cfg = midi.seenNotes[note];
  if (!cfg) return;
  const room  = MAX_PARTICLES - midi.particles.length;
  if (room <= 0) return;
  const x     = noteXFrac(note) * window.innerWidth;
  const y     = window.innerHeight * 0.65;
  const count = Math.min(Math.round(10 + (vel / 127) * 20), room);
  for (let i = 0; i < count; i++) spawnParticle(x, y, note, cfg.color, vel);
}

function spawnTrickle(note) {
  if (midi.particles.length >= MAX_PARTICLES) return;
  const cfg = midi.seenNotes[note];
  if (!cfg) return;
  const x = noteXFrac(note) * window.innerWidth;
  const y = window.innerHeight * 0.65;
  spawnParticle(x, y, note, cfg.color, 60);
}

function spawnParticle(x, y, note, color, vel) {
  const speed  = 1.5 + Math.random() * (3 + vel / 127 * 5);
  const angle  = -Math.PI * (0.15 + Math.random() * 0.70);
  const jitter = 20;
  midi.particles.push({
    x: x + (Math.random() - 0.5) * jitter,
    y: y + (Math.random() - 0.5) * jitter,
    vx: Math.cos(angle) * speed,
    vy: Math.sin(angle) * speed,
    r: clamp(color[0] + (Math.random() - 0.5) * 50),
    g: clamp(color[1] + (Math.random() - 0.5) * 50),
    b: clamp(color[2] + (Math.random() - 0.5) * 50),
    size: 2.5 + Math.random() * 3.5,
    life: 1.0,
    note,
  });
}

function clamp(v) { return Math.max(0, Math.min(255, v)); }

// --- Particle interactions ---------------------------------------------------
// Particles from DIFFERENT notes repel at close range and weakly attract at
// medium range. Same-note particles ignore each other. Spatial hash grid
// keeps comparisons O(N) per frame.

const CELL = 80;

function buildGrid(particles) {
  const grid = new Map();
  for (const pt of particles) {
    const key = Math.floor(pt.x / CELL) + ',' + Math.floor(pt.y / CELL);
    if (!grid.has(key)) grid.set(key, []);
    grid.get(key).push(pt);
  }
  return grid;
}

function applyInteractions(particles, grid) {
  const MAX_SPEED = 12;

  for (const pt of particles) {
    const cx = Math.floor(pt.x / CELL);
    const cy = Math.floor(pt.y / CELL);

    for (let dx = -1; dx <= 1; dx++) {
      for (let dy = -1; dy <= 1; dy++) {
        const cell = grid.get((cx + dx) + ',' + (cy + dy));
        if (!cell) continue;
        for (const other of cell) {
          if (other === pt || other.note === pt.note) continue;

          const nx   = pt.x - other.x;
          const ny   = pt.y - other.y;
          const dist = Math.sqrt(nx * nx + ny * ny);
          if (dist < 1) continue;

          if (dist < 40) {
            const f = 2.5 / dist;
            pt.vx += (nx / dist) * f;
            pt.vy += (ny / dist) * f;
          } else if (dist < 120) {
            const t = (dist - 40) / 80;
            const f = 0.09 * (1 - t);
            pt.vx -= (nx / dist) * f;
            pt.vy -= (ny / dist) * f;
          }
        }
      }
    }

    const spd = Math.sqrt(pt.vx * pt.vx + pt.vy * pt.vy);
    if (spd > MAX_SPEED) { pt.vx = pt.vx / spd * MAX_SPEED; pt.vy = pt.vy / spd * MAX_SPEED; }
  }
}

// --- Web Audio: chromatically tuned explosion sounds -------------------------
let audioCtx = null;
let soundOn  = false;
let started  = false;

const soundBtn = document.getElementById('sound-toggle');

function updateSoundIcon() {
  soundBtn.textContent = soundOn ? soundBtn.dataset.on : soundBtn.dataset.off;
  soundBtn.classList.toggle('on', soundOn);
}

document.getElementById('start-btn').addEventListener('click', () => {
  if (!audioCtx) audioCtx = new AudioContext();
  audioCtx.resume();
  soundOn = true;
  started = true;
  updateSoundIcon();
  document.getElementById('start-overlay').remove();
});

soundBtn.addEventListener('click', () => {
  if (!audioCtx) return;
  if (soundOn) {
    audioCtx.suspend();
    soundOn = false;
  } else {
    audioCtx.resume();
    soundOn = true;
  }
  updateSoundIcon();
});

function getAudio() {
  return (soundOn && audioCtx) ? audioCtx : null;
}

function midiToHz(note) {
  return 440 * Math.pow(2, (note - 69) / 12);
}

let activeVoices = 0;
const MAX_VOICES = 6;

function playExplosion(note, vel) {
  const ctx = getAudio();
  if (!ctx) return;
  if (activeVoices >= MAX_VOICES) return;
  const now  = ctx.currentTime;
  const freq = midiToHz(note);
  const amp  = 0.55 * (vel / 127);

  activeVoices++;
  const master = ctx.createGain();
  master.gain.setValueAtTime(amp, now);
  master.connect(ctx.destination);
  setTimeout(() => { activeVoices--; }, 780);

  // Layer 1: pitched sine with pitch-drop attack
  const osc1 = ctx.createOscillator();
  const env1 = ctx.createGain();
  osc1.type = 'sine';
  osc1.frequency.setValueAtTime(freq * 1.2, now);
  osc1.frequency.exponentialRampToValueAtTime(freq, now + 0.025);
  env1.gain.setValueAtTime(1.0, now);
  env1.gain.exponentialRampToValueAtTime(0.001, now + 0.7);
  osc1.connect(env1); env1.connect(master);
  osc1.start(now); osc1.stop(now + 0.75);

  // Layer 2: sub-octave sine for low-end weight
  const osc2 = ctx.createOscillator();
  const env2 = ctx.createGain();
  osc2.type = 'sine';
  osc2.frequency.setValueAtTime(freq / 2, now);
  env2.gain.setValueAtTime(0.7, now);
  env2.gain.exponentialRampToValueAtTime(0.001, now + 0.55);
  osc2.connect(env2); env2.connect(master);
  osc2.start(now); osc2.stop(now + 0.6);

  // Layer 3: short burst of band-passed white noise
  const bufLen   = Math.ceil(ctx.sampleRate * 0.12);
  const noiseBuf = ctx.createBuffer(1, bufLen, ctx.sampleRate);
  const data     = noiseBuf.getChannelData(0);
  for (let i = 0; i < bufLen; i++) data[i] = Math.random() * 2 - 1;

  const noise  = ctx.createBufferSource();
  noise.buffer = noiseBuf;

  const bpf = ctx.createBiquadFilter();
  bpf.type = 'bandpass';
  bpf.frequency.value = freq * 2;
  bpf.Q.value = 1.2;

  const env3 = ctx.createGain();
  env3.gain.setValueAtTime(0.8, now);
  env3.gain.exponentialRampToValueAtTime(0.001, now + 0.10);

  noise.connect(bpf); bpf.connect(env3); env3.connect(master);
  noise.start(now); noise.stop(now + 0.12);
}

// --- WebMIDI setup -----------------------------------------------------------
WebMidi.enable()
  .then(() => {
    function attachInput(input) {
      document.getElementById('device-name').textContent = input.name;
      document.getElementById('device-name').classList.remove('none');

      input.addListener('noteon', e => {
        const note = e.note.number;
        const vel  = e.rawVelocity;
        registerNote(note);
        midi.activeNotes.add(note);
        spawnBurst(note, vel);
        playExplosion(note, vel);
      });

      input.addListener('noteoff', e => {
        midi.activeNotes.delete(e.note.number);
      });

      input.addListener('controlchange', e => {
        const key = e.message.channel + ':' + e.controller.number;
        midi.ccData[key] = {
          channel: e.message.channel,
          cc:      e.controller.number,
          value:   e.rawValue,
        };
        midi.activeCcKey = key;
      });
    }

    WebMidi.inputs.forEach(attachInput);

    WebMidi.addListener('connected', e => {
      if (e.port.type === 'input') attachInput(e.port);
    });
    WebMidi.addListener('disconnected', e => {
      const el = document.getElementById('device-name');
      if (el.textContent === e.port.name) {
        el.textContent = 'no device';
        el.classList.add('none');
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
  textFont('Courier New');
}

function draw() {
  // Low-alpha fill creates motion trails instead of a hard clear
  noStroke();
  fill(8, 8, 16, 35);
  rect(0, 0, width, height);

  const g = gravityAccel();

  // Trickle particles for held notes
  for (const note of midi.activeNotes) {
    spawnTrickle(note);
  }

  // Build spatial grid once per frame (used for both physics and sparks)
  const grid = buildGrid(midi.particles);

  // Cross-note physics: repulsion + orbital attraction
  applyInteractions(midi.particles, grid);

  // Update positions and draw particles
  for (const pt of midi.particles) {
    pt.vy += g;
    pt.x  += pt.vx;
    pt.y  += pt.vy;
    pt.vx *= 0.995;
    pt.life -= 0.007;

    const a = pt.life * 255;

    noStroke();
    fill(pt.r, pt.g, pt.b, a * 0.08);
    circle(pt.x, pt.y, pt.size * 6);

    fill(pt.r, pt.g, pt.b, a * 0.25);
    circle(pt.x, pt.y, pt.size * 2.8);

    fill(pt.r, pt.g, pt.b, a);
    circle(pt.x, pt.y, pt.size);
  }

  // Connection sparks: bright arcs between close different-note particles
  drawConnectionSparks(midi.particles, grid);

  // Remove dead particles
  midi.particles = midi.particles.filter(
    pt => pt.life > 0 && pt.y < height + 80 && pt.y > -80
  );

  // Draw held-note glow spots at spawn height
  for (const note of midi.activeNotes) {
    const cfg = midi.seenNotes[note];
    if (!cfg) continue;
    const x = noteXFrac(note) * width;
    const y = height * 0.65;
    const [r, g2, b] = cfg.color;
    noStroke();
    for (let radius = 50; radius > 0; radius -= 8) {
      fill(r, g2, b, 4);
      circle(x, y, radius * 2);
    }
  }

  drawBottomUI(g);

  // Hint when nothing has happened yet (only after start)
  const hasNotes = Object.keys(midi.seenNotes).length > 0;
  const hasCc    = midi.activeCcKey !== null;
  if (started && !hasNotes && !hasCc) {
    noStroke();
    fill(55, 55, 80);
    textAlign(CENTER, CENTER);
    textSize(14);
    text('press a key ' + SEP + ' move a slider', width / 2, height / 2);
  }
}

// --- Connection sparks -------------------------------------------------------
function drawConnectionSparks(particles, grid) {
  const SPARK_R = 28;

  for (const pt of particles) {
    const cx = Math.floor(pt.x / CELL);
    const cy = Math.floor(pt.y / CELL);

    for (let dx = -1; dx <= 1; dx++) {
      for (let dy = -1; dy <= 1; dy++) {
        const cell = grid.get((cx + dx) + ',' + (cy + dy));
        if (!cell) continue;
        for (const other of cell) {
          if (other === pt || other.note === pt.note || other < pt) continue;

          const nx   = pt.x - other.x;
          const ny   = pt.y - other.y;
          const dist = Math.sqrt(nx * nx + ny * ny);
          if (dist > SPARK_R) continue;

          const t = 1 - dist / SPARK_R;
          const a = t * 200 * Math.min(pt.life, other.life);

          const mr = (pt.r + other.r) / 2;
          const mg = (pt.g + other.g) / 2;
          const mb = (pt.b + other.b) / 2;
          const mx = (pt.x + other.x) / 2;
          const my = (pt.y + other.y) / 2;

          stroke(mr, mg, mb, a);
          strokeWeight(1 + t);
          line(pt.x, pt.y, other.x, other.y);

          noStroke();
          fill(mr, mg, mb, a * 1.4);
          circle(mx, my, 4 * t + 1);
        }
      }
    }
  }
}

// --- Bottom UI: note dots (left) + CC gravity meter (right) ------------------
function drawBottomUI(g) {
  const barH = 80;
  const barY = height - barH;
  const divX = width * 0.60;

  noStroke();
  fill(8, 8, 16, 200);
  rect(0, barY, width, barH);

  stroke(20, 20, 32);
  strokeWeight(1);
  line(0, barY, width, barY);
  line(divX, barY, divX, height);

  drawNoteRow(barY, divX);
  drawCCPanel(divX, barY, g);
}

function drawNoteRow(barY, maxX) {
  const sorted = sortedSeenNotes();
  if (sorted.length === 0) return;

  const cy = barY + 28;

  for (let i = 0; i < sorted.length; i++) {
    const note   = sorted[i];
    const cfg    = midi.seenNotes[note];
    const x      = ((i + 1) / (sorted.length + 1)) * maxX;
    const active = midi.activeNotes.has(note);
    const [r, g2, b] = cfg.color;
    const dotR   = active ? 10 : 7;

    noStroke();
    fill(r, g2, b, active ? 220 : 55);
    circle(x, cy, dotR * 2);

    if (active) {
      noFill();
      stroke(r, g2, b, 120);
      strokeWeight(1.5);
      circle(x, cy, dotR * 3.5);
    }

    noStroke();
    fill(r, g2, b, active ? 220 : 80);
    textStyle(active ? BOLD : NORMAL);
    textAlign(CENTER, CENTER);
    textSize(11);
    text(noteName(note), x, cy + 20);

    fill(r, g2, b, active ? 160 : 50);
    textStyle(NORMAL);
    textSize(9);
    text(note, x, cy + 32);
  }
}

function drawCCPanel(leftX, barY, g) {
  const rightX  = width - 12;
  const barW    = rightX - leftX - 100;
  const labelX  = leftX + 12;
  const trackX  = leftX + 90;
  const trackY  = barY + 22;
  const trackH  = 8;

  if (!midi.activeCcKey) {
    noStroke();
    fill(50, 50, 65);
    textAlign(LEFT, CENTER);
    textStyle(NORMAL);
    textSize(11);
    text('move a slider -> controls gravity', labelX, barY + 38);
    return;
  }

  const d    = midi.ccData[midi.activeCcKey];
  const norm = d.value / 127;

  // Section label
  noStroke();
  fill(80, 80, 100);
  textAlign(LEFT, CENTER);
  textStyle(NORMAL);
  textSize(10);
  text('GRAVITY  ' + UPDN, labelX, trackY + 4);

  // CC info below
  fill(50, 50, 65);
  textSize(10);
  text('ch ' + d.channel + ' ' + SEP + ' ' + ccLabel(d.cc), labelX, trackY + trackH + 16);

  // Track background
  fill(20, 20, 35);
  rect(trackX, trackY, barW, trackH, 2);

  // Filled portion
  fill(86, 180, 247);
  rect(trackX, trackY, barW * norm, trackH, 2);

  // Gravity direction arrow
  const arrowX = trackX + barW + 8;
  const arrowY = trackY + trackH / 2;
  stroke(86, 180, 247, 160);
  strokeWeight(1.5);
  if (g < -0.02) {
    drawArrow(arrowX, arrowY + 6, arrowX, arrowY - 6);
  } else if (g > 0.02) {
    drawArrow(arrowX, arrowY - 6, arrowX, arrowY + 6);
  } else {
    noStroke();
    fill(86, 180, 247, 100);
    circle(arrowX, arrowY, 5);
  }

  // Current value number
  noStroke();
  fill(86, 180, 247);
  textAlign(RIGHT, CENTER);
  textStyle(BOLD);
  textSize(18);
  text(d.value, trackX + barW + 50, trackY + 4);

  fill(50, 50, 70);
  textStyle(NORMAL);
  textSize(10);
  text('/ 127', trackX + barW + 50, trackY + 18);
}

function drawArrow(x1, y1, x2, y2) {
  line(x1, y1, x2, y2);
  const angle = Math.atan2(y2 - y1, x2 - x1);
  const len   = 5;
  line(x2, y2,
    x2 - len * Math.cos(angle - 0.5),
    y2 - len * Math.sin(angle - 0.5));
  line(x2, y2,
    x2 - len * Math.cos(angle + 0.5),
    y2 - len * Math.sin(angle + 0.5));
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}
