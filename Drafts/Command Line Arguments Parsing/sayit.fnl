(print "see the source code :(
I could not evaluate my string...")

;; Wrong Implementations:
;; (print arg:1)
;; (print arg.1)
;; (print arg[1])
;;
;; Correct one:
(print (. arg 1))
