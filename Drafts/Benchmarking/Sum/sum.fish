#!/usr/bin/env fish

# set start (date +%s.%N)

# set result 0

# THIS DOESN'T WORK, TAKES TOO~ LONG:
#
# set i 0
# while test $i -le 10000000;
#     set result (math $result + $i)
#     set i (math $i + 1)
# end


# THE FOLLOWING RESULTS IN:
# ./sum.fish: Expansion produced too many results
#
# for i in (seq 10000000);
#     set result (math $result + $i)
# end

# set finish (date +%s.%N)
# echo -e "\x1b[93mFISH: $(math $finish - $start) seconds.\x1b[0m"

echo -e "\x1b[95mFish: This takes absolutely too long, more than 30 secons.\x1b[0m"
echo -e "\x1b[95m      The whole script is commented because of that.\x1b[0m"
