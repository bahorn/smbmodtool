#!/bin/sh
python3 patcher.py $1 0xa6a5c filename.bin
python3 patcher.py $1 0x2ae8 jmp.bin
python3 patcher.py $1 0xa6760 relloader.bin
