n = io.read()

local sorted_entries = {}

for _ = 1, n do
   local a, b = string.match(io.read(),"(-?%d+)%s(%d+)")
   -- print(a) print(b)
   a = tonumber(a) b=tonumber(b)
   print(type(a)) print(type(b))
   if sorted_entries[b] then
      sorted_entries[b] = sorted_entries[b] + a
   else sorted_entries[b] = a end
end

for i,j in pairs(sorted_entries) do print(i,j) end

local summations = {}
summations[0]=0
local maximum = -math.huge
for i=1,#sorted_entries do
   print('---')
   table.insert(summations, summations[#summations] + sorted_entries[i])
   if summations[#summations]>maximum then maximum=summations[#summations] end
end

for i,j in ipairs(summations) do print(i,j) end

print(maximum)

-- print(math.max(table.unpack(summations)))

-- print(table.unpack(summations))
