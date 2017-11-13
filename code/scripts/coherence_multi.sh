#!/bin/bash -e

./memlog.sh > ./mem.txt &
memkey=$!
python cpulog.py ./cpu.txt &
cpukey=$!
./disklog.sh > ./disk.txt &
diskkey=$!

python coherence_multi.py

kill $memkey $cpukey $diskkey
