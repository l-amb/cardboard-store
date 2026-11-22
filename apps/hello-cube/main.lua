-- Hello Cube: a cube turns in front of you; pinch it to change its colour.
-- Space: x is right, y is up, z is forward, in metres, from where you were when the app began.

local cube
local angle = 0
local n = 1
local colors = {
  {1.0, 0.3, 0.3},
  {0.3, 0.8, 0.4},
  {0.3, 0.5, 1.0},
  {1.0, 0.8, 0.2},
}

function on_start()
  cube = scene.cube():position(0, 0, 2):scale(0.5):color(1.0, 0.3, 0.3)
  cube.on_click = function(self)
    n = n % #colors + 1
    local c = colors[n]
    self:color(c[1], c[2], c[3])
    sound.beep(330 + n * 110, 0.08, 0.4)
  end

  scene.label('Hello! Pinch the cube.'):position(0, 0.9, 2)

  local panel = ui.panel('Hello Cube')
  panel:text('Pinch the cube to change its colour.')
  panel:button('Close', function() app.exit() end)
end

function on_update(dt)
  angle = angle + 45 * dt
  cube:rotation(0, angle, angle * 0.5)
end
