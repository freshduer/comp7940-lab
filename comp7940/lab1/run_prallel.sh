# python parallel.py --num-points 1e6 1e7 1e8 --workers 1 2 4 8
echo -e "\n=== Running parallel methods ==="
module load openmpi
for procs in 4; do
    echo "Running MPI with $procs processes..."
    mpiexec -n $procs python pi_calculation_mpi.py --num-points 1e6 1e7 1e8 --workers 1 2 4 8
    echo ""
done