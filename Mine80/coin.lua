-- title:   Coin Toss
-- author:  Wired Unwell
-- desc:    A small cart about tossing a coin.
-- site:    https://wired_unwell.codeberg.page
-- license: GPL-3.0
-- version: 0.1
-- script:  lua

---@diagnostic enable: spell-check
---@diagnostic disable: lowercase-global

---@alias todo string An alias to mark an incomplete part of code.

--- A small class for 3D vectors and their calculation
---@class vector
---@field x number
---@field y number
---@field z number
local vector = {x=0,y=0,z=0}
vector.__index=vector
function vector:new(obj)
   return setmetatable(obj,self)
end

---@nodiscard
function vector:normalize(factor)
   -- self = self or v?
   factor = factor or 1
   assert(factor~=0, "Oi")
   local abs = self.x ^ 2 + self.y ^ 2 + self.z ^ 2
   abs = abs / factor
   return {x = self.x/abs, y = self.y/abs, z = self.z/abs}
end

--- A method two good normal vectors to a vector.
---@return vector, vector
---@nodiscard
function vector:orthogonals()
   local u = vector:new {
      x = self.y * self.z,
      y = self.x * self.z,
      z = -2 * self.x * self.y
   }
   local v = vector:new {
      x = self.y * self.z,
      y = -2 * self.x * self.z,
      z = self.x * self.y
   }
   return u, v
end

---@class coin
---@field center vector
---@field normal vector
---@field radius number
local coin = {
   center = vector:new{},
   normal = vector:new{x=1,y=1,z=1},
   radius = 10,
}
coin.__index = coin

function coin:new(obj)
   -- obj.center = obj.center or {0,0,0}
   return setmetatable(obj,self) -- this returns obj
end

function vector:shift(dir)
  self.x = self.x + dir.x
  self.y = self.y + dir.y
  self.z = self.z + dir.z
  return self
end

--- Rotate a 3D point/vector.
---@param self vector
---@param dx number: How much to rotate around x axis.
---@param dy number: ... in y axis.
---@param dz number: ... in z axis.
---@return vector point
---@nodiscard
function vector:rotate(dx, dy, dz)
   local x,y,z = self.x, self.y, self.z
   local yt = y * math.cos(dx) - z * math.sin(dx)
   local zt = y * math.sin(dx) + z * math.cos(dx)
   y = yt; z = zt
   local xt = x * math.cos(dy) - z * math.sin(dy)
   zt = x * math.sin(dy) + z * math.cos(dy)
   x = xt; z = zt
   xt = x * math.cos(dz) - y * math.sin(dz)
   yt = x * math.sin(dz) + y * math.cos(dz)
   x = xt; y = yt
   -- Unncessary side effect: point = {x=x,y=y,z=z}
   return {x=x,y=y,z=z}
end

--- Constructs points on a coin based on its normal and radius.
---@nodiscard
function coin:update()
   local r = self.radius
   -- local u,v = {x=1,y=0,z=0}, {x=0,y=1,z=0} -- this is for 2D circle.
   local u,v = vector.orthogonals(self.normal)
   local points = {}
   for i=-r,r do
      local num_r = r-i^2
      for j=-num_r,num_r do
	 -- SHOULD USE NORMAL HERE
	 table.insert(
	    points,
	    {x = self.center.x + i * u.x + j * v.x,
	     y = self.center.y + i * u.y + j * v.y,
	     z = self.center.z + i * u.z + j * v.z}) -- IDR WHY!!!
	 -- pix(new_point)
      end
   end
   table.sort(points,function(a,b) return a.z>b.z end)
   return points
end

function coin:draw(points)
   local color = 4
   points = points or self:update()
   for i=1,#points do
      local point = points[i]
      pix(
	 100*point.x / (point.z + 300),
	 100*point.y / (point.z + 300),
	 color
      )
   end
end

---@nodiscard
---@depricated
function coin:wobble()
   return self.normal:rotate(3*math.random(), 3*math.random(), 3*math.random()) -- or something
end

---@param cor vector Center Of Rotation
function coin:spin(cor,dx,dy,dz)
   trace(self.center:shift{x=-cor.x,y=-cor.y,z=-cor.z}.x)
   self.center = self.center:shift{x=-cor.x,y=-cor.y,z=-cor.z}:rotate(dx,dy,dz):shift{x=cor.x,y=cor.y,z=cor.z} -- I need to define a proper operator? Not yet, /shift/ works.
   return self
end

mycoin = coin:new{
   center=vector:new{x=160,y=68+20,z=0},
   normal=vector:new{z=1.1,y=0,x=1},
   radius=100} -- center normal radius


function TIC()
   cls(12)
   local t = time()/999
   mycoin.center.y = math.abs((10*t)%272-136)

   -- Why does it not work as a proper method? because it checks up methods in /mycoin/ instead of /normal/?
   mycoin.normal=vector.rotate(mycoin.normal,t/10,0,0)
   mycoin:draw() -- mycoin:draw(mycoin:update())
end


-- <PALETTE>
-- 000:1a1c2c5d275db13e53ef7d57ffcd75a7f07038b76425717929366f3b5dc941a6f673eff7f4f4f494b0c2566c86333c57
-- </PALETTE>
