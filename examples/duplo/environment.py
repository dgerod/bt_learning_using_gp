from dataclasses import dataclass
from interface import implements
from behavior_tree_learning.sbt import BehaviorTreeExecutor, ExecutionParameters
from behavior_tree_learning.sbt import StringBehaviorTree, BehaviorNodeFactory
from behavior_tree_learning.gp import GeneticEnvironment
from duplo.world import WorldSimulator
from duplo.fitness_function import FitnessFunction


class Environment(implements(GeneticEnvironment)):

    def __init__(self, node_factory: BehaviorNodeFactory, world: WorldSimulator,
                 target_positions,
                 static_tree=None, verbose=False, sm_pars=None, mode=0, fitness_coefficients=None):

        self._node_factory = node_factory
        self._world = world

        self._targets = target_positions
        self._static_tree = static_tree
        self._verbose = verbose
        self._sm_pars = sm_pars
        self._mode = mode
        self._fitness_coefficients = fitness_coefficients
        self._random_events = False

    def run_and_compute(self, individual):

        print('[Environment::run_and_compute] -- {')

        sbt = individual
        print("SBT: ", sbt)

        tree = StringBehaviorTree(sbt, behaviors=self._node_factory, world=self._world)
        success, ticks = tree.run_bt(parameters=ExecutionParameters(successes_required=1))

        fitness_value = FitnessFunction().compute_cost(self._world, tree, ticks, self._targets,
                                                       self._fitness_coefficients, verbose=self._verbose)
        print("fitness: ", fitness_value)

        print('} --')
        return fitness_value

    def plot_individual(self, path, plot_name, individual):
        """ Saves a graphical representation of the individual """

        if self._static_tree is not None:
            tree = StringBehaviorTree(self._add_to_static_tree(individual), behaviors=self._node_factory)
        else:
            tree = StringBehaviorTree(individual[:], behaviors=self._node_factory)

        tree.save_figure(path, name=plot_name)

    def set_random_events(self, random_events):
        """ Sets the random events flag """
        import pdb; pdb.set_trace()
        self._random_events = random_events

    def _add_to_static_tree(self, individual):
        """ Add invididual to the static part of the tree in the front """

        new_individual = self._static_tree[:]
        new_individual[-2:-2] = individual
        return new_individual


class Environment1(Environment):
    """ Test class for only running first target in list  """

    def __init__(self, targets, static_tree, verbose=False):
        super().__init__(targets, static_tree, verbose)
        self._targets = [self._targets[0]]

    def get_fitness(self, individual):
        return super().get_fitness(self._add_to_static_tree(individual))


class Environment12(Environment):
    """ Test class for only running first two targets in list  """

    def __init__(self, targets, static_tree, verbose=False):
        super().__init__(targets, static_tree, verbose)
        self._targets = self._targets[:2]

    def get_fitness(self, individual):
        return super().get_fitness(self._add_to_static_tree(individual))


class Environment123(Environment):
    """ Test class for only running first three targets in list  """

    def __init__(self, targets, static_tree, verbose=False):
        super().__init__(targets, static_tree, verbose)
        self._targets = self._targets[:3]

    def get_fitness(self, individual):
        return super().get_fitness(self._add_to_static_tree(individual))
