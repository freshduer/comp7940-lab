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
        
        # 获取MPI信息
        if MPI_AVAILABLE:
            comm = MPI.COMM_WORLD
            rank = comm.Get_rank()
            size = comm.Get_size()
        else:
            rank = 0
            size = 1
        
        # 先运行MPI版本 - 所有进程参与
        if MPI_AVAILABLE:
            print(f"\n=== Running MPI method with {size} processes ===")
            for num_points in args.num_points:
                num_points = int(num_points)
                print(f"MPI: Testing {num_points} points...")
                mpi_result = self.mpi_version(num_points)
                if mpi_result and rank == 0:  # 只有rank 0收集结果
                    mpi_result['num_points'] = num_points
                    mpi_result['workers'] = size
                    results.append(mpi_result)
        
        # 只有rank 0运行其他方法
        if rank == 0:
            # Sequential方法 - 不需要workers参数
            print(f"\n=== Running Sequential method ===")
            for num_points in args.num_points:
                num_points = int(num_points)
                print(f"Sequential: Testing {num_points} points...")
                result = self.sequential(num_points)
                result['num_points'] = num_points
                result['workers'] = 1
                results.append(result)
            
            # NumPy方法 - 不需要workers参数
            print(f"\n=== Running NumPy method ===")
            for num_points in args.num_points:
                num_points = int(num_points)
                print(f"NumPy: Testing {num_points} points...")
                result = self.numpy_version(num_points)
                result['num_points'] = num_points
                result['workers'] = 1
                results.append(result)
            
            # Multiprocessing方法 - 测试不同points和workers组合
            print(f"\n=== Running Multiprocessing method ===")
            for num_points in args.num_points:
                num_points = int(num_points)
                for worker_count in args.workers:
                    print(f"Multiprocessing: Testing {num_points} points with {worker_count} workers...")
                    result = self.multiprocessing_version(num_points, worker_count)
                    result['num_points'] = num_points
                    result['workers'] = worker_count
                    results.append(result)
            
            # Concurrent Futures方法 - 测试不同points和workers组合
            print(f"\n=== Running Concurrent Futures method ===")
            for num_points in args.num_points:
                num_points = int(num_points)
                for worker_count in args.workers:
                    print(f"Concurrent Futures: Testing {num_points} points with {worker_count} workers...")
                    result = self.concurrent_futures_version(num_points, worker_count)
                    result['num_points'] = num_points
                    result['workers'] = worker_count
                    results.append(result)
            
            # Thread Executor方法 - 测试不同points和workers组合
            print(f"\n=== Running Thread Executor method ===")
            for num_points in args.num_points:
                num_points = int(num_points)
                for worker_count in args.workers:
                    print(f"Thread Executor: Testing {num_points} points with {worker_count} workers...")
                    result = self.thread_executor_version(num_points, worker_count)
                    result['num_points'] = num_points
                    result['workers'] = worker_count
                    results.append(result)

            # 只有rank 0绘制图表和输出结果
            if results:
                df = pd.DataFrame(results)
                print("\n" + "=" * 100)
                print("BENCHMARK RESULTS:")
                print("=" * 100)
                print(df.to_string(index=False))

                # 创建时间对比图 - 按方法分组
                plt.figure(figsize=(14, 8))
                methods = df['method'].unique()
                colors = plt.cm.tab10(np.linspace(0, 1, len(methods)))
                
                for i, method in enumerate(methods):
                    subset = df[df['method'] == method]
                    
                    # 使用 num_points 作为 x 轴，对于有多个 workers 的方法用不同标记
                    if len(subset['workers'].unique()) > 1:
                        # 有多个worker配置的方法，用不同标记区分
                        for worker in subset['workers'].unique():
                            worker_subset = subset[subset['workers'] == worker]
                            plt.plot(worker_subset['num_points'], worker_subset['time'], 
                                   marker='o', label=f"{method} ({worker}w)", 
                                   linewidth=2, markersize=6)
                    else:
                        # 只有一个worker配置的方法
                        plt.plot(subset['num_points'], subset['time'], 
                               marker='o', label=method, 
                               linewidth=2, color=colors[i], markersize=6)
                
                plt.xlabel("Number of Points")
                plt.ylabel("Time (micro seconds)")
                plt.title("Pi Calculation Benchmark - Time Comparison")
                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.grid(True, alpha=0.3)
                plt.xscale('log')  # x轴也用对数坐标
                plt.yscale('log')  # y轴用对数坐标
                plt.tight_layout()
                plt.savefig("pi_benchmark_time.png", dpi=300, bbox_inches='tight')
                print(f"\nTime comparison plot saved as 'pi_benchmark_time.png'")
                plt.close()

                # 创建误差对比图 - 按方法分组
                plt.figure(figsize=(14, 8))
                for i, method in enumerate(methods):
                    subset = df[df['method'] == method]
                    
                    if len(subset['workers'].unique()) > 1:
                        # 有多个worker配置的方法
                        for worker in subset['workers'].unique():
                            worker_subset = subset[subset['workers'] == worker]
                            plt.plot(worker_subset['num_points'], worker_subset['error'], 
                                   marker='x', label=f"{method} ({worker}w)", 
                                   linewidth=2, markersize=8)
                    else:
                        # 只有一个worker配置的方法
                        plt.plot(subset['num_points'], subset['error'], 
                               marker='x', label=method, 
                               linewidth=2, color=colors[i], markersize=8)

                plt.xlabel("Number of Points")
                plt.ylabel("Abs Pi Error")
                plt.title("Pi Calculation Benchmark - Error Comparison")
                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.grid(True, alpha=0.3)
                plt.xscale('log')  # x轴用对数坐标
                plt.yscale('log')  # y轴用对数坐标
                plt.tight_layout()
                plt.savefig("pi_benchmark_error.png", dpi=300, bbox_inches='tight')
                print(f"Error comparison plot saved as 'pi_benchmark_error.png'")
                plt.close()
                
                # 性能分析 - 按方法分组显示
                print("\n" + "=" * 100)
                print("PERFORMANCE ANALYSIS BY METHOD")
                print("=" * 100)
                
                for method in methods:
                    subset = df[df['method'] == method]
                    fastest = subset.loc[subset['time'].idxmin()]
                    most_accurate = subset.loc[subset['error'].idxmin()]
                    
                    print(f"\n{method}:")
                    print(f"  Fastest config: {int(fastest['num_points']):.0e} points, {fastest['workers']} workers ({fastest['time']:.4f}s)")
                    print(f"  Most accurate:  {int(most_accurate['num_points']):.0e} points, {most_accurate['workers']} workers (error: {most_accurate['error']:.2e})")
                
                # 整体最佳性能
                print(f"\n" + "=" * 80)
                print("OVERALL BEST PERFORMANCE")
                print("=" * 80)
                fastest_overall = df.loc[df['time'].idxmin()]
                most_accurate_overall = df.loc[df['error'].idxmin()]
                print(f"Fastest overall: {fastest_overall['method']} ({fastest_overall['time']:.4f}s)")
                print(f"Most accurate:   {most_accurate_overall['method']} (error: {most_accurate_overall['error']:.2e})")
        
        # 确保所有进程同步完成
        if MPI_AVAILABLE:
            comm.Barrier()
            
        return results if rank == 0 else None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pi calculation using various parallel methods')
    parser.add_argument("--num-points", type=float, nargs="+", default=[1e6])
    parser.add_argument("--workers", type=int, nargs="+", default=[1])
    args = parser.parse_args()
    
    calculator = PiCalculator()
    calculator.benchmark_all(args)
