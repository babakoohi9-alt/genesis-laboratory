import unittest
from unittest.mock import patch

import genesis


class GenesisTests(unittest.TestCase):
    def test_new_world_has_expected_population(self):
        world = genesis.new_world(seed=123)
        self.assertEqual(len(world["agents"]), genesis.POPULATION_START)
        self.assertEqual(world["generation"], 0)

    def test_generation_advances_and_records_population(self):
        world = genesis.new_world(seed=123)
        record = genesis.run_generation(world)
        self.assertEqual(world["generation"], 1)
        self.assertEqual(record["generation"], 1)
        self.assertEqual(record["population"], len(world["agents"]))
        self.assertGreaterEqual(record["food_eaten"], 0)
        self.assertLessEqual(record["food_eaten"], genesis.FOOD_PER_GENERATION)

    def test_reproduction_cost_is_paid_before_birth(self):
        world = {
            "generation": 0,
            "next_id": 1,
            "agents": [{
                "id": 0,
                "generation": 0,
                "energy": 20.0,
                "age": 0,
                "genome": {"efficiency": 1.0, "mobility": 1.0, "fertility": 100.0},
            }],
            "history": [],
        }
        with patch.object(genesis.random, "shuffle", lambda items: None), \
             patch.object(genesis.random, "random", lambda: 0.0):
            record = genesis.run_generation(world)
        self.assertEqual(record["births"], 1)
        self.assertGreater(world["agents"][0]["energy"], 0)

    def test_empty_population_is_handled(self):
        world = {"generation": 0, "next_id": 0, "agents": [], "history": []}
        record = genesis.run_generation(world)
        self.assertEqual(record["population"], 0)
        self.assertEqual(record["average_traits"], {
            "efficiency": 0.0, "mobility": 0.0, "fertility": 0.0
        })


if __name__ == "__main__":
    unittest.main()
