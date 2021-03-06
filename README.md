## Benchmarking Tool : `benchmark`

Before using this tool, one has to create appropriate `conda` environment and `activate` the environment. Environment
required for this tool can be created using the script: `create_environment.py`

#### Usage of `create_environment.py`

    usage: create_environment.py [-h] --env ENV

optional arguments:

        -h, --help  show this help message and exit
        --env ENV   Name of the ENVIRONMENT. If ABSOLUTE PATH not given, CURRENT
                    WORKING DIRECTORY will be appended.

Once the environment is created and activated, you are ready to use the `benchmark` tool.

##### Dependencies for `create_environment.py`

* `Python 2.7 or more`


### Usage of benchmark

    usage: benchmark.py [-h] {create,submit,inspect,analyze} ...

There are four submodules available:
* `create`
* `submit`
* `inspect`
* `analyze`

#### create

This submodule is responsible for creating job scripts for specified `Cluster`.

    usage: benchmark.py create [-h] [-n NAME] -c {Tegner,Beskow} -p PROJECT
                        [-wt WALL_TIME] [--min-nodes MIN_NODES]
                        [--max-nodes MAX_NODES]
                        [--min-ntasks-per-node MIN_NTASKS_PER_NODE]
                        [--max-ntasks-per-node MAX_NTASKS_PER_NODE]
                        [-g GRES [GRES ...]] [-mem MEMORIES [MEMORIES ...]]
                        [-o [OUTPUT_FILE]] [-e [ERROR_FILE]]
                        [-mod MODULES [MODULES ...]]
                        [-env KEY=VALUE [KEY=VALUE ...]] -exe EXE [EXE ...]
                        [-wd WORKDIR] [--simg SIMG] [-th THREADS] [-gpu]
                        [--node NODE]

More information for each option for this submodule can found by running `benchmark.py create -h/--help`

###### Sample command for create module for Cluster `Tegner` at `PDC`

    usage: benchmark.py create -n job -c Tegner -p pdc.staff -wt 05:00:00 --max-ntasks-per-node 8 -th 6 -exe 'gmx_mpi mdrun -s /cfs/klemming/nobackup/m/maaahad/gromacs/benchmark/gromacs_benchmark/topol-2020.1-img-ahad.tpr -deffnm gmx_md' -s /cfs/klemming/nobackup/m/maaahad/gromacs/singularity/images/hpccm-gromacs-2020.1-openmpi-3.0.0-fftw-3.3.7-test.sif -mod gcc/7.2.0 openmpi/3.0-gcc-7.2

#### submit

This submodule will submit all jobs to the Queue System of the Cluster where the Script runs.

    usage: benchmark.py submit [-h] [-s SUFFIX] [-d DIRECTORIES [DIRECTORIES ...]]
                        [-o] [-r]
More information for each option for this submodule can found by running `benchmark.py submit -h/--help`

#### inspect

This submodule inspects the currently submitted job in the Cluster where the script runs (`Not Implemented Properly`).

    usage: benchmark.py inspect [-h] [-s]

More information for each option for this submodule can found by running `benchmark.py inspect -h/--help`

#### analyze

This submodule analyze the performance of all finished jobs in given directory/directories. analyze module includes options for viewing, plotting and saving the performance data to `csv` file.

    usage: benchmark.py analyze [-h] [--csv] [-f FILE]
                         [-dt directory:tag [directory:tag ...]] [-r]
                         [-s SUFFIX] [--view] [--plot]

More information for each option for this submodule can found by running `benchmark.py analyze -h/--help`


##### Dependencies for `benchmark`

* `Python 3.0 or more`
* `seaborn`
* `pandas`
* `matplotlib`

If appropriate environment is created using the script `create_environment.py` and activated,
one does not have to worry about the above dependencies.

