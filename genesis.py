
import json
import random
from pathlib import Path

STATE_FILE = Path("genesis_state.json")
LOG_FILE = Path("genesis_log.txt")

POPULATION_START = 40
GENERATIONS_PER_RUN = 100
WORLD_SIZE = 100
FOOD_PER_GENERATION = 35

def new_agent(agent_id, generation, genome=None):
    if genome is None:
        genome = {
            "efficiency": random.uniform(0.5, 1.5),
            "mobility": random.uniform(0.5, 1.5),
            "fertility": random.uniform(0.5, 1.5),
        }

    return {
        "id": agent_id,
        "generation": generation,
        "energy": 10.0,
        "age": 0,
        "genome": genome,
    }

def load_world():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())

    return {
        "generation": 0,
        "next_id": POPULATION_START,
        "agents": [
            new_agent(i, 0)
            for i in range(POPULATION_START)
        ],
        "history": [],
    }

def mutate(genome):
    child = {}
    for trait, value in genome.items():
        child[trait] = max(
            0.1,
            value + random.gauss(0, 0.08)
        )
    return child

def run_generation(world):
    generation = world["generation"] + 1
    agents = world["agents"]

    food = FOOD_PER_GENERATION

    for agent in agents:
        agent["age"] += 1
        genome = agent["genome"]

        food_found = (
            random.random()
            < min(0.95, 0.25 * genome["mobility"])
        )

        if food_found and food > 0:
            gain = 3.0 * genome["efficiency"]
            agent["energy"] += gain
            food -= 1

        agent["energy"] -= 1.0

    survivors = [
        a for a in agents
        if a["energy"] > 0 and a["age"] < 40
    ]

    offspring = []

    for parent in survivors:
        chance = min(
            0.8,
            0.08 * parent["genome"]["fertility"]
            * parent["energy"] / 10
        )

        if random.random() < chance:
            child = new_agent(
                world["next_id"],
                generation,
                mutate(parent["genome"])
            )
            world["next_id"] += 1
            child["energy"] = 8.0
            offspring.append(child)
            parent["energy"] -= 2.0

    world["agents"] = survivors + offspring
    world["generation"] = generation

    population = len(world["agents"])

    average = {
        trait: round(
            sum(a["genome"][trait] for a in world["agents"])
            / population, 3
        )
        if population else 0
        for trait in ["efficiency", "mobility", "fertility"]
    }

    record = {
        "generation": generation,
        "population": population,
        "average_traits": average,
    }

    world["history"].append(record)
    return record

def main():
    world = load_world()

    print("GENESIS LABORATORY")
    print("Starting generation:", world["generation"])

    for _ in range(GENERATIONS_PER_RUN):
        record = run_generation(world)

        if record["population"] == 0:
            print("EXTINCTION at generation",
                  record["generation"])
            break

    STATE_FILE.write_text(
        json.dumps(world, indent=2)
    )

    with LOG_FILE.open("a") as log:
        log.write(json.dumps(record) + "\n")

    print("Generation:", world["generation"])
    print("Population:", len(world["agents"]))
    print("Average traits:", record["average_traits"])
    print("State saved.")

if __name__ == "__main__":
    main()
  
