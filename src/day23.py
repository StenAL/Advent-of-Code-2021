import heapq
import queue
from typing import Iterable

from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 23


class Agent:
    def __init__(self, goal: str, location: str, move_cost):
        self.goal = goal
        self.location = location
        self.move_cost = move_cost


class Action:
    def __init__(self, agent: Agent, to: str, cost: int):
        self.agent = agent
        self.to = to
        self.cost = cost

    def __str__(self):
        return f"{self.agent.goal}: {self.agent.location}->{self.to} ({self.cost})"


def get_distance_map(reachability_map: dict[str, Iterable[str]], double_distance_rooms: Iterable[str]) -> dict[(str,
                                                                                                                str): int]:
    distance_map = {}
    for room in reachability_map:
        q = [(room, 0)]
        while len(q) > 0:
            (destination, distance) = q.pop(0)
            reachable = reachability_map[destination]
            for el in reachable:
                if room != el and (room, el) not in distance_map:
                    d = distance + 1
                    if {destination, el}.issubset(double_distance_rooms):
                        d = distance + 2
                    q.append((el, d))
                    distance_map[(room, el)] = d
    return distance_map


class State:

    def __init__(self, agents: set[Agent], cost: int, reachability_map, distance_map, room_depth):
        self.agents = agents
        self.cost = cost
        self.location_map: dict[str, Agent] = {agent.location: agent for agent in self.agents}
        self.reachability_map = reachability_map
        self.distance_map = distance_map
        self.room_depth = room_depth

    def __eq__(self, other):
        cost_eq = self.cost == other.cost
        agents = {(agent.location, agent.goal) for agent in self.agents}
        other_agents = {(agent.location, agent.goal) for agent in other.agents}
        return cost_eq and agents == other_agents

    def __lt__(self, other):
        return self.cost < other.cost

    def __hash__(self):
        agents = ((agent.location, agent.goal) for agent in self.agents)
        return hash((self.cost, agents))

    def is_agent_in_final_position(self, agent: Agent):
        if not agent.location.startswith(agent.goal):
            return False
        others_deeper_in_room = set()
        for i in range(self.room_depth):
            a = self.location_map.get(agent.goal + str(i + 1))
            if a is None or a == agent:
                continue
            if a.goal != agent.goal:
                return False
            if a.location > agent.location:
                others_deeper_in_room.add(a)

        return len(others_deeper_in_room) == self.room_depth - int(agent.location[-1])

    def get_reachable_locations(self, origin: str) -> set[str]:
        occupied_locations = self.location_map.keys()
        reachable_locations = set()
        q = [origin]
        while len(q) > 0:
            location = q.pop()
            r = self.reachability_map[location]
            for el in r:
                if el not in reachable_locations and el not in occupied_locations:
                    q.append(el)
                    reachable_locations.add(el)
        return reachable_locations

    def is_room_occupied_by_incorrect_agent(self, room: str) -> bool:
        agents_in_room = {self.location_map.get(room + str(i + 1)) for i in
                          range(self.room_depth)}
        return any(a is not None and a.goal != room for a in agents_in_room)

    def get_actions(self):
        actions = []
        for agent in self.agents:
            if self.is_agent_in_final_position(agent):
                continue

            reachable_locations = self.get_reachable_locations(agent.location)
            room_occupied_by_incorrect_agent = self.is_room_occupied_by_incorrect_agent(agent.goal)
            reachable_room_locations = {location for location in reachable_locations if
                                        location.startswith(agent.goal)}
            should_go_to_room = (not room_occupied_by_incorrect_agent) and len(reachable_room_locations) > 0

            if should_go_to_room:
                potential_destinations = {max(reachable_room_locations)}
            elif agent.location.startswith("H"):
                potential_destinations = set()
            else:
                potential_destinations = {location for location in reachable_locations if location.startswith("H")}

            for dest in potential_destinations:
                distance = self.distance_map[(agent.location, dest)]
                actions.append(Action(agent, dest, distance * agent.move_cost))
        return actions

    def apply(self, action: Action):
        agent = self.location_map[action.agent.location]
        del self.location_map[agent.location]
        self.location_map[action.to] = agent
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
                    cost += self.distance_map[(agent.location, agent.goal + "1")] * agent.move_cost
                else:
                    closest_hallway_distance = max(self.distance_map.values())
                    for i in range(1, 8):
                        d = self.distance_map[("H" + str(i), agent.location)] + self.distance_map[
                            ("H" + str(i), agent.goal + "1")]
                        closest_hallway_distance = min(d, closest_hallway_distance)
                    cost += closest_hallway_distance * agent.move_cost
        return cost


