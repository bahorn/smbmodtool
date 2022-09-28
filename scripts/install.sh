#!/bin/sh
python3 patcher.py $1 0xa6a5c ../asm/filename.bin
python3 patcher.py $1 0x2ae8 ../asm/jmp.bin
python3 patcher.py $1 0xa6760 ../asm/relloader.bin
