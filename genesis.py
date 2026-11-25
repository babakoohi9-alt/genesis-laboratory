import json
import random
from pathlib import Path

STATE_FILE = Path("genesis_state.json")
LOG_FILE = Path("genesis_log.jsonl")

POPULATION_START = 40
GENERATIONS_PER_RUN = 100
FOOD_PER_GENERATION = 35
STARTING_ENERGY = 10.0
OFFSPRING_ENERGY = 8.0
UPKEEP_PER_GENERATION = 1.0
REPRODUCTION_COST = 2.0
MAX_AGE = 40
MUTATION_SD = 0.08
TRAITS = ("efficiency", "mobility", "fertility")


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
        "energy": STARTING_ENERGY,
        "age": 0,
        "genome": dict(genome),
    }


def new_world(seed=None):
    if seed is not None:
        random.seed(seed)
    return {
        "generation": 0,
        "next_id": POPULATION_START,
        "agents": [new_agent(i, 0) for i in range(POPULATION_START)],
        "history": [],
        "seed": seed,
    }


def load_world():
    if STATE_FILE.exists():
        world = json.loads(STATE_FILE.read_text())
        required = {"generation", "next_id", "agents", "history"}
        if not required.issubset(world):
            raise ValueError("Saved Genesis state is missing required fields")
        return world
    return new_world()


def mutate(genome):
    return {
        trait: max(0.1, value + random.gauss(0, MUTATION_SD))
        for trait, value in genome.items()
    }


def trait_averages(agents):
    if not agents:
        return {trait: 0.0 for trait in TRAITS}
    return {
        trait: round(sum(a["genome"][trait] for a in agents) / len(agents), 4)
        for trait in TRAITS
    }


def run_generation(world):
    generation = world["generation"] + 1
    agents = list(world["agents"])
    random.shuffle(agents)

    food_remaining = FOOD_PER_GENERATION
    births = 0
    food_eaten = 0

    # Each agent gets one opportunity to find food. Food is a shared,
    # finite resource, so the order of foraging matters.
    for agent in agents:
        agent["age"] += 1
        genome = agent["genome"]
        finds_food = random.random() < min(0.95, 0.25 * genome["mobility"])

        if finds_food and food_remaining > 0:
            agent["energy"] += 3.0 * genome["efficiency"]
            food_remaining -= 1
            food_eaten += 1

        agent["energy"] -= UPKEEP_PER_GENERATION

    survivors = [
        agent for agent in agents
        if agent["energy"] > 0 and agent["age"] < MAX_AGE
    ]

    offspring = []
    for parent in survivors:
        chance = min(
            0.8,
            0.08 * parent["genome"]["fertility"] * parent["energy"] / 10.0,
        )
        # Pay the reproductive cost before creating offspring. An agent
        # must retain positive energy after paying it.
        if parent["energy"] > REPRODUCTION_COST and random.random() < chance:
            parent["energy"] -= REPRODUCTION_COST
            child = new_agent(
                world["next_id"],
                generation,
                mutate(parent["genome"]),
            )
            world["next_id"] += 1
            child["energy"] = OFFSPRING_ENERGY
            offspring.append(child)
            births += 1

    world["agents"] = survivors + offspring
    world["generation"] = generation

    population = len(world["agents"])
    record = {
        "generation": generation,
        "population": population,
        "survivors": len(survivors),
        "births": births,
        "food_eaten": food_eaten,
        "food_remaining": food_remaining,
        "average_traits": trait_averages(world["agents"]),
    }
    world["history"].append(record)
    return record


def save_world(world):
    temporary = STATE_FILE.with_suffix(".tmp")
    temporary.write_text(json.dumps(world, indent=2))
    temporary.replace(STATE_FILE)


def main():
    world = load_world()
    print("GENESIS LABORATORY")
    print("Starting generation:", world["generation"])

    last_record = None
    with LOG_FILE.open("a") as log:
        for _ in range(GENERATIONS_PER_RUN):
            last_record = run_generation(world)
            log.write(json.dumps(last_record) + "\n")
            if last_record["population"] == 0:
                print("EXTINCTION at generation", last_record["generation"])
                break

    save_world(world)
    print("Generation:", world["generation"])
    print("Population:", len(world["agents"]))
    if last_record is not None:
        print("Average traits:", last_record["average_traits"])
    print("State saved.")


if __name__ == "__main__":
    main()
