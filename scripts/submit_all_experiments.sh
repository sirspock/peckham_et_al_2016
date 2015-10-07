#! /bin/bash

GROUP_NAME="nlsq5"
ALL_EXPERIMENTS=" \
  power_model \
  power_model_nl2sol \
"

#  power_model_global \
#  power_model_cobyla \
#  power_model_local \
#  peckham_model_nl2sol \
#  peckham_model
#  peckham_model_cobyla \
#  peckham_model_global \
#  peckham_model_local \
#  power_model
#  power_model_nl2sol


cd _experiments_$GROUP_NAME
for name in $ALL_EXPERIMENTS; do
  export EXPERIMENT_NAMES=$name
  qsub ../run_experiments.sh -N "dakota-$name-$GROUP_NAME" -v EXPERIMENT_NAMES -l nodes=1:ppn=1
done
