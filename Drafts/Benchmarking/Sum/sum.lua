#!/usr/bin/env lua
local start = os.clock()
local result = 0
for i=0,10000000 do
	result=result+i
end
local finish = os.clock()
print("\x1b[36mLua: " .. finish - start .. " seconds.\x1b[0m")
