(local animals {})

(fn animals.new [self sound size]
  (set self.__index self)
  (local new-obj {: size : sound})
  (setmetatable new-obj self))

(fn animals.makeSound [self]
  (print self.sound))

(local dog (animals:new :barks :medium))

(dog:makeSound)
