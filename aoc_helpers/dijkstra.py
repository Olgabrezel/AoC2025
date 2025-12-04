from math import inf
import heapq
from typing import List, Dict, Optional, Self, TypeVar, Union
from functools import total_ordering


class DijkstraEdge:
    def __init__(self, to_node, weight: Union[int, float]):
        self.to_node = to_node
        self.weight = weight


T_Id = TypeVar('T_Id')


@total_ordering
class DijkstraNode:
    def __init__(self, identifier: T_Id):
        self.identifier = identifier
        self.edges: List[DijkstraEdge] = []
        self.dist: Union[int, float] = inf
        self.predecessors: List[Self] = []

    def __eq__(self, other: Self):
        return isinstance(other, DijkstraNode) and (self.identifier == other.identifier)

    def __lt__(self, other: Self):
        return self.dist < other.dist


def compute_shortest_path(nodes: Dict[T_Id, DijkstraNode], start_id: T_Id, end_ids: Optional[List[T_Id]] = None):
    """
    Runs Dijkstra algorithm on the graph given by nodes. Input should be dict[identifier, node].
    If end_ids is specified, the path from start_id to one of end_ids is computed and returned as a list.
    Otherwise, distances to all nodes in the graph are computed and nothing is returned.
    The distances and predecessors can then be accessed in the node class.
    """
    nodes[start_id].dist = 0
    Q = []
    enqueued = set()

    for node in nodes.values():
        heapq.heappush(Q, node)
        enqueued.add(node.identifier)

    while len(Q) > 0:
        u = heapq.heappop(Q)
        enqueued.remove(u.identifier)

        if (end_ids is not None) and (u.identifier in end_ids):
            break

        for e in u.edges:
            if e.to_node.identifier in enqueued:
                new_dist = u.dist + e.weight
                if new_dist < e.to_node.dist:
                    e.to_node.dist = new_dist
                    e.to_node.predecessors = [u]
                    heapq._siftdown(Q, 0, Q.index(e.to_node))
                elif new_dist == e.to_node.dist:
                    e.to_node.predecessors.append(u)

    if end_ids is not None:
        u = min(nodes[end_id] for end_id in end_ids)
        path = [u]
        while len(u.predecessors) > 0:
            u = u.predecessors[0]
            path.append(u)
        path.reverse()
        return path
