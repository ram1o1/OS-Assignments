import sys
import copy
import random

class Process:
    def __init__(self, pid, at, bt, priority, deadline):
        self.pid = pid
        self.at = at             # Arrival Time
        self.bt = bt             # Burst Time
        self.priority = priority # Priority (Lower number = Higher Priority)
        self.deadline = deadline # Deadline
        
        # Working variables
        self.remaining_bt = bt
        self.first_response_time = -1
        self.ct = 0              # Completion Time
        self.tat = 0             # Turnaround Time
        self.wt = 0              # Waiting Time
        self.rt = 0              # Response Time

class ScheduleResult:
    def __init__(self, algo_name, processes, cpu_utilization):
        self.algo_name = algo_name
        self.processes = processes
        self.cpu_util = cpu_utilization
        
        # Calculate Averages
        n = len(processes)
        self.avg_tat = sum(p.tat for p in processes) / n if n > 0 else 0
        self.avg_wt = sum(p.wt for p in processes) / n if n > 0 else 0
        self.avg_rt = sum(p.rt for p in processes) / n if n > 0 else 0

class CPUScheduler:
    def __init__(self):
        # Using SystemRandom for near-perfect random number generation
        self.rng = random.SystemRandom()

    def generate_processes(self, num_processes):
        processes = []
        for i in range(1, num_processes + 1):
            at = self.rng.randint(0, int(num_processes/2))
            bt = self.rng.randint(1, 20)
            priority = self.rng.randint(1, 10)
            deadline = at + bt + self.rng.randint(10, 50)
            processes.append(Process(i, at, bt, priority, deadline))
        return processes

    def _finalize_process(self, p, completion_time):
        p.ct = completion_time
        p.tat = p.ct - p.at
        p.wt = p.tat - p.bt
        p.rt = p.first_response_time - p.at

    def fcfs(self, processes):
        procs = sorted(copy.deepcopy(processes), key=lambda x: x.at)
        time = 0
        idle_time = 0

        for p in procs:
            if time < p.at:
                idle_time += (p.at - time)
                time = p.at
            
            p.first_response_time = time
            time += p.bt
            self._finalize_process(p, time)

        cpu_util = ((time - idle_time) / time) * 100 if time > 0 else 0
        procs.sort(key=lambda x: x.pid)
        return ScheduleResult("FCFS (Non-Preemptive)", procs, cpu_util)

    def sjf(self, processes):
        # Rule: In SJF there is no need for Arrival time. All jobs arrive at start.
        procs = copy.deepcopy(processes)
        for p in procs:
            p.at = 0 

        # Sort by Burst Time
        procs.sort(key=lambda x: (x.at, x.bt))
        time = 0

        for p in procs:
            p.first_response_time = time
            time += p.bt
            self._finalize_process(p, time)

        cpu_util = 100.0 # Since all arrive at 0, no idle time
        procs.sort(key=lambda x: x.pid)
        return ScheduleResult("SJF (Non-Preemptive, All AT=0)", procs, cpu_util)

    def srtn(self, processes):
        procs = copy.deepcopy(processes)
        time = 0
        completed = 0
        n = len(procs)
        idle_time = 0

        while completed != n:
            available = [p for p in procs if p.at <= time and p.remaining_bt > 0]
            
            if not available:
                idle_time += 1
                time += 1
                continue

            # Sort by remaining BT, then arrival time
            available.sort(key=lambda x: (x.remaining_bt, x.at))
            current = available[0]

            if current.first_response_time == -1:
                current.first_response_time = time

            current.remaining_bt -= 1
            time += 1

            if current.remaining_bt == 0:
                self._finalize_process(current, time)
                completed += 1

        cpu_util = ((time - idle_time) / time) * 100 if time > 0 else 0
        procs.sort(key=lambda x: x.pid)
        return ScheduleResult("SRTN (Preemptive SJF)", procs, cpu_util)

    def rr(self, processes, quantum):
        procs = sorted(copy.deepcopy(processes), key=lambda x: x.at)
        time = 0
        idle_time = 0
        queue = []
        completed = 0
        n = len(procs)
        idx = 0

        if idx < n and procs[idx].at == 0:
            while idx < n and procs[idx].at <= time:
                queue.append(procs[idx])
                idx += 1

        while completed != n:
            if not queue:
                if idx < n:
                    idle_time += (procs[idx].at - time)
                    time = procs[idx].at
                    while idx < n and procs[idx].at <= time:
                        queue.append(procs[idx])
                        idx += 1
                continue

            current = queue.pop(0)

            if current.first_response_time == -1:
                current.first_response_time = time

            execution_time = min(quantum, current.remaining_bt)
            
            time += execution_time
            current.remaining_bt -= execution_time

            # Add new arrivals to queue before re-queueing the current process
            while idx < n and procs[idx].at <= time:
                queue.append(procs[idx])
                idx += 1

            if current.remaining_bt > 0:
                queue.append(current)
            else:
                self._finalize_process(current, time)
                completed += 1

        cpu_util = ((time - idle_time) / time) * 100 if time > 0 else 0
        procs.sort(key=lambda x: x.pid)
        return ScheduleResult(f"Round Robin (Quantum={quantum})", procs, cpu_util)

    def priority_scheduling(self, processes):
        # Non-preemptive priority. Lower number = Higher priority
        procs = sorted(copy.deepcopy(processes), key=lambda x: x.at)
        time = 0
        completed = 0
        n = len(procs)
        idle_time = 0

        while completed != n:
            available = [p for p in procs if p.at <= time and p.remaining_bt > 0]
            
            if not available:
                next_at = min(p.at for p in procs if p.remaining_bt > 0)
                idle_time += (next_at - time)
                time = next_at
                continue

            available.sort(key=lambda x: (x.priority, x.at))
            current = available[0]

            current.first_response_time = time
            time += current.bt
            current.remaining_bt = 0
            
            self._finalize_process(current, time)
            completed += 1

        cpu_util = ((time - idle_time) / time) * 100 if time > 0 else 0
        procs.sort(key=lambda x: x.pid)
        return ScheduleResult("Priority (Non-Preemptive)", procs, cpu_util)

