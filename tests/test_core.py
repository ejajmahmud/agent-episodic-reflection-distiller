"""Unit tests for agent-episodic-reflection-distiller."""
import unittest
from agent_episodic_reflection_distiller.core import ReflectionDistiller, TrajectorySummary

class TestReflectionDistiller(unittest.TestCase):
    def setUp(self):
        self.distiller = ReflectionDistiller()

    def test_distill_port_error(self):
        t = TrajectorySummary("1", False, ["act"], "Error: port already in use")
        rules = self.distiller.distill([t])
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0].condition, "bind_failure_port_in_use")

    def test_distill_success_trajectory_produces_no_error_rules(self):
        t = TrajectorySummary("2", True, ["act1", "act2"])
        rules = self.distiller.distill([t])
        self.assertEqual(len(rules), 0)
