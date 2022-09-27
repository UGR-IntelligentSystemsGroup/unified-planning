# Copyright 2021 AIPlan4EU project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License

import os
import tempfile
from typing import cast

import pytest
import unified_planning
from unified_planning.engines import PlanGenerationResultStatus
from unified_planning.io import PDDLReader, PDDLWriter
from unified_planning.io.hpdl_reader import HPDLReader
from unified_planning.model.problem_kind import full_numeric_kind
from unified_planning.model.types import _UserType
from unified_planning.shortcuts import *
from unified_planning.test import (
    TestCase,
    main,
    skipIfNoOneshotPlannerForProblemKind,
    skipIfNoOneshotPlannerSatisfiesOptimalityGuarantee,
)
from unified_planning.test.examples import get_example_problems

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
PDDL_DOMAINS_PATH = os.path.join(FILE_PATH, "pddl")


class TestHpdlIO(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        # self.problems = get_example_problems()

    def test_hpdl_reader(self):
        reader = HPDLReader()

        domain_filename = os.path.join(PDDL_DOMAINS_PATH, "hpdl", "domain.hpdl")
        problem_filename = os.path.join(PDDL_DOMAINS_PATH, "hpdl", "problem.hpdl")
        problem = reader.parse_problem(domain_filename, problem_filename)

        assert isinstance(problem, up.model.htn.HierarchicalProblem)
        self.assertEqual(10, len(problem.fluents))
        self.assertEqual(14, len(problem.actions))
        self.assertEqual(
            [
                "Turn",
                "turn_avatar",
                "turn_objects",
                "create",
                "check",
            ],
            [task.name for task in problem.tasks],
        )
        self.assertEqual(
            [
                "finish_game",
                "turn",
                "avatar_move_up",
                "avatar_move_down",
                "avatar_move_left",
                "avatar_move_right",
                "avatar_turn_up",
                "avatar_turn_down",
                "avatar_turn_left",
                "avatar_turn_right",
                "avatar_nil",
                "turn",
                "create",
                "base_case",
                "avatar_wall_stepback",
                "box_avatar_bounceforward",
                "box_wall_undoall",
                "box_box_undoall",
                "box_hole_killsprite",
                "base_case",
            ],
            [method.name for method in problem.methods],
        )
        self.assertEqual(1, len(problem.method("avatar_move_up").subtasks))
        self.assertEqual(4, len(problem.method("avatar_wall_stepback").subtasks))
        # self.assertEqual(2, len(problem.task_network.subtasks))