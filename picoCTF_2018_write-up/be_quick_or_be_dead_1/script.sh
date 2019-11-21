#!/bin/bash

cp be-quick-or-be-dead-1 be-quick-or-be-dead-1_patched
chmod +x be-quick-or-be-dead-1_patched

rasm2 'mov eax, 0xeb866516' | xxd -p -r | dd conv=notrunc of=be-quick-or-be-dead-1_patched bs=1 seek=$((0x7a9)) 2>/dev/null

./be-quick-or-be-dead-1_patched | tail -1 
