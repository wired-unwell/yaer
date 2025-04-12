#!/usr/bin/env nu

# timeit {let res = 0; for i in 0..10000000 {let res = $res + $i}}

# let start = (^date +%s.%N | into float)
# let res = 0
# for i in 0..10000000 {let res = $res + $i}
# let finish = (^date +%s.%N | into float)
# echo "\e[33mNu\e[93mShell: " ($finish - $start) "seconds.\e[0m"

^echo "\e[33mNu\e[93mShell: Around 10 seconds.\e[0m"
