graph = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B"],
    "F": ["C"]
}

queue = ["A"]
visited = {"A"}  
parent = {}

def explore_once(graph, queue, visited):
    if not queue:
        print("Search Algorithm Complete.")
        return None
        
    current = queue.pop(0)
    print(f"Exploring node: {current}")
    
    for neighbor in graph[current]:
        if neighbor not in visited:
            visited.add(neighbor)
            queue.append(neighbor)
            parent[neighbor] = current 
            
    return current

while queue:
    explore_once(graph, queue, visited)

print(f"Final queue: {queue}")