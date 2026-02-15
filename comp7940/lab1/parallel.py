import multiprocessing as mp
import concurrent.futures
import numpy as np
import random
import time
import math
import argparse
import matplotlib.pyplot as plt

# MPI implementation (separate file: pi_calculation_mpi.py)
try:
    from mpi4py import MPI
    MPI_AVAILABLE = True
except ImportError:
    MPI_AVAILABLE = False
    print("Warning: mpi4py not available. MPI functions will be disabled.")

class PiCalculator:
    def __init__(self):
        self.actual_pi = math.pi
    
    def _monte_carlo_points(self, num_points):
        """计算单个进程/线程的蒙特卡洛点数"""
        count = 0
        for _ in range(num_points):
            x = random.random()
            y = random.random()
            if x*x + y*y <= 1:
                count += 1
        return count
    
    def sequential(self, num_points):
        # TODO: Implement sequential version
        start_time = time.time()
        count_inside = self._monte_carlo_points(num_points)
        pi_estimate = 4.0 * count_inside / num_points
        end_time = time.time()
        print(f"Sequential: Estimated pai = {pi_estimate}, Error = {abs(pi_estimate - self.actual_pi)}, Time = {end_time - start_time} seconds")
        
        return {
            'pi_estimate': pi_estimate,
            'error': abs(pi_estimate - self.actual_pi),
            'time': end_time - start_time,
            'method': 'Sequential'
        }
    
    def multiprocessing_version(self, num_points, num_processes):
        # TODO: Implement multiprocessing version
        start_time = time.time()
        
        points_per_process = num_points // num_processes
        
        with mp.Pool(num_processes) as pool:
            results = pool.map(self._monte_carlo_points, [points_per_process] * num_processes)
        
        total_inside = sum(results)
        pi_estimate = 4.0 * total_inside / (points_per_process * num_processes)
        end_time = time.time()
        print(f"Multiprocessing ({num_processes} processes): Estimated pi = {pi_estimate}, Error = {abs(pi_estimate - self.actual_pi)}, Time = {end_time - start_time} seconds")
        
        return {
            'pi_estimate': pi_estimate,
            'error': abs(pi_estimate - self.actual_pi),
            'time': end_time - start_time,
            'method': f'Multiprocessing ({num_processes} processes)'
        }
    def concurrent_futures_version(self, num_points, num_workers):
        # TODO: Implement concurrent.futures version
        start_time = time.time()
        
        points_per_worker = num_points // num_workers
        
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(self._monte_carlo_points, points_per_worker) 
                      for _ in range(num_workers)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        total_inside = sum(results)
        pi_estimate = 4.0 * total_inside / (points_per_worker * num_workers)
        end_time = time.time()
        print(f"Concurrent Futures ({num_workers} workers): Estimated pi = {pi_estimate}, Error = {abs(pi_estimate - self.actual_pi)}, Time = {end_time - start_time} seconds")
        
        return {
            'pi_estimate': pi_estimate,
            'error': abs(pi_estimate - self.actual_pi),
            'time': end_time - start_time,
            'method': f'Concurrent Futures ({num_workers} workers)'
        }
    def numpy_version(self, num_points):
        # TODO: Implement numpy vectorized version (bonus)
        start_time = time.time()
        
        # Generate random points
        x = np.random.random(num_points)
        y = np.random.random(num_points)
        
        # Count points inside unit circle
        inside_circle = (x*x + y*y) <= 1
        count_inside = np.sum(inside_circle)
        
        pi_estimate = 4.0 * count_inside / num_points
        end_time = time.time()
        print(f"NumPy Vectorized: Estimated pi = {pi_estimate}, Error = {abs(pi_estimate - self.actual_pi)}, Time = {end_time - start_time} seconds")
        
        return {
            'pi_estimate': pi_estimate,
            'error': abs(pi_estimate - self.actual_pi),
            'time': end_time - start_time,
            'method': 'NumPy Vectorized'
        }
    def thread_executor_version(self, num_points, num_workers):
        # TODO: Implement ThreadPoolExecutor version (bonus)
        # Note: This may not show speedup for CPU-bound tasks due to GIL
        start_time = time.time()
        
        points_per_worker = num_points // num_workers
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(self._monte_carlo_points, points_per_worker) 
                      for _ in range(num_workers)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        total_inside = sum(results)
        pi_estimate = 4.0 * total_inside / (points_per_worker * num_workers)
        end_time = time.time()
        print(f"Thread Pool ({num_workers} threads): Estimated pi = {pi_estimate}, Error = {abs(pi_estimate - self.actual_pi)}, Time = {end_time - start_time} seconds")
        
        return {
            'pi_estimate': pi_estimate,
            'error': abs(pi_estimate - self.actual_pi),
            'time': end_time - start_time,
            'method': f'Thread Pool ({num_workers} threads)'
        }
    def mpi_version(self, num_points):
        # TODO: Implement MPI version (bonus)
        # Note: This requires running with mpiexec
        if not MPI_AVAILABLE:
            print("MPI not available. Skipping MPI version.")
            return None
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        size = comm.Get_size()
        
        start_time = time.time()
        
        # Each process calculates partial points
        points_per_process = num_points // size
        local_count = self._monte_carlo_points(points_per_process)
        
        # Gather results from all processes
        total_count = comm.reduce(local_count, op=MPI.SUM, root=0)
        
        end_time = time.time()
        
        if rank == 0:
            pi_estimate = 4.0 * total_count / (points_per_process * size)
            return {
                'pi_estimate': pi_estimate,
                'error': abs(pi_estimate - self.actual_pi),
                'time': end_time - start_time,
                'method': f'MPI ({size} processes)'
            }
        return None

    def benchmark_all(self, args):
        # TODO: Run comprehensive benchmarks
        # TODO: Generate performance tables
        # TODO: Compare different approaches
        # TODO: Create plots if matplotlib available
        import pandas as pd
        results = []
        for num_points in args.num_points:
            num_points = int(num_points)
            for worker_count in args.workers:
                print(f"\n=== Running benchmark: num_points={num_points}, workers={worker_count} ===")
                results.append(self.sequential(num_points))
                results.append(self.multiprocessing_version(num_points, worker_count))
                results.append(self.concurrent_futures_version(num_points, worker_count))
                results.append(self.numpy_version(num_points))
                results.append(self.thread_executor_version(num_points, worker_count))

        df = pd.DataFrame(results)
        print(df)

        plt.figure(figsize=(10, 6))
        for method in df['method'].unique():
            subset = df[df['method'] == method]
            x_labels = [f"{int(p)} pts, {w} workers" for p, w in zip(subset['num_points'], subset['workers'])]
            plt.plot(x_labels, subset['time'], marker='o', label=method)

        plt.xticks(rotation=45)
        plt.xlabel("Configuration (points, workers)")
        plt.ylabel("Time (s)")
        plt.title("Pi Calculation Benchmark Time Comparison")
        plt.legend()
        plt.tight_layout()
        plt.savefig("pi_benchmark_time.png")

        plt.figure(figsize=(10, 6))
        for method in df['method'].unique():
            subset = df[df['method'] == method]
            x_labels = [f"{int(p)} pts, {w} workers" for p, w in zip(subset['num_points'], subset['workers'])]
            plt.plot(x_labels, subset['error'], marker='x', label=method)

        plt.xticks(rotation=45)
        plt.xlabel("Configuration (points, workers)")
        plt.ylabel("Error")
        plt.title("Pi Calculation Benchmark Error Comparison")
        plt.legend()
        plt.tight_layout()
        plt.savefig("pi_benchmark_error.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pi calculation using various parallel methods')
    parser.add_argument("--num-points", type=float, nargs="+", default=[1e6])
    parser.add_argument("--workers", type=int, nargs="+", default=[1])
    args = parser.parse_args()
    
    calculator = PiCalculator()
    calculator.benchmark_all(args)
