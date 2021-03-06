# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 22:34:53 2021

@author: 20210595
"""
import pygmo as pg
import numpy as np
# from pygmo import *
# from . import space_args
# from .import space_autogenerated
# from . import create_pipeline
# argsInput = space_args.space_args
# positionsPreprocessingTechniques = space_autogenerated.positionsPreprocessingTechniques
# EvaluateVector = create_pipeline.EvaluateVector

from space_args import NewUpperBound, NewlowerBound
from space_autogenerated import positionsPreprocessingTechniques
from create_pipeline import EvaluateVector

class AutoTSProblem:
    def __init__(self, serie, upperValues = NewUpperBound, lowerValues = NewlowerBound, positionsPreProceTech = positionsPreprocessingTechniques):
        self.serie = serie
        self.upperValues = upperValues
        self.lowerValues = lowerValues
        self.positionsPreProceTech = positionsPreProceTech
    # Define objectives
    def fitness(self, x):
        instanceClassEvaluation = EvaluateVector(self.serie)
        f1 = instanceClassEvaluation(x)
        listWithPositions = self.positionsPreProceTech
        listOfNumberOfMethodsToUse = [self._evaluateNumberOfPreProcessingMethods(x[i]) for i in listWithPositions]
        #Count the number of True in the vector listOfNumberOfMethodsToUse
        true_count = sum(listOfNumberOfMethodsToUse)
        f2 = true_count
        return [f1, f2]
        #f1 = x[0]**2
        #return [f1]

     # Return number of objectives
    def get_nobj(self):
        return 2

    def _evaluateNumberOfPreProcessingMethods(self, value):
        if value > 15:
            return True
        else:
            return False

    # Return bounds of decision variables
    def get_bounds(self):
        lower = self.lowerValues
        upper = self.upperValues
        #Exceptions:
        lower[0] = 16 #SimpleImputer
        upper[2] = max(self.serie) # 'SimpleImputer_fill_value'
        return (lower, upper)

    # Return function name
    def get_name(self):
        return "AutoTimeSeriesProblem"


def main(serie, generations=1000, pop_size=80):
    #a_cstrs_sa = pg.algorithm(pg.cstrs_self_adaptive(iters=generations))
    # select algorithm
    algo = pg.algorithm(pg.nsga2(gen=generations))
    # select problem
    prob = pg.problem(AutoTSProblem(serie))
    # create population
    pop = pg.population(prob, size=pop_size)
    # run optimization
    pop = algo.evolve(pop)
    fits, vectors = pop.get_f(), pop.get_x()
    # extract and print non-dominated fronts
    ndf, dl, dc, ndr = pg.fast_non_dominated_sorting(fits)
    print(ndf)
    first_objective_func = fits[:,0]
    index_min = min(range(len(first_objective_func)), key = first_objective_func.__getitem__)
    x_best = vectors[index_min]
    print(x_best)
    #print(f_best)
    np.savetxt("prueba.csv", pop.get_x(), delimiter=",")
    return x_best

# if __name__=='__main__':
#     main([1,2,3], generations = 20, pop_size = 40)



# np.savetxt("prueba.csv", pop.get_x(), delimiter=",")

# # create UDP
# prob = pg.problem(AutoMLProblem(20, 20))
# # create population
# pop = pg.population(prob, size=20)
# # select algorithm
# algo = pg.algorithm(pg.nsga2(gen=40))
# # run optimization
# pop = algo.evolve(pop)
# # extract results
# fits, vectors = pop.get_f(), pop.get_x()
# # extract and print non-dominated fronts
# ndf, dl, dc, ndr = pg.fast_non_dominated_sorting(fits)
# print(ndf) 


# #Multi-objective Hypervolume-based ACO (MHACO)

# algo = algorithm(maco(gen=100))
# algo.set_verbosity(20)
# # create UDP
# prob = pg.problem(AutoMLProblem(20, 20))
# pop = population(zdt(1), 200)
# pop = algo.evolve(pop) 
# uda = algo.extract(maco)
# uda.get_log() 
