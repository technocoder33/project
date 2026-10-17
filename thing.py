graph = {     
    "A": {"B": 2, "C": 5},     
    "B": {"A": 2, "D": 3},     
    "C": {"A": 5, "D": 1},     
    "D": {"B": 3, "C": 1},  
    "E": {} 
}  

graph["A"]["C"] = 1 
graph["C"]["A"] = 1  

graph["D"]["E"] = 4 
graph["E"]["D"] = 4  

def relax_neighbors(graph, distances, parent, current):     
    for neighbor, weight in graph[current].items():         
        new_distance = distances[current] + weight          
        if new_distance < distances[neighbor]:             
            distances[neighbor] = new_distance             
            parent[neighbor] = current  

def find_closest_unvisited(distances, visited):     
    best_node = None     
    best_distance = float("inf")      
    for node, distance in distances.items():         
        if node not in visited and distance < best_distance:             
            best_node = node             
            best_distance = distance      
    return best_node  

def reconstruct_route(parent, start, end):     
    if start == end:
        return [start]
        
    current = end     
    route = []      
    while current != start:         
        route.append(current)         
        current = parent[current]      
    route.append(start)     
    route.reverse()      
    return route  

def dijkstra(graph, start):     
    distances = {}      
    for node in graph:         
        distances[node] = float("inf")      
    distances[start] = 0      
    visited = set()     
    parent = {}      
    
    while True:         
        current = find_closest_unvisited(distances, visited)         
        if current is None:             
            break          
        relax_neighbors(graph, distances, parent, current)          
        visited.add(current)      
    return distances, parent  

def find_shortest_route(graph, start, end):
    if start not in graph or end not in graph:
        return None, None

    distances, parent = dijkstra(graph, start)      
    if distances[end] == float("inf"):         
        return float("inf"), None      
    route = reconstruct_route(parent, start, end)      
    return distances[end], route   

print(find_shortest_route(graph, "A", "E"))
print(find_shortest_route(graph, "A", "A"))
print(find_shortest_route(graph, "A", "Z"))
