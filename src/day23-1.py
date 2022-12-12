import heapq
import queue

from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 23

move_costs = {"A": 1, "B": 10, "C": 100, "D": 1000}


class Agent:
    def __init__(self, goal: str, location: str):
        self.goal = goal
        self.location = location
        self.move_cost = move_costs[goal]


class Action:
    def __init__(self, agent: Agent, to: str, cost: int):
        self.agent = agent
        self.to = to
        self.cost = cost

    def __str__(self):
        return f"{self.agent.goal}: {self.agent.location}->{self.to} ({self.cost})"


reachability_map = {"H1": {"H2"}, "H2": {"H1", "H3", "A1"}, "H3": {"H2", "H4", "A1", "B1"},
                    "H4": {"H3", "H5", "B1", "C1"}, "H5": {"H4", "H6", "C1", "D1"}, "H6": {"H5", "H7", "D1"},
                    "H7": {"H6"}, "A1": {"A2", "H2", "H3"}, "B1": {"B2", "H3", "H4"}, "C1": {"C2", "H4", "H5"},
                    "D1": {"D2", "H5", "H6"}, "A2": {"A1"}, "B2": {"B1"}, "C2": {"C1"},
                    "D2": {"D1"}}

distance_map = {
    ("H1", "A1"): 3, ("H1", "A2"): 4, ("H1", "B1"): 5, ("H1", "B2"): 6, ("H1", "C1"): 7, ("H1", "C2"): 8,
    ("H1", "D1"): 9, ("H1", "D2"): 10,
    ("H2", "A1"): 2, ("H2", "A2"): 3, ("H2", "B1"): 4, ("H2", "B2"): 5, ("H2", "C1"): 6, ("H2", "C2"): 7,
    ("H2", "D1"): 8, ("H2", "D2"): 9,
    ("H3", "A1"): 2, ("H3", "A2"): 3, ("H3", "B1"): 2, ("H3", "B2"): 3, ("H3", "C1"): 4, ("H3", "C2"): 5,
    ("H3", "D1"): 6, ("H3", "D2"): 7,
    ("H4", "A1"): 4, ("H4", "A2"): 5, ("H4", "B1"): 2, ("H4", "B2"): 3, ("H4", "C1"): 2, ("H4", "C2"): 3,
    ("H4", "D1"): 4, ("H4", "D2"): 5,
    ("H5", "A1"): 6, ("H5", "A2"): 7, ("H5", "B1"): 4, ("H5", "B2"): 5, ("H5", "C1"): 2, ("H5", "C2"): 3,
    ("H5", "D1"): 2, ("H5", "D2"): 3,
    ("H6", "A1"): 9, ("H6", "A2"): 8, ("H6", "B1"): 7, ("H6", "B2"): 6, ("H6", "C1"): 5, ("H6", "C2"): 4,
    ("H6", "D1"): 3, ("H6", "D2"): 2,
    ("H7", "A1"): 10, ("H7", "A2"): 9, ("H7", "B1"): 8, ("H7", "B2"): 7, ("H7", "C1"): 6, ("H7", "C2"): 5,
    ("H7", "D1"): 4, ("H7", "D2"): 3
}


