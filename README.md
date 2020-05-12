```Benchmarking Tool```
Details comming soon...

#### Sample argument for create module (Tested on Tegner at PDC)

    benchmark create -n job -c Tegner -p pdc.staff -wt 05:00:00 --max-ntasks-per-node 8 -th 6 -exe 'gmx_mpi mdrun -s /cfs/klemming/nobackup/m/maaahad/gromacs/benchmark/gromacs_benchmark/topol-2020.1-img-ahad.tpr -deffnm gmx_md' -s /cfs/klemming/nobackup/m/maaahad/gromacs/singularity/images/hpccm-gromacs-2020.1-openmpi-3.0.0-fftw-3.3.7-test.sif -mod gcc/7.2.0 openmpi/3.0-gcc-7.2
