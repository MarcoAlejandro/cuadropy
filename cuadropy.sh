
#!/usr/bin/env bash

if [[ ! $1 ]]; then
  echo "Missing required argument: PROGRAM"
  echo "Usage: sh cuadropy.sh path/to/program.cupy"
  exit
fi

python3 -m src.main $1
