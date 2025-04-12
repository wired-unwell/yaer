(var animals {
                :new (fn [self ?sound ?size]
                       (local new-obj {:sound ?sound :size ?size})
                       (set self.__index self)
                       (print self)
                       (setmetatable new-obj self))
                :make-sound (fn [self]
                              (print self.sound))})


(var dog {})
(print dog)

(set dog (animals:new dog "bark" "med"))
(print dog)

(print (table.concat dog))