def search(state: State):
    q = [state]
    seen = set()
    best = 10000000000
    while len(q) > 0:
        state = q.pop()
        seen.add(state)
        if state.h() > best:
            continue
        print(len(q), best)
        if state.is_finished():
            best = min(best, state.cost)
        actions = state.get_actions()
        for action in actions:
            neighbor = State(copy.deepcopy(state.agents), state.cost, state.reachability_map, state.distance_map, state.room_depth)
            neighbor.apply(action)
            tentative_cost = neighbor.cost + neighbor.h()
            if neighbor not in seen and tentative_cost < best:
                q.append(neighbor)
    return best


def task1():
    data = get_input_for_day(day)
    data = get_input_for_file("test")
    agent_order = ["A1", "B1", "C1", "D1", "A2", "B2", "C2", "D2"]
    agent_index = 0
    move_costs = {"A": 1, "B": 10, "C": 100, "D": 1000}
    agents = set()

    for line in data:
        for c in line:
            if c in {"A", "B", "C", "D"}:
                agents.add(Agent(c, agent_order[agent_index], move_costs[c]))
                agent_index += 1

    reachability_map = {"H1": {"H2"}, "H2": {"H1", "H3", "A1"}, "H3": {"H2", "H4", "A1", "B1"},
                        "H4": {"H3", "H5", "B1", "C1"}, "H5": {"H4", "H6", "C1", "D1"}, "H6": {"H5", "H7", "D1"},
                        "H7": {"H6"}, "A1": {"A2", "H2", "H3"}, "B1": {"B2", "H3", "H4"}, "C1": {"C2", "H4", "H5"},
                        "D1": {"D2", "H5", "H6"}, "A2": {"A1"}, "B2": {"B1"}, "C2": {"C1"},
                        "D2": {"D1"}}

    double_distance_rooms = {"H2", "H3", "H4", "H5", "H6", "A1", "B1", "C1", "D1"}

    distance_map = get_distance_map(reachability_map, double_distance_rooms)

    starting_state = State(agents, 0, reachability_map, distance_map, 2)
    ans = search(starting_state)
    print(ans)


def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    data.extend(["#D#C#B#A#", "#D#B#A#C#"])
    agent_order = ["A1", "B1", "C1", "D1", "A4", "B4", "C4", "D4", "A2", "B2", "C2", "D2", "A3", "B3", "C3", "D3"]
    agent_index = 0
    move_costs = {"A": 1, "B": 10, "C": 100, "D": 1000}
    agents = set()

    for line in data:
        for c in line:
            if c in {"A", "B", "C", "D"}:
                agents.add(Agent(c, agent_order[agent_index], move_costs[c]))
                agent_index += 1


    reachability_map = {"H1": {"H2"}, "H2": {"H1", "H3", "A1"}, "H3": {"H2", "H4", "A1", "B1"},
                        "H4": {"H3", "H5", "B1", "C1"}, "H5": {"H4", "H6", "C1", "D1"}, "H6": {"H5", "H7", "D1"},
                        "H7": {"H6"}, "A1": {"A2", "H2", "H3"}, "B1": {"B2", "H3", "H4"}, "C1": {"C2", "H4", "H5"},
                        "D1": {"D2", "H5", "H6"}, "A2": {"A1", "A3"}, "B2": {"B1", "B3"}, "C2": {"C1", "C3"},
                        "D2": {"D1", "D3"}, "A3": {"A2", "A4"}, "B3": {"B2", "B4"}, "C3": {"C2", "C4"},
                        "D3": {"D2", "D4"},
                        "A4": {"A3"}, "B4": {"B3"}, "C4": {"C3"}, "D4": {"D3"}}

    double_distance_rooms = {"H2", "H3", "H4", "H5", "H6", "A1", "B1", "C1", "D1"}

    distance_map = get_distance_map(reachability_map, double_distance_rooms)

    starting_state = State(agents, 0, reachability_map, distance_map, 4)
    ans = search(starting_state)
    print(ans)


# task1()
task2()
