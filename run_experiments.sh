#! /bin/bash
#PBS -l nodes=1:ppn=8

run_experiment()
{
  name=$1
  mkdir -p $name && cd $name
  cp ../../$name.in ../../beaver_creek.npy .
  dakota -i $name.in -o $name.out
}

if [[ $PBS_O_WORKDIR ]]; then
  cd $PBS_O_WORKDIR
fi

PYTHON_ROOT=/usr/local/anaconda/2.7
DAKOTA_ROOT=/usr/local/dakota

export PATH=$(pwd):$PYTHON_ROOT/bin:$DAKOTA_ROOT/bin:$PATH
export LD_LIBRARY_PATH=$DAKOTA_ROOT/bin:$DAKOTA_ROOT/lib:$LD_LIBRARY_PATH

EXPERIMENT_NAMES="log_model_global \
  peckham_model \
  power_model_local \
  log_model \
  power_model_global \
  log_model_local \
  power_model"

echo "dakota_version: $(dakota --version)"
echo "which_dakota: $(which dakota)"

mkdir _experiments && cd _experiments
for name in $EXPERIMENT_NAMES; do
  (run_experiment $name > /dev/null) &
done

wait
