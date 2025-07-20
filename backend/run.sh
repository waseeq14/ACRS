#!/bin/bash

OUTPUT="/tmp/enum_results.txt"
echo "[+] Running LinPEAS" > "$OUTPUT"
chmod +x /tmp/linpeas.sh
bash /tmp/linpeas.sh -q -P 'HowDothTheLittleCrocodileImproveHisShiningTail'  -o users_information &>> "$OUTPUT"
echo "[+] LinPEAS execution complete." >> "$OUTPUT"
