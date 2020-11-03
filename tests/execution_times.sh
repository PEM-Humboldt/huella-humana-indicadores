#!/bin/bash
function timeit () {
  { time "$@" 2>> err.log ; } 2>&1 | grep real | awk '{print $2}'
}

for filename in data/test/geofences/*.shp; do
  name=$(echo "$filename" | rev | cut -d "/" -f 1 | rev | cut -d "." -f 1)
  args=("$filename" data/test/IHEH -c epsg:4326)
  exec_time=$(timeit python src/create_hf_indicators.py "results/test/hf_indicators_${name}.shp" "${args[@]}")
  echo "Indicators ${name}:" "$exec_time" >> time.log
  exec_time=$(timeit python src/create_hf_persistence.py "results/test/hf_persistence_${name}.shp" "${args[@]}")
  echo "Persistence ${name}:" "$exec_time" >> time.log
done
