-- Orb Pop: pinch the orbs before they fade.
local util = require('util')

local MAX_ORBS = 6
local LIFETIME = 6

local orbs = {}
local score = 0
local best = storage.get('best', 0)
local scoreText

local function show_score()
  scoreText:set_text('Score ' .. score .. '    Best ' .. best)
end

local function remove(orb)
  for i = 1, #orbs do
    if orbs[i] == orb then
      table.remove(orbs, i)
      break
    end
  end
  orb:destroy()
end

local function pop(orb)
  remove(orb)
  score = score + 1
  sound.beep(500 + score * 15, 0.06, 0.4)
  if score > best then
    best = score
    storage.set('best', best)
  end
  show_score()
end

local function spawn_orb()
  if #orbs >= MAX_ORBS then return end
  local x, y, z = util.random_point(2.2)
  local orb = scene.sphere():position(x, y, z):scale(0.3):color(util.hue(math.random()))
  orb.born = time.now()
  orb.on_click = pop
  orbs[#orbs + 1] = orb
end

function on_start()
  local panel = ui.panel('Orb Pop')
  scoreText = panel:text('')
  panel:button('Close', function() app.exit() end)
  show_score()
  every(0.8, spawn_orb)
end

function on_update(dt)
  for i = #orbs, 1, -1 do
    local orb = orbs[i]
    local age = time.now() - orb.born
    if age > LIFETIME then
      remove(orb)
    else
      local s = 0.3 * (1 - age / LIFETIME * 0.6)
      orb:scale(s)
    end
  end
end
