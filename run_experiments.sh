#! /bin/bash
#PBS -l nodes=1:ppn=8

run_experiment()
{
  name=$1
  mkdir -p $name && cd $name
  cp ../../$name.in ../../beaver_creek.npy ../../long_profile.py .
  dakota -i $name.in -o $name.out
}

if [[ $PBS_O_WORKDIR ]]; then
  cd $PBS_O_WORKDIR
fi

PYTHON_ROOT=/home/huttone/anaconda
DAKOTA_ROOT=/usr/local/dakota

export PATH=$(pwd):$PYTHON_ROOT/bin:$DAKOTA_ROOT/bin:$PATH
export LD_LIBRARY_PATH=$DAKOTA_ROOT/bin:$DAKOTA_ROOT/lib:$LD_LIBRARY_PATH

if [ -z ${EXPERIMENT_NAMES+x} ]; then
  EXPERIMENT_NAMES="log_model_global \
    peckham_model \
    power_model_local \
    log_model \
    power_model_global \
    log_model_local \
    power_model"
fi

echo "Running the following set of experiments:"
echo $EXPERIMENT_NAMES

echo "dakota_version: $(dakota --version)"
echo "which_dakota: $(which dakota)"

for name in $EXPERIMENT_NAMES; do
  (run_experiment $name > /dev/null) &
done

wait