class OutputWriter:
    @staticmethod
    def write_process_data(filename, processes):
        with open(filename, 'w') as f:
            f.write("Randomly Generated Process Data\n")
            f.write("="*60 + "\n")
            f.write(f"{'PID':<5} | {'Arrival Time':<12} | {'Burst Time':<10} | {'Priority':<8} | {'Deadline':<8}\n")
            f.write("-" * 60 + "\n")
            for p in processes:
                f.write(f"{p.pid:<5} | {p.at:<12} | {p.bt:<10} | {p.priority:<8} | {p.deadline:<8}\n")

    @staticmethod
    def write_results(filename, results):
        with open(filename, 'w') as f:
            for res in results:
                f.write("="*80 + "\n")
                f.write(f"ALGORITHM: {res.algo_name}\n")
                f.write("="*80 + "\n")
                
                f.write(f"CPU Utilization: {res.cpu_util:.2f}%\n\n")

                f.write(f"{'PID':<5} | {'AT':<4} | {'BT':<4} | {'CT':<5} | {'TAT':<5} | {'WT':<5} | {'RT':<5}\n")
                f.write("-" * 50 + "\n")
                for p in res.processes:
                    f.write(f"{p.pid:<5} | {p.at:<4} | {p.bt:<4} | {p.ct:<5} | {p.tat:<5} | {p.wt:<5} | {p.rt:<5}\n")
                
                f.write("\n")
                f.write(f"Average Turn-Around Time: {res.avg_tat:.2f}\n")
                f.write(f"Average Waiting Time    : {res.avg_wt:.2f}\n")
                f.write(f"Average Response Time   : {res.avg_rt:.2f}\n\n")

def main():
    print("SVNIT, DoAI Operating System Lab")
    print("root# CPUSimulator")
    print("Hi! Welcome to CPU Scheduling Simulator. Please give me required parameters.")
    
    algo_choice = input("Scheduling algorithm – (1) FCFS (2) RR (3) SJF (4) SRTN (5) Priority (6) All\n> ")
    num_procs_input = input("No. of Processes in the system : ")
    
    try:
        choice = int(algo_choice)
        n = int(num_procs_input)
    except ValueError:
        print("Invalid input. Please enter numbers.")
        return

    print("Wait.... Generating Schedules...")

    scheduler = CPUScheduler()
    processes = scheduler.generate_processes(n)
    
    # Changed extension from .tex to .txt
    OutputWriter.write_process_data("process_data.txt", processes)

    results = []
    
    if choice in [1, 6]:
        results.append(scheduler.fcfs(processes))
    if choice in [2, 6]:
        results.append(scheduler.rr(processes, quantum=2))
        results.append(scheduler.rr(processes, quantum=4))
    if choice in [3, 6]:
        results.append(scheduler.sjf(processes))
    if choice in [4, 6]:
        results.append(scheduler.srtn(processes))
    if choice in [5, 6]:
        results.append(scheduler.priority_scheduling(processes))

    # Changed extension from .tex to .txt
    OutputWriter.write_results("Output.txt", results)
    
    print("DONE. Please check output file Output.txt for all the results.")

if __name__ == "__main__":
    main()