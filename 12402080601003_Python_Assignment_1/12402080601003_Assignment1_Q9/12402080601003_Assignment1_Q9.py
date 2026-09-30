# Assignment 1
# Question 9 - Threaded Job Scheduler Simulation

import threading
import heapq


# Store completed job information
results = []

# Protect shared data
results_lock = threading.Lock()


# Worker function
def worker(worker_id, assigned_jobs):

    for job in assigned_jobs:

        job_id, start_time, finish_time, waiting_time = job

        with results_lock:
            results.append(
                (
                    job_id,
                    worker_id,
                    start_time,
                    finish_time,
                    waiting_time
                )
            )


# Main function
def main():

    first_line = input().split()

    if len(first_line) != 2:
        print("INVALID")
        return

    try:
        w, n = map(int, first_line)
    except ValueError:
        print("INVALID")
        return

    if w < 1 or n < 1:
        print("INVALID")
        return

    jobs = []

    # Read job details
    for order in range(n):

        parts = input().split()

        if len(parts) != 5:
            print("INVALID")
            return

        try:
            arrival = int(parts[0])
            job_id = parts[1]
            priority = int(parts[2])
            duration = int(parts[3])
            resources = int(parts[4])
        except ValueError:
            print("INVALID")
            return

        if arrival < 0 or priority < 0:
            print("INVALID")
            return

        if duration < 1 or resources < 1:
            print("INVALID")
            return

        jobs.append(
            (
                arrival,
                -priority,
                order,
                job_id,
                duration,
                resources
            )
        )

    # Sort jobs by arrival time
    jobs.sort(key=lambda x: (x[0], x[2]))

    # Worker availability times
    worker_available = [0] * w

    # Jobs waiting to be assigned
    job_queue = []

    # Jobs assigned to each worker
    assigned_jobs = [[] for _ in range(w)]

    current_time = 0
    job_index = 0

    while job_index < n or job_queue:

        # Add all jobs that have arrived
        while job_index < n and jobs[job_index][0] <= current_time:

            arrival, negative_priority, order, job_id, duration, resources = jobs[job_index]

            heapq.heappush(
                job_queue,
                (
                    negative_priority,
                    arrival,
                    order,
                    job_id,
                    duration,
                    resources
                )
            )

            job_index += 1

        # Assign jobs to available workers
        assigned = False

        while job_queue:

            available_workers = [
                i for i in range(w)
                if worker_available[i] <= current_time
            ]

            if not available_workers:
                break

            # Lowest worker ID gets the job
            worker_index = min(available_workers)

            job = heapq.heappop(job_queue)

            negative_priority, arrival, order, job_id, duration, resources = job

            start_time = max(current_time, arrival)
            finish_time = start_time + duration
            waiting_time = start_time - arrival

            assigned_jobs[worker_index].append(
                (
                    job_id,
                    start_time,
                    finish_time,
                    waiting_time
                )
            )

            worker_available[worker_index] = finish_time

            assigned = True

        if assigned:
            continue

        # Find next important time
        next_times = []

        if job_index < n:
            next_times.append(jobs[job_index][0])

        if job_queue:
            next_times.extend(worker_available)

        if next_times:
            current_time = min(
                time for time in next_times
                if time > current_time
            )
        elif job_index < n:
            current_time = jobs[job_index][0]

    # Create worker threads
    threads = []

    for worker_index in range(w):

        thread = threading.Thread(
            target=worker,
            args=(
                worker_index + 1,
                assigned_jobs[worker_index]
            )
        )

        threads.append(thread)
        thread.start()

    # Wait for all workers
    for thread in threads:
        thread.join()

    # Sort results by job ID
    results.sort(key=lambda item: item[0])

    total_waiting = 0

    # Print execution report
    for job_id, worker_id, start_time, finish_time, waiting_time in results:

        print(
            job_id,
            f"W{worker_id}",
            start_time,
            finish_time
        )

        total_waiting += waiting_time

    average_waiting = total_waiting / n

    print(
        f"AVG_WAIT {average_waiting:.2f}"
    )


# Start program
if __name__ == "__main__":
    main()