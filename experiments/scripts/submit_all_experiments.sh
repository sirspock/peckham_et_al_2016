#! /bin/bash

GROUP_NAME="power_analytic"
ALL_EXPERIMENTS=" \
  power_model_cobyla \
  power_model_global \
  power_model_local \
"

#  power_model_nl2sol_numerical_grads \
#  power_model_numerical_grads \
#  power_model_cobyla
#  power_model
#  power_model_nl2sol_analytic_grads
#  power_model_numerical_grads
#  power_model_global
#  power_model_local
#  power_model_nl2sol_numerical_grads
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


cd output/_experiments_$GROUP_NAME
for name in $ALL_EXPERIMENTS; do
  export EXPERIMENT_NAMES=$name
  qsub ../../scripts/run_experiments.sh -N "dakota-$name-$GROUP_NAME" -v EXPERIMENT_NAMES -l nodes=1:ppn=1
done
