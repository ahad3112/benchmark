```Benchmarking Tool```
Details comming soon...

#### Sample argument for create module

    -n 2020.1 -c Tegner -p pdc.staff -wt 05:00:00 --max-ntasks-per-node 8 -th 6 -exe 'gmx_mpi mdrun -s /cfs/klemming/nobackup/m/maaahad/gromacs/benchmark/gromacs_benchmark_test/topol-2020.1-img-ahad.tpr -deffnm gmx_md' -s /cfs/klemming/nobackup/m/maaahad/gromacs/singularity/images/gromacs-2020.1-openmpi-3.0.0-fftw-3.3.7_final_test.sif -mod gcc/7.2.0 openmpi/3.0-gcc-7.2
