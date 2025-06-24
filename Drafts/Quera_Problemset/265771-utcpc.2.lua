-- I think this works perfectly.

local n = io.read()

local entries = {}

for _ = 1, n do
   local a, b = string.match(io.read(),"(-?%d+)%s+(%d+)")
   -- print(a) print(b)
   a = tonumber(a) b=tonumber(b)
   -- print(type(a)) print(type(b))
   table.insert(entries, {b,a})
   -- if entries[b] then
   --    entries[b] = sorted_entries[b] + a
   -- else sorted_entries[b] = a end
end

table.sort(entries, function(a, b) return a[1] < b[1] end)

-- for i,j in pairs(entries) do print(i,j[1] .. j[2]) end

local summations = {}
summations[0] = 0
local maximum = -math.huge

for i,j in ipairs(entries) do
   summations[i] = summations[i-1] + j[2]
   if summations[i] > maximum then maximum = summations[i] end
end


-- for i,j in ipairs(summations) do print("\x1b[31m" .. i, j .. "\x1b[35m") end

print(maximum)

-- print(math.max(table.unpack(summations)))

-- print(table.unpack(summations))
