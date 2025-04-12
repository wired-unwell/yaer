--local csv = require("csv")
local csv = require("/home/behnam/.luarocks/share/lua/5.4/csv.lua")
local f = csv.open("try-csv.lua.csv")
for fields in f:lines() do
  for i, v in ipairs(fields) do print(i, v) end
end
