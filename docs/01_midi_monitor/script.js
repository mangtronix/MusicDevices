// 01 -- MIDI Monitor
//
// Lists every connected MIDI input and output and shows a live, colour-coded
// log of every incoming MIDI message (note on/off, control change, pitch bend,
// and anything else) with timestamps and a filter. Useful as an oscilloscope
// for MIDI when you are building your own controllers and need to see what
// they are actually sending.
//
// Written with Claude by Michael Ang for Music Devices (IM-UH 3116, NYU Abu Dhabi).
// More info: https://mangtronix.github.io/MusicDevices/p5examples.html#01-midi-monitor

// --- State -------------------------------------------------------------------
let messageCount = 0;
const MAX_ENTRIES = 200;   // keep the DOM lean
let filterType = 'all';

// --- Helpers -----------------------------------------------------------------
function timestamp() {
  const d = new Date();
  return d.toLocaleTimeString('en-US', { hour12: false }) +
         '.' + String(d.getMilliseconds()).padStart(3, '0');
}

function noteLabel(number) {
  const names = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'];
  return names[number % 12] + Math.floor(number / 12 - 1);
}

// --- Log a MIDI message ------------------------------------------------------
function logMessage(type, detail) {
  if (filterType !== 'all' && type !== filterType) return;

  const log = document.getElementById('log');

  const entry = document.createElement('div');
  entry.className = 'entry';

  const typeClass = {
    noteon: 'type-noteon',
    noteoff: 'type-noteoff',
    controlchange: 'type-cc',
    pitchbend: 'type-pitchbend',
  }[type] || 'type-other';

  entry.innerHTML =
    '<span class="time">' + timestamp() + '</span>' +
    '<span class="type ' + typeClass + '">' + type + '</span>' +
    '<span class="detail">' + detail + '</span>';

  log.prepend(entry);   // newest at top

  // Trim old entries
  while (log.children.length > MAX_ENTRIES) {
    log.removeChild(log.lastChild);
  }

  messageCount++;
  document.getElementById('log-count').textContent = messageCount + ' messages';
}

// --- Attach listeners to a MIDI input ----------------------------------------
function attachListeners(input) {
  // Note On -- a key / button was pressed
  input.addListener('noteon', e => {
    const note = e.note.number;
    const name = noteLabel(note);
    const vel  = e.rawVelocity;
    const ch   = e.message.channel;
    logMessage('noteon',
      'note ' + note + ' (' + name + ')  vel ' + vel + '  ch ' + ch + '  [' + input.name + ']');
  });

  // Note Off -- a key / button was released
  input.addListener('noteoff', e => {
    const note = e.note.number;
    const name = noteLabel(note);
    const ch   = e.message.channel;
    logMessage('noteoff',
      'note ' + note + ' (' + name + ')  ch ' + ch + '  [' + input.name + ']');
  });

  // Control Change -- sliders, knobs, pedals, etc.
  input.addListener('controlchange', e => {
    const cc  = e.controller.number;
    const val = e.rawValue;          // 0-127
    const ch  = e.message.channel;
    logMessage('controlchange',
      'CC ' + cc + '  value ' + val + '  ch ' + ch + '  [' + input.name + ']');
  });

  // Pitch Bend
  input.addListener('pitchbend', e => {
    logMessage('pitchbend',
      'value ' + e.value.toFixed(3) + '  ch ' + e.message.channel + '  [' + input.name + ']');
  });

  // Catch everything else as a raw byte dump
  input.addListener('midimessage', e => {
    const type = e.message.type;
    if (['noteon','noteoff','controlchange','pitchbend'].includes(type)) return;
    const bytes = Array.from(e.message.data)
      .map(b => b.toString(16).padStart(2,'0'))
      .join(' ');
    logMessage('other', type + '  [' + bytes + ']  [' + input.name + ']');
  });
}

// --- Update the device list sidebar ------------------------------------------
function refreshDeviceList() {
  const inEl  = document.getElementById('inputs-list');
  const outEl = document.getElementById('outputs-list');

  inEl.innerHTML  = WebMidi.inputs.length  ? '' : '<span class="no-devices">none</span>';
  outEl.innerHTML = WebMidi.outputs.length ? '' : '<span class="no-devices">none</span>';

  WebMidi.inputs.forEach(input => {
    const d = document.createElement('div');
    d.className = 'device active';
    d.textContent = input.name;
    inEl.appendChild(d);
  });

  WebMidi.outputs.forEach(output => {
    const d = document.createElement('div');
    d.className = 'device output';
    d.textContent = output.name;
    outEl.appendChild(d);
  });
}

// --- Main --------------------------------------------------------------------
WebMidi.enable()
  .then(() => {
    const statusEl = document.getElementById('status');
    statusEl.textContent = 'Web MIDI ready';
    statusEl.className = 'ok';

    WebMidi.inputs.forEach(attachListeners);
    refreshDeviceList();

    WebMidi.addListener('connected', e => {
      if (e.port.type === 'input') attachListeners(e.port);
      refreshDeviceList();
      logMessage('other', 'Device connected: ' + e.port.name);
    });

    WebMidi.addListener('disconnected', e => {
      refreshDeviceList();
      logMessage('other', 'Device disconnected: ' + e.port.name);
    });
  })
  .catch(err => {
    const statusEl = document.getElementById('status');
    statusEl.textContent = 'MIDI access denied: ' + err.message;
    statusEl.className = 'err';
    console.error(err);
  });

// --- UI controls -------------------------------------------------------------
document.getElementById('btn-clear').addEventListener('click', () => {
  document.getElementById('log').innerHTML = '';
  messageCount = 0;
  document.getElementById('log-count').textContent = '0 messages';
});

document.getElementById('filter').addEventListener('change', e => {
  filterType = e.target.value;
});
