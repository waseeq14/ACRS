#!/bin/bash

OUTPUT="/tmp/enum_results.txt"
echo "[+] Running LinPEAS" > "$OUTPUT"
chmod +x /tmp/linpeas.sh
bash /tmp/linpeas.sh -q -o interesting_perms_files &>> "$OUTPUT"
echo "[+] LinPEAS execution complete." >> "$OUTPUT"
