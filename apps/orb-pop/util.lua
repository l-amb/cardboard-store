-- Helpers for Orb Pop. require('util') loads this file from the same folder.
local util = {}

-- A random point on a shell r metres away, in front of you and a little above and below eye level.
function util.random_point(r)
  local azimuth = math.rad(math.random(-70, 70))
  local elevation = math.rad(math.random(-15, 30))
  return r * math.sin(azimuth) * math.cos(elevation),
         r * math.sin(elevation),
         r * math.cos(azimuth) * math.cos(elevation)
end

-- A bright colour for h between 0 and 1.
function util.hue(h)
  local i = math.floor(h * 6)
  local f = h * 6 - i
  local q = 1 - f
  i = i % 6
  if i == 0 then return 1, f, 0.2 end
  if i == 1 then return q, 1, 0.2 end
  if i == 2 then return 0.2, 1, f end
  if i == 3 then return 0.2, q, 1 end
  if i == 4 then return f, 0.2, 1 end
  return 1, 0.2, q
end

return util
