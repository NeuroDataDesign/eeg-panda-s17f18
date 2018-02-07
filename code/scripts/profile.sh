#!/bin/bash -e
# For python functions only
# Usage: ./profile.sh path/to/output command_to_profile other_args

./memlog.sh > ${1}/${2}_mem.txt &
memkey=$!
python cpulog.py ${1}/${2}_cpu.txt &
cpukey=$!
./disklog.sh > ${1}/${2}_disk.txt &
diskkey=$!

${3} ${@:4}

kill $memkey $cpukey $diskkey
