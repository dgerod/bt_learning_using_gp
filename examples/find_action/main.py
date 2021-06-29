#!/usr/bin/env python3

import sys
import os

PACKAGE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.normpath(PACKAGE_DIRECTORY))

from interface import implements
from behavior_tree_learning.sbt import StringBehaviorTree
from behavior_tree_learning.sbt import BehaviorNodeFactory, BehaviorRegister
from behavior_tree_learning.sbt import World

from find_action.paths import EXAMPLE_DIRECTORY
from find_action.BT import behavior_tree_2 as sbt
from find_action.execution_nodes import Anchored, MoveArmTo, RetrieveObjects


class ExecutionParameters:
    
    def __init__(self, max_ticks=30, max_time=30.0, max_straight_fails=1, successes_required=2):
        
        self.max_ticks= max_ticks
        self.max_time = max_time 
        self.max_straight_fails = max_straight_fails
        self.successes_required = successes_required

class DummyWorld(implements(World)):

    def get_feedback(self):
        return True

    def send_references(self):
        pass


def run():

    print(sbt)

    behavior_register = BehaviorRegister()
    behavior_register.add_condition('CHECK_anchored[gear_1: gear]', Anchored)
    behavior_register.add_action('DO_move_arm_to[A: place]', MoveArmTo)
    behavior_register.add_action('DO_move_arm_to[B: place]', MoveArmTo)
    behavior_register.add_action('DO_move_arm_to[C: place]', MoveArmTo)
    behavior_register.add_action('DO_move_arm_to[D: place]', MoveArmTo)
    behavior_register.add_action('DO_move_arm_to[E: place]', MoveArmTo)
    behavior_register.add_action('DO_retrive_objects[] => [objects]', RetrieveObjects)
    node_factory = BehaviorNodeFactory(behavior_register)

    my_world = DummyWorld()
    tree = StringBehaviorTree(sbt, behaviors=node_factory, world=my_world)
    tree.save_figure(EXAMPLE_DIRECTORY, name='test')

    tree.run_bt(parameters=ExecutionParameters(successes_required=1))


if __name__ == "__main__":
    run()