class State:

    def __init__(self, agents: set[Agent], cost: int):
        self.agents = agents
        self.cost = cost

    def __eq__(self, other):
        cost_eq = self.cost == other.cost
        agents = {(agent.location, agent.goal) for agent in self.agents}
        other_agents = {(agent.location, agent.goal) for agent in other.agents}
        return cost_eq and agents == other_agents

    def __lt__(self, other):
        return True

    def __hash__(self):
        agents = ((agent.location, agent.goal) for agent in self.agents)
        return hash(self.cost) * hash(agents)

    def is_agent_in_final_position(self, agent: Agent):
        if agent.location == agent.goal + "2":
            return True
        other = next(a for a in self.agents if a.goal == agent.goal and a != agent)
        return other.location == agent.goal + "2" and agent.location == agent.goal + "1"

    def get_reachable_locations(self, origin: str) -> set[str]:
        occupied_locations = {agent.location for agent in self.agents}
        reachable_locations = set()
        q = [origin]
        while len(q) > 0:
            location = q.pop()
            r = reachability_map[location]
            for el in r:
                if el not in reachable_locations and el not in occupied_locations:
                    q.append(el)
                    reachable_locations.add(el)
        return reachable_locations

    def get_agent_in_location(self, location: str) -> str | None:
        a = [agent for agent in self.agents if agent.location == location]
        if len(a) == 1:
            return a[0].goal
        return None

    def get_actions(self):
        neighbors: dict[str, list[str]] = defaultdict(list)
        for el in distance_map.keys():
            neighbors[el[1]].append(el[0])
            neighbors[el[0]].append(el[1])
        actions = []
        for agent in self.agents:
            if self.is_agent_in_final_position(agent):
                continue
            neighboring = neighbors[agent.location]
            if not agent.location.startswith("H"):
                potential_destinations = {location for location in neighboring if location.startswith("H")}
            else:
                potential_destinations = {location for location in neighboring if location.startswith(agent.goal)}

            reachable_destinations = self.get_reachable_locations(agent.location)
            potential_destinations = potential_destinations.intersection(reachable_destinations)

            # don't go to A1 if A2 is occupied by B or C or D
            if self.get_agent_in_location(agent.goal + "2") != agent.goal:
                potential_destinations.discard(agent.goal + "1")
            # don't go to A1 if A2 is free
            if agent.goal + "2" in potential_destinations:
                potential_destinations.discard(agent.goal + "1")

            # print(agent.goal, potential_destinations)
            for dest in potential_destinations:
                distance = distance_map[(agent.location, dest)] if (agent.location, dest) in distance_map else distance_map[
                    (dest, agent.location)]
                actions.append(Action(agent, dest, distance * agent.move_cost))
        actions = sorted(actions, key=lambda a: a.cost)
        # print([str(a) for a in actions])
        return actions

    def apply(self, action: Action):
        agent = next(agent for agent in self.agents if action.agent.location == agent.location)
        agent.location = action.to
        self.cost += action.cost

    def print(self):
        locations = defaultdict(lambda: " ")
        for agent in self.agents:
            locations[agent.location] = agent.goal
        print("█████████████")
        print(
            f"█{locations['H1']}{locations['H2']} {locations['H3']} {locations['H4']} {locations['H5']} {locations['H6']}{locations['H7']}█")
        print(f"███{locations['A1']}█{locations['B1']}█{locations['C1']}█{locations['D1']}███")
        print(f"  █{locations['A2']}█{locations['B2']}█{locations['C2']}█{locations['D2']}█  ")
        print("  █████████  ")

    def is_finished(self):
        for agent in self.agents:
            if not agent.location.startswith(agent.goal):
                return False
        return True

    def h(self):
        cost = 0
        for agent in self.agents:
            if not self.is_agent_in_final_position(agent):
                if agent.location.startswith("H"):
                    cost += distance_map[(agent.location, agent.goal + "1")] * agent.move_cost
                else:
                    closest_hallway_distance = 20
                    closest_hallway = "H1"
                    for i in range(1, 8):
                        d = distance_map[("H" + str(i), agent.location)] + distance_map[("H" + str(i), agent.goal + "1")]
                        if d < closest_hallway_distance:
                            closest_hallway_distance = min(d, closest_hallway_distance)
                            closest_hallway = "H" + str(i)
                    cost += closest_hallway_distance * agent.move_cost
        return cost


def search(state: State):
    q = [(state.h(), state)]
    while len(q) > 0:
        (priority, state) = heapq.heappop(q)
        print(len(q), priority)
        if state.is_finished():
            return priority
        actions = state.get_actions()
        for action in actions:
            neighbor = copy.deepcopy(state)
            neighbor.apply(action)
            tentative_cost = neighbor.cost + neighbor.h()
            heapq.heappush(q, (tentative_cost, neighbor))



def task1():
    # data = get_input_for_day(day)
    # data = get_input_for_file("test")
    """
        #############
        #...........#
        ###D#A#A#D###
          #C#C#B#B#
          #########
        ^ my data
        v example
        #############
        #...........#
        ###B#C#B#D###
          #A#D#C#A#
          #########
    """
    agents = {Agent("A", "B1"), Agent("A", "C1"), Agent("B", "C2"), Agent("B", "D2"), Agent("C", "A2"),
              Agent("C", "B2"), Agent("D", "A1"), Agent("D", "D1")}
    # agents = {Agent("A", "A2"), Agent("A", "D2"), Agent("B", "A1"), Agent("B", "C1"), Agent("C", "B1"),
    #           Agent("C", "C2"), Agent("D", "B2"), Agent("D", "D1")}
    starting_state = State(agents, 0)
    # starting_state.print()
    # print(starting_state.h())
    ans = search(starting_state)
    print(ans)

def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")


task1()
# task2()
