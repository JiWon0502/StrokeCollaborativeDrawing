import numpy as np

import numpy as np

def rdp(coords, epsilon):
    def distance(p1, p2):
        return np.linalg.norm(p2 - p1)

    def find_furthest_point(coords, start, end):
        dmax = 0
        index = 0
        for i in range(start+1, end):
            d = distance(coords[start], coords[end])
            if d > dmax:
                dmax = d
                index = i
        return index

    def rdp_recursive(coords, start, end, epsilon, simplified):
        if end > start + 1:
            index = find_furthest_point(coords, start, end)
            if distance(coords[start], coords[index]) > epsilon:
                simplified = rdp_recursive(coords, start, index, epsilon, simplified)
                simplified = rdp_recursive(coords, index, end, epsilon, simplified)
            else:
                simplified.append(coords[start])
                simplified.append(coords[end])
        return simplified

    simplified_coords = [coords[0]]
    simplified_coords = rdp_recursive(coords, 0, len(coords) - 1, epsilon, simplified_coords)
    simplified_coords.append(coords[-1])
    return np.array(simplified_coords)

# Example usage:
# Assuming 'deltas' is a list of delta coordinates (dx, dy) as tuples
# Convert it to a NumPy array of shape (n, 2)
# deltas = np.array(deltas)
# Apply RDP algorithm with epsilon=2.0
# simplified_deltas = rdp(deltas, epsilon=2.0)
