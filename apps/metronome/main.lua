-- Metronome: a tempo slider and a start/stop button.
local bpm = storage.get('bpm', 100)
local running = false
local beat = 0
local timer
local status
local tempo

local function tick()
  beat = beat % 4 + 1
  sound.beep(beat == 1 and 880 or 660, 0.05, 0.6)
  status:set_text('Beat ' .. beat)
end

local function restart()
  if timer then
    timer:cancel()
    timer = nil
  end
  if running then
    timer = every(60 / bpm, tick)
  end
end

function on_start()
  local panel = ui.panel('Metronome')
  status = panel:text('Stopped')
  tempo = panel:slider('Tempo ' .. bpm .. ' BPM', 40, 200, bpm, function(value)
    bpm = math.floor(value + 0.5)
    storage.set('bpm', bpm)
    tempo:set_text('Tempo ' .. bpm .. ' BPM')
    restart()
  end)
  panel:button('Start / stop', function()
    running = not running
    beat = 0
    status:set_text(running and 'Running' or 'Stopped')
    restart()
  end)
  panel:button('Close', function() app.exit() end)
end
