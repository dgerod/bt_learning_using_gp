from interface import implements
from behavior_tree_learning.sbt import BehaviorTreeExecutor, ExecutionParameters
from behavior_tree_learning.sbt import StringBehaviorTree, BehaviorNodeFactory
from behavior_tree_learning.gp import GeneticEnvironment
from duplo.world import WorldFactory
from duplo.fitness_function import FitnessFunction


class Environment(implements(GeneticEnvironment)):

    def __init__(self, node_factory: BehaviorNodeFactory, world_factory: WorldFactory,
                 target_positions,
                 static_tree=None, sm_pars=None, mode=0, fitness_coefficients=None, verbose=False):

        self._node_factory = node_factory
        self._world_factory = world_factory
        self._verbose = verbose

        self._targets = target_positions
        self._static_tree = static_tree
        self._fitness_coefficients = fitness_coefficients
        self._random_events = False

    def run_and_compute(self, individual, verbose):

        verbose_enabled = self._verbose or verbose

        sbt = list(individual)
        if verbose_enabled:
            print("SBT: ", sbt)

        world = self._world_factory.make()

        tree = StringBehaviorTree(sbt, behaviors=self._node_factory, world=world, verbose=verbose)
        success, ticks = tree.run_bt(parameters=ExecutionParameters(successes_required=1))
        fitness = FitnessFunction().compute_cost(world, tree, ticks, self._targets,
                                                 self._fitness_coefficients, verbose=verbose)

        if verbose_enabled:
            print("fitness: ", fitness)

        return fitness

    def plot_individual(self, path, plot_name, individual):
        """ Saves a graphical representation of the individual """

        sbt = list(individual)

        if self._static_tree is not None:
            tree = StringBehaviorTree(self._add_to_static_tree(sbt), behaviors=self._node_factory)
        else:
            tree = StringBehaviorTree(sbt[:], behaviors=self._node_factory)

        tree.save_figure(path, name=plot_name)


class Environment1(Environment):
    """ Test class for only running first target in list  """

    def __init__(self, node_factory: BehaviorNodeFactory, world_factory: WorldFactory,
                 target_positions,
                 static_tree=None, sm_pars=None, mode=0, fitness_coefficients=None, verbose=False):

        super().__init__(node_factory, world_factory,
                         target_positions,
                         static_tree, sm_pars, mode, fitness_coefficients, verbose)
        self._targets = [self._targets[0]]

    def get_fitness(self, individual):
        return super().get_fitness(self._add_to_static_tree(individual))


class Environment12(Environment):
    """ Test class for only running first two targets in list  """

    def __init__(self, node_factory: BehaviorNodeFactory, world_factory: WorldFactory,
                 target_positions,
                 static_tree=None, sm_pars=None, mode=0, fitness_coefficients=None, verbose=False):

        super().__init__(node_factory, world_factory,
                         target_positions,
                         static_tree, sm_pars, mode, fitness_coefficients, verbose)
        self._targets = self._targets[:2]

    def get_fitness(self, individual):
        return super().get_fitness(self._add_to_static_tree(individual))


class Environment123(Environment):
    """ Test class for only running first three targets in list  """

    def __init__(self, node_factory: BehaviorNodeFactory, world_factory: WorldFactory,
                 target_positions,
                 static_tree=None, sm_pars=None, mode=0, fitness_coefficients=None, verbose=False):

        super().__init__(node_factory, world_factory,
                         target_positions,
                         static_tree, sm_pars, mode, fitness_coefficients, verbose)
        self._targets = self._targets[:3]

    def get_fitness(self, individual):
        return super().get_fitness(self._add_to_static_tree(individual))
