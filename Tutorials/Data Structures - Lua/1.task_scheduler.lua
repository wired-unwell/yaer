-- script: lua
-- license: GPL-3.0

--[[ What is this script?
   Me learning Stack, Queue, Linked Lists, and Hash Tables to solve an exercise by GPT-4o.
   The solution is completely mine, and I don't even know if it works as intended.
   Even the form of the question I've written is my own interpretation of original problem, obviously.

   A simple task scheduler that allows use of dependencies and priprities.
--]]


--[[
local tasks = {}
local task = {
   id = 0,
   pri = 3,
   dep = {1,2,3},
   desc = 'Shit',
}
table.insert(tasks,t1)
tasks[task.id]=task
--]]

function tprint(tab,ind,line)
   local ind = ind or ''
   local line = line or '==='
   for i,j in pairs(tab) do print(ind .. i,j)
      if type(j) == 'table' then
	 tprint(j,ind..'\t\t','')
      end
   end
end

--[[
table.insert(tasks,{id=1,pri=3,job=8,dep=1})
table.insert(tasks,{id=3,pri=1,job=8,dep=2})
table.insert(tasks,{pri=0,job=8,dep=1})
-- tprint(tasks)
--]]

-- wtf am I even doing?
--[[
   high pro tasks first.
   deps done? -> do it
   deps notyet? -> do deps
   come back to task
   next pri
--]]

--[[
local task_low={}
local task_med={}
local task_high={}
local task_db={task_low,task_med,task_high}

task_db.new = function (task)
   task.pri = task.pri or 1
   table.insert(task_db[task.pri],task)
end

task_db.new({id='fack',pri=2,desc="I'm a task"})

task_db.new({id='noway',pri=3,desc="I'm a NEW AND BETTER task",dep={'fack'}})

tprint(task_db)

-- while true do
for i=3,1,-1 do
   print(i)
   -- OOOH. IF I SEPARATE TASKS IN DIFFERENT INDEXES, I CAN'T LINK BACK DEPS
end
-- end

--]]


--- Initial working version

local tasks = {}

-- I had indeed added some crappy implementation, where you could assign bad task ids.
-- Now the simple reassignment makes the id value unnecessary

function tasks.add (task)
   task.id=#tasks+1
   tasks[task.id]=task
end

function tasks.process(id)
   local task = tasks[id]
   -- print(task.desc .. ' ptry')
   if task.deps.resolved == true and task.done~=true then
      print(task.desc)
   else
      for _,dep_id in ipairs(task.deps) do
	 -- print("\x1b[1;31;43mLINE 80\x1b[0m")
	 if tasks[dep_id].done ~=true then
	    tasks.process(dep_id)
	 end
      end
      -- tasks.process(task.id)
      task.deps.resolved = true
      print(task.desc)
   end
   task.done=true
end

function tasks.resolve_deps(id)
   local task = tasks.id
   for _,n in pairs(task.deps) do
      tasks.process(n.id)
   end
end

function tasks.processAll()
   for _,task in ipairs(tasks) do
      -- print(task.desc .. " try")
      if task.done ~= true
	 and (task.deps.resolved==true or task.deps==nil or #task.deps==0) then
	 tasks.process(task.id)
	 
      elseif task.done ~= true and task.deps.resolved ~= true then
	 for _,dep_id in pairs(task.deps) do
	    if tasks[dep_id].done ~=true then
	       tasks.process(dep_id)
	    end
	 end	 
	 tasks.process(task.id)

      elseif task.done ~= true then
	 -- print('Something is wrong about task number: ' .. task.id)

      elseif task.done == true then
	 -- print('Already done: ' .. task.id)
      end
   end
end

tasks.add(
   {
      id=1,
      desc='One',
      done=false,
      deps={3, resolved=nil}
   }
)

tasks.add(
   {
      id=2,
      desc='Two',
      done=false,
      deps={}
   }
)
tasks.add(
   {
      id=3,
      desc='Three',
      -- done=false
      deps={}
   }
)
tasks.add(
   {
      id=4,
      desc='Four',
      -- done=false,
      deps={3}
   }
)
tasks.add(
   {
      id=6,
      desc='Five',
      done=false,
      deps={}
   }
)

-- tprint(tasks)
tasks.processAll()
