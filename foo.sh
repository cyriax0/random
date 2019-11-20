while true; do test $(head -c 1 /dev/urandom |od|head -n 1|cut -d \  -f 2) -gt 200 && echo -n \\ || echo -n _;done
