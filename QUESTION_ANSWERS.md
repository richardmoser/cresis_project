  GNU nano 5.6.1                        QUESTIONS.txt                                  # SCC23 MPAS-A Competition

Team Name: Embarrassingly Parallel (The University of Kansas)

Q1.1) What branch from MPAS-Dev/MPAS-Model was your basis for competition?
* The main branch of https://github.com/MPAS-Dev/MPAS-Model

Q1.2) Did you use a GPU version of the code? If so, what offload method?
* No, NA

Q1.3) Very briefly: what version of compiler, MPI library, and other major
libraries (e.g. CUDA) did you use to compile MPAS-A?
* GCC v11.3.1
* GFortran v11.3.1
* MPICH v4.0.2
* NetCDF-C v4.9.0
* NetCDF-Fortran v4.6.0
* PnetCDF v1.12.3
* ParallelIO v2.5.9
* HDF5 v1.12.2
* Zlib v1.2.12
* Curl v7.76.1


Q1.4) Paste your `make` command below:
* `make gfortran CORE=atmosphere USE_PIO2=true PRECISION=single`


Q1.5) Number of partitons used for submissions (# of CPU and # of GPU ranks):
* Problem 1: 8 (CPU only)
* Problem 2: 8 (CPU only)