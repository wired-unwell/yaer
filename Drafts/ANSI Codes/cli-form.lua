
-- This is my main form file
-- dependencies: lua 5.4, stty 9.4,

--[[
local function up()  end
local function down()  end
local function update_form() end
local function draw() end
--]]

local form = {
	{name = "Name", val = ""},
	{name = "Age", val = ""},
	{name = "Gender", val = ""},
}

local a = io.popen("stty -g")
local sttymode = a:read()
a:close();
a=nil
io.write("\x1b[?25l\n") -- \x1b[?1049h
os.execute("stty raw -echo")

do
   io.write("\x1b[6n")
   local r = ""
   repeat r=r..io.read(1) until r:sub(-1)=="R"
   local y, x = r:match("\x1b%[(%d+);(%d+)R")
   local a = io.popen("stty size")
   local lines, cols = a:read():match("(%d+)%s(%d+)")
   a:close(); a=nil
   if tonumber(y) > lines - 5 then io.write("We need scrolls.\n\r\x1b[2J\x1b[H") else ;; end
end

current = 1

while true do
   io.write("\x1b7")
   for i,item in ipairs(form) do
      if i==current then io.write(" \x1b[33m>> ") else io.write("    ") end
      io.write(item.name .. ":\x1b[0;1m \x1b[0K" .. item.val .. "\x1b[0m\n\r") -- \x1b[41m
   end
   local c= io.read(1)
   if c=="\x0d" or c == "\x03" or c=="\x1c" then break
   elseif c=="\x1b" then local seq=io.read(2)
      if seq=="[A" then current = current - 1;
      elseif seq=="[B" then current = current + 1 end -- C right, D left
      if current <= 1 then current = 1 elseif current >= #form then current = #form end
   elseif c=="\x08" or c=="\x7f" and #form[current].val>0
   then form[current].val = form[current].val:sub(1,#form[current].val-1)
   else
      -- print("Pressed: " .. c)
      form[current].val = form[current].val .. c
   end
   io.write("\x1b8")--\x1b[A
end

os.execute("stty " .. sttymode)

io.write("\x1b[?25h\n") -- \x1b[?1049l

do
   local name, age, gender
   for i,item in ipairs(form) do
      if item.name == "Name" then name = item.val
      elseif item.name == "Age" then age = tonumber(item.val) or 0
      elseif item.name == "Gender" then gender = item.val end
   end
   print(("Hello %s, you are a %s born around %d, huh?"):format(name, gender, os.date("*t").year - age))
end

