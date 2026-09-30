# Assignment 1
# Question 6 - Python Module Dependency Resolver

import heapq


# Find lexicographically smallest loading order
def find_loading_order(modules, edges):

    graph = {module: [] for module in modules}
    indegree = {module: 0 for module in modules}

    # Build dependency graph
    for module_a, module_b in edges:

        if module_a not in graph[module_b]:
            graph[module_b].append(module_a)
            indegree[module_a] += 1
                        
             

    # Add modules with no dependency to heap
    heap = []

    for module in modules:
        if indegree[module] == 0:
            heapq.heappush(heap, module)

    order = []

    # Perform lexicographically smallest topological sort
    while heap:

        current = heapq.heappop(heap)
        order.append(current)

        for neighbour in graph[current]:

            indegree[neighbour] -= 1

            if indegree[neighbour] == 0:
                heapq.heappush(heap, neighbour)

    # Check for cycle
    if len(order) != len(modules):
        return None

    return order


# Find one cycle using DFS
def find_cycle(modules, edges):

    graph = {module: [] for module in modules}

    # Build graph
    for module_a, module_b in edges:

        if module_b not in graph[module_a]:
            graph[module_a].append(module_b)

    state = {module: 0 for module in modules}
    path = []
    position = {}

    # DFS for cycle detection
    def dfs(module):

        state[module] = 1
        position[module] = len(path)
        path.append(module)

        for neighbour in graph[module]:

            if state[neighbour] == 0:

                cycle = dfs(neighbour)

                if cycle:
                    return cycle

            elif state[neighbour] == 1:

                start = position[neighbour]

                return path[start:] + [neighbour]

        path.pop()
        position.pop(module, None)
        state[module] = 2

        return None

    # Check every module
    for module in sorted(modules):

        if state[module] == 0:

            cycle = dfs(module)

            if cycle:
                return cycle

    return []


# Main function
def main():

    try:

        # Read number of modules and imports
        first_line = input().split()

        if len(first_line) != 2:
            print("INVALID")
            return

        n = int(first_line[0])
        e = int(first_line[1])

        if n < 1 or e < 0:
            print("INVALID")
            return

        modules = set()

        # Read module names
        for _ in range(n):

            module = input().strip()

            if not module:
                print("INVALID")
                return

            modules.add(module)

        # Check duplicate module names
        if len(modules) != n:
            print("INVALID")
            return

        edges = []

        # Read import relationships
        for _ in range(e):

            parts = input().split()

            if len(parts) != 2:
                print("INVALID")
                return

            module_a = parts[0]
            module_b = parts[1]

            if (
                module_a not in modules
                or module_b not in modules
            ):
                print("INVALID")
                return

            edges.append(
                (module_a, module_b)
            )

        # Find loading order
        order = find_loading_order(
            modules,
            edges
        )

        if order is not None:

            print(" ".join(order))
            return

        # Find cycle
        cycle = find_cycle(
            modules,
            edges
        )

        print(
            "CYCLE",
            " ".join(cycle)
        )

    except (ValueError, EOFError):

        print("INVALID")

    except KeyboardInterrupt:

        print("\nProgram stopped by user.")


# Start program
if __name__ == "__main__":
    main()