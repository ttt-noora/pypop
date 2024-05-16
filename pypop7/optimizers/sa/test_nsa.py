def test_optimize():
    import numpy  # engine for numerical computing
    from pypop7.benchmarks.base_functions import rosenbrock  # function to be minimized
    from pypop7.optimizers.sa.nsa import NSA
    problem = {'fitness_function': rosenbrock,  # define problem arguments
               'ndim_problem': 2,
               'lower_boundary': -5.0 * numpy.ones((2,)),
               'upper_boundary': 5.0 * numpy.ones((2,))}
    options = {'max_function_evaluations': 5000,  # set optimizer options
               'seed_rng': 2022,
               'x': 3 * numpy.ones((2,)),
               'sigma': 3.0,
               'temperature': 100}
    nsa = NSA(problem, options)  # initialize the optimizer class
    results = nsa.optimize()  # run the optimization process
    # return the number of function evaluations and best-so-far fitness
    print(f"NSA: {results['n_function_evaluations']}, {results['best_so_far_y']}")
