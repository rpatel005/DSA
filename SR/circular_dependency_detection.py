from typing import List, Optional 
from dataclasses import dataclass 

def dfs_cycle_detection(graph, node, visited, path): 
    visited.append(node) # all the visited nodes in order
    path.append(node) # current path
    for child in graph[node]:
        if child not in visited:
            visited,path, isCycle = dfs_cycle_detection(graph, child, visited, path)
            if isCycle:
                return visited, path, True
        elif child in path: # child is visited and in path
            cycle = path[path.index(child):] + [child]
            return visited, cycle, True
        
    path.pop()
    return visited, path, False

@dataclass 
class Template: 
    id: str 
    inherits_from: List[str]  # IDs of parent templates 

def find_circular_dependency(templates: List[Template]) -> Optional[List[str]]: 
    """ 
    Detect circular inheritance and return the circular path. 
    Returns: 
    None if no circular dependency exists 
    List of template IDs forming the cycle (e.g., ["A", "B", 
    "C", "A"]) 
    """
    nodes = [n.id for n in templates] 
    graph = {n.id: n.inherits_from for n in templates}

    visited_forest_set = []
    cycle = []
    for n in nodes:
        if n not in visited_forest_set:
            temp, cycle_path, isCycle = dfs_cycle_detection(graph, n, visited=[], path = [])
            visited_forest_set.extend(temp)
            if isCycle:
                cycle.append(cycle_path)
           
    if len(cycle):
        return cycle
    else: return None


if __name__ == "__main__":
    # simple cycle
    templates = [
        Template("A", inherits_from=["B"]), 
        Template("B", inherits_from=["C"]), 
        Template("C", inherits_from=["A"]) 
        ] 
    result = find_circular_dependency(templates) # Output: ["A", "B", "C", "A"] 
    print("Simple cycle: ", result)
    
    # No cycle
    templates = [ 
        Template("A", inherits_from=["B"]), 
        Template("B", inherits_from=["C"]), 
        Template("C", inherits_from=[]) 
        ] 
    result = find_circular_dependency(templates) # Output: None 
    print("No cycle: ", result)

    # Self reference
    templates = [ 
        Template("A", inherits_from=["A"]) 
        ] 
    result = find_circular_dependency(templates) # Output: ["A", "A"] 
    print("Self reference: ", result)

    # Multiple inheritence with cycle
    templates = [ 
        Template("A", inherits_from=["B", "C"]), 
        Template("B", inherits_from=["D"]), 
        Template("C", inherits_from=["D"]), 
        Template("D", inherits_from=["A"]) 
        ] 
    result = find_circular_dependency(templates) # Output: ["A", "B", "D", "A"] or ["A", "C", "D", "A"] 
    print("Multiple inheritence with cycle: ", result)

    # Diamond (No Cycle - Valid) 
    templates = [ 
        Template("A", inherits_from=["B", "C"]), 
        Template("B", inherits_from=["D"]), 
        Template("C", inherits_from=["D"]), 
        Template("D", inherits_from=[]) 
        ] 
    result = find_circular_dependency(templates) # Output: None 
    print("Diamond (No Cycle - Valid): ", result)