#!/usr/bin/env janet

## 1 Slow AF
# (def start1 (os/clock))
# (+ ;(range 100000000))
# (def finish1 (os/clock))
# (print "Janet (range): \x1b[31m" (- finish1 start1) " seconds\x1b[0m.")
(print "Janet (range): This takes more than 10 seconds. It's been commented out.")

## 2
(def start2 (os/clock))
(var result 0)
(for i 0 10000000
  # (set result (+ result i))
  (+= result i)
    )
(def finish2 (os/clock))
(print "\x1b[32mJanet (for):" (- finish2 start2) " seconds\x1b[0m.")

## 3
(def start3 (os/clock))
(var total 0)
(var i 0)
(while (< i 10000000)
    (+= total i)
    (++ i))
(def finish3 (os/clock))
(print "\x1b[33mJanet (while): " (- finish3 start3) " seconds\x1b[0m.")

## 4
(def start4 (os/clock))
(var total 0)
# (loop [i :range [0 100000000] :when (even? i)] (+= total i))
(loop [i :range [0 10000000]] (+= total i))
(def finish4 (os/clock))
(print "\x1b[34mJanet (loop): " (- finish4 start4) " seconds\x1b[0m.")
