#! /bin/bash

ALL_EXPERIMENTS="log_model_global peckham_model power_model_local log_model power_model_global log_model_local power_model"

cd _experiments_new
for name in $ALL_EXPERIMENTS; do
  export EXPERIMENT_NAMES=$name
  qsub ../run_experiments.sh -N "dakota-$name-new" -v EXPERIMENT_NAMES -l nodes=1:ppn=1
done
