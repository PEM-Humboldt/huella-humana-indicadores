#!/bin/bash
function timeit () {
  { time "$@" 2>> logs/err.log ; } 2>&1 | grep real | awk '{print $2}'
}

for filename in data/shp/geofences/*.shp; do
  name=$(echo "$filename" | rev | cut -d "/" -f 1 | rev | cut -d "." -f 1)
  args=("$filename" data/tif/IHEH -c epsg:4326)
  exec_time=$(timeit python src/create_hf_indicators.py "results/hf_indicators_${name}.shp" "${args[@]}")
  echo "Indicators ${name}:" "$exec_time" >> logs/time.log
  exec_time=$(timeit python src/create_hf_persistence.py "results/hf_persistence_${name}.shp" "${args[@]}")
  echo "Persistence ${name}:" "$exec_time" >> logs/time.log
done
