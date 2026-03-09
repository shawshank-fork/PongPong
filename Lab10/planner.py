import heapq   # used for priority queue (min heap) required in A* search

# Task dictionary representing a directed graph
# Each task has a duration and a list of dependencies
tasks = {
    'A': {'duration': 3, 'deps': []},
    'B': {'duration': 8, 'deps': ['A']},
    'C': {'duration': 2, 'deps': ['A']},
    'D': {'duration': 3, 'deps': ['B']},
    'E': {'duration': 1, 'deps': ['C']}
}

# Heuristic function for A* search
# It estimates the remaining cost by summing durations of tasks not yet completed
def heuristic(completed):
    remaining = [tasks[t]['duration'] for t in tasks if t not in completed]
    return sum(remaining)


# Function to find tasks that can be executed at the current state
# A task is available if:
# 1. It is not already completed
# 2. All its dependencies are completed
def available_tasks(completed):

    avail = []

    for task in tasks:

        # Skip tasks already completed
        if task not in completed:

            # Check if all dependencies are satisfied
            if all(dep in completed for dep in tasks[task]['deps']):
                avail.append(task)

    return avail


# A* Scheduler implementation
def astar_scheduler():

    # Start state
    # f_cost = 0 initially
    # completed_tasks = empty
    # g_cost = 0 (time spent so far)
    start = (0, [], 0)

    pq = []   # priority queue
    heapq.heappush(pq, start)

    visited = set()   # to avoid revisiting the same state

    while pq:

        # Pop the state with the smallest f_cost
        f, completed, g = heapq.heappop(pq)

        # Convert list to tuple because sets cannot store lists
        completed_tuple = tuple(completed)

        # Skip if already visited
        if completed_tuple in visited:
            continue

        visited.add(completed_tuple)

        # Goal condition: if all tasks are completed
        if len(completed) == len(tasks):
            return completed, g

        # Expand the node by exploring available tasks
        for task in available_tasks(completed):

            # Create a new state with this task completed
            new_completed = completed + [task]

            # Update total cost so far
            new_cost = g + tasks[task]['duration']

            # Estimate remaining cost using heuristic
            h = heuristic(new_completed)

            # Total estimated cost
            f_new = new_cost + h

            # Push the new state into priority queue
            heapq.heappush(pq, (f_new, new_completed, new_cost))


# Greedy Scheduler
# Chooses the task with the smallest duration among available tasks
def greedy_scheduler():

    completed = []   # list of completed tasks
    total_time = 0   # total execution time

    while len(completed) < len(tasks):

        # Find tasks that can be executed
        avail = available_tasks(completed)

        # Pick the task with minimum duration
        next_task = min(avail, key=lambda x: tasks[x]['duration'])

        # Add task to completed list
        completed.append(next_task)

        # Add its duration to total time
        total_time += tasks[next_task]['duration']

    return completed, total_time


# Run A* scheduler
astar_order, astar_time = astar_scheduler()

# Run Greedy scheduler
greedy_order, greedy_time = greedy_scheduler()


# Print results
print("A* Optimal Schedule:")
print("Order:", astar_order)
print("Total Time:", astar_time)

print("\nGreedy Schedule:")
print("Order:", greedy_order)
print("Total Time:", greedy_time)