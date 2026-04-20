// --- Common CC names ---------------------------------------------------------
const CC_NAMES = {
  0:'Bank Select',  1:'Modulation',   2:'Breath',        4:'Foot Ctrl',
  5:'Portamento Time', 7:'Volume',    8:'Balance',       10:'Pan',
  11:'Expression',  12:'Effect 1',   13:'Effect 2',     32:'Bank (LSB)',
  64:'Sustain',     65:'Portamento', 66:'Sostenuto',    67:'Soft Pedal',
  68:'Legato',      71:'Resonance',  72:'Release',      73:'Attack',
  74:'Filter Cutoff', 75:'Decay',    76:'Vib Rate',     77:'Vib Depth',
  78:'Vib Delay',   91:'Reverb',     92:'Tremolo',      93:'Chorus',
  94:'Detune',      95:'Phaser',    120:'All Sound Off',121:'Reset Ctrls',
  123:'All Notes Off',
};

function ccName(cc) { return CC_NAMES[cc] || ''; }

// --- State -------------------------------------------------------------------
const HISTORY_LEN = 300;

const state = {
  activeKey: null,
  ccData: {},        // "ch:cc" -> { channel, cc, value, history[] }
};

function keyFor(ch, cc) { return ch + ':' + cc; }

function getOrCreate(channel, cc, value) {
  const key = keyFor(channel, cc);
  if (!state.ccData[key]) {
    state.ccData[key] = {
      channel, cc, value,
      history: new Array(HISTORY_LEN).fill(value),
    };
  }
  return state.ccData[key];
}

// Middle-dot separator (U+00B7) rendered via escape so this file stays ASCII
const SEP = '\u00b7';

// --- HTML update helpers -----------------------------------------------------
function updateInfoLine() {
  const el = document.getElementById('cc-info');
  if (!state.activeKey) {
    el.innerHTML = '<span class="hint">move a slider or knob on your controller...</span>';
    return;
  }
  const d = state.ccData[state.activeKey];
  const name = CC_NAMES[d.cc] || '(generic CC)';
  el.innerHTML =
    '<span class="field">ch</span> <span class="val">' + d.channel + '</span>' +
    '<span class="sep"> ' + SEP + ' </span>' +
    '<span class="field">cc</span> <span class="val">' + d.cc + '</span>' +
    '<span class="sep"> ' + SEP + ' </span>' +
    '<span class="name">' + name + '</span>' +
    '<span class="sep"> ' + SEP + ' </span>' +
    '<span class="field">value</span> <span class="val-big">' + d.value + '</span>' +
    '<span class="sep">/ 127</span>';
}

function updateChips() {
  const container = document.getElementById('cc-list');

  for (const [key, d] of Object.entries(state.ccData)) {
    let chip = document.getElementById('chip-' + key);

    if (!chip) {
      chip = document.createElement('div');
      chip.id = 'chip-' + key;
      chip.innerHTML =
        '<div class="chip-top">' +
          '<span class="chip-value" id="val-' + key + '">0</span>' +
          '<span class="chip-name">' + (ccName(d.cc) || 'CC ' + d.cc) + '</span>' +
        '</div>' +
        '<div class="chip-bar-track"><div class="chip-bar-fill" id="bar-' + key + '"></div></div>' +
        '<div class="chip-meta">ch ' + d.channel + ' ' + SEP + ' cc ' + d.cc + '</div>';
      container.appendChild(chip);
    }

    chip.className = 'cc-chip' + (key === state.activeKey ? ' active' : '');

    document.getElementById('val-' + key).textContent = d.value;
    document.getElementById('bar-' + key).style.width = (d.value / 127 * 100).toFixed(1) + '%';
  }
}

// Estimate chip grid height so the canvas avoids it
function chipGridHeight() {
  const rows = Math.max(1, Math.ceil(Object.keys(state.ccData).length / 4));
  return rows * 74 + 1;
}

// --- WebMIDI setup -----------------------------------------------------------
WebMidi.enable()
  .then(() => {
    function attachInput(input) {
      document.getElementById('device-name').textContent = input.name;
      document.getElementById('device-name').classList.remove('none');

      input.addListener('controlchange', e => {
        const channel = e.message.channel;
        const cc      = e.controller.number;
        const value   = e.rawValue;

        const d = getOrCreate(channel, cc, value);
        d.value = value;
        d.history.push(value);
        if (d.history.length > HISTORY_LEN) d.history.shift();

        state.activeKey = keyFor(channel, cc);
        updateInfoLine();
        updateChips();
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
const ACCENT = [86, 180, 247];

function setup() {
  createCanvas(windowWidth, windowHeight);
  colorMode(RGB, 255, 255, 255, 255);
  textFont('Courier New');
}

function draw() {
  background(13, 13, 20);

  if (!state.activeKey) {
    noStroke();
    fill(60, 60, 90);
    textAlign(CENTER, CENTER);
    textSize(14);
    text('move a slider or knob on your controller...', width / 2, height / 2);
    return;
  }

  const d = state.ccData[state.activeKey];

  // Layout: reserve space for the top HUD (85px) and bottom chip grid
  const topPad  = 85;
  const botPad  = chipGridHeight() + 10;
  const availH  = height - topPad - botPad;

  // Dial -- centered horizontally, upper portion of available area
  const dialR = Math.min(width * 0.15, availH * 0.38);
  const cx    = width / 2;
  const cy    = topPad + dialR + 10;

  // Waveform -- full width, between dial and chip grid
  const waveTop    = cy + dialR + 30;
  const waveBottom = height - botPad - 10;
  const waveLeft   = width * 0.06;
  const waveRight  = width * 0.94;

  drawDial(cx, cy, dialR, d);
  if (waveBottom > waveTop + 40) {
    drawWaveform(d, waveLeft, waveRight, waveTop, waveBottom);
  }
}

// --- Dial --------------------------------------------------------------------
function drawDial(cx, cy, r, d) {
  const norm       = d.value / 127;
  const startAngle = radians(150);
  const sweepAngle = radians(240);
  const endAngle   = startAngle + sweepAngle * norm;

  // Background track
  noFill();
  stroke(28, 28, 42);
  strokeWeight(8);
  arc(cx, cy, r * 2, r * 2, startAngle, startAngle + sweepAngle);

  // Value arc
  if (norm > 0) {
    stroke(ACCENT[0], ACCENT[1], ACCENT[2]);
    strokeWeight(8);
    arc(cx, cy, r * 2, r * 2, startAngle, endAngle);
  }

  // Needle tip dot
  fill(ACCENT[0], ACCENT[1], ACCENT[2]);
  noStroke();
  circle(
    cx + Math.cos(endAngle) * r,
    cy + Math.sin(endAngle) * r,
    12
  );

  // Center value (big)
  fill(ACCENT[0], ACCENT[1], ACCENT[2]);
  textAlign(CENTER, CENTER);
  textStyle(BOLD);
  textSize(r * 0.55);
  text(d.value, cx, cy - r * 0.04);

  // "/ 127"
  fill(55, 55, 75);
  textStyle(NORMAL);
  textSize(r * 0.14);
  text('/ 127', cx, cy + r * 0.34);

  // Tick marks
  drawTick(cx, cy, r, startAngle,                   '0');
  drawTick(cx, cy, r, startAngle + sweepAngle * 0.5, '64');
  drawTick(cx, cy, r, startAngle + sweepAngle,       '127');
}

function drawTick(cx, cy, r, angle, label) {
  stroke(38, 38, 55);
  strokeWeight(1.5);
  line(
    cx + Math.cos(angle) * r * 1.12, cy + Math.sin(angle) * r * 1.12,
    cx + Math.cos(angle) * r * 1.22, cy + Math.sin(angle) * r * 1.22,
  );
  noStroke();
  fill(48, 48, 68);
  textStyle(NORMAL);
  textSize(11);
  textAlign(CENTER, CENTER);
  text(label, cx + Math.cos(angle) * r * 1.38, cy + Math.sin(angle) * r * 1.38);
}

// --- Waveform ----------------------------------------------------------------
function drawWaveform(d, left, right, top, bottom) {
  const midY = (top + bottom) / 2;
  const h    = bottom - top;
  const w    = right - left;

  // Axes
  stroke(25, 25, 40);
  strokeWeight(1);
  line(left, top,    right, top);
  line(left, bottom, right, bottom);
  line(left, midY,   right, midY);
  line(left, top,    left,  bottom);

  // Axis labels
  noStroke();
  fill(38, 38, 58);
  textStyle(NORMAL);
  textSize(10);
  textAlign(RIGHT, CENTER);
  text('127', left - 5, top);
  text(' 64', left - 5, midY);
  text('  0', left - 5, bottom);

  const hist = d.history;

  // Filled area
  noStroke();
  fill(ACCENT[0], ACCENT[1], ACCENT[2], 25);
  beginShape();
  vertex(left, bottom);
  for (let i = 0; i < hist.length; i++) {
    vertex(left + (i / (hist.length - 1)) * w, bottom - (hist[i] / 127) * h);
  }
  vertex(right, bottom);
  endShape(CLOSE);

  // Line
  noFill();
  stroke(ACCENT[0], ACCENT[1], ACCENT[2], 210);
  strokeWeight(2);
  beginShape();
  for (let i = 0; i < hist.length; i++) {
    vertex(left + (i / (hist.length - 1)) * w, bottom - (hist[i] / 127) * h);
  }
  endShape();

  // Current value dot + label on right edge
  const curY = bottom - (d.value / 127) * h;
  fill(ACCENT[0], ACCENT[1], ACCENT[2]);
  noStroke();
  circle(right, curY, 8);
  textAlign(LEFT, CENTER);
  textSize(12);
  text(d.value, right + 8, curY);
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}
