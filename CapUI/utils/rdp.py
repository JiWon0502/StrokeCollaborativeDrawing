# rdp algorithm
# line = LineString([(0,0),(1,0.1),(2,-0.1),(3,5),(4,6),(5,7),(6,8.1),(7,9),(8,9),(9,9)])
# print (line.simplify(1.0, preserve_topology=True)) -> preserve_topology must be true
from shapely.geometry import LineString

class RDP:
    def __init__(self):
        pass

    def raw_to_lines(raw, epsilon=0.5):
        result = []
        N = len(raw)
        for i in range(N):
            line = []
            rawline = raw[i]
            M = len(rawline[0])
            if M <= 2:
                continue
            for j in range(M):
                line.append([rawline[0][j], rawline[1][j]])
            line = LineString(line)
            line.simplify(2.0)
            result.append(line)
        return result
