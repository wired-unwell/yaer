---[[
animals = {}

function animals:new(sound, size)
   self.__index=self
   newObj = {sound = sound, size = size}
   return setmetatable(newObj, self)
   end

function animals:makeSound()
   print(self.__name,self.sound)
   end

dog=animals:new("barks","medium")
dog:makeSound()
--]]

print("\x1b[33m")

---[[
class={desc = "class: This is a dummy class used to try OOP.", name = 'OK'}
print(class, "class")

print("\x1b[32m")

function class:add(o)
	o = o or {}
	self.__index=self
	print(self, "self")
	new={ name = self, 1}
	print(o,"o")
	return setmetatable(new,self)
	end

function class:echo()
	print(self) end
	
A = class:add()

print(A,"A")

print("\x1b[31m")

A:echo()

print("\x1b[34m")

print(class.desc)

--print(table.concat(getmetatable(A)))
--]]

print("\x1b[00m")

-- os.execute("clear")
