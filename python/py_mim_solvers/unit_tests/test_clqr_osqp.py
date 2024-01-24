import pathlib
import os
python_path = pathlib.Path('.').absolute().parent
os.sys.path.insert(1, str(python_path))

import numpy as np
import matplotlib.pyplot as plt
from csqp import CSQP

from clqr_problem import create_clqr_problem

LINE_WIDTH = 100

problem, xs_init, us_init = create_clqr_problem()


ddp1 = CSQP(problem, "CustomOSQP")
ddp2 = CSQP(problem, "OSQP")

ddp1.with_callbacks = True
ddp2.with_callbacks = True

max_qp_iters = 10000
ddp1.max_qp_iters = max_qp_iters
ddp2.max_qp_iters = max_qp_iters

eps_abs = 1e-8
eps_rel = 0.
ddp1.eps_abs = eps_abs
ddp2.eps_abs = eps_abs

converged = ddp1.solve(xs_init, us_init, 1)
converged = ddp2.solve(xs_init, us_init, 1)


assert ddp1.qp_iters == ddp2.qp_iters

set_tol = 1e-8
assert np.linalg.norm(np.array(ddp1.xs) - np.array(ddp2.xs)) < set_tol, "Test failed"
assert np.linalg.norm(np.array(ddp1.us) - np.array(ddp2.us)) < set_tol, "Test failed"
assert np.linalg.norm(np.array(ddp1.lag_mul) - np.array(ddp2.lag_mul)) < set_tol, "Test failed"
for t in range(len(ddp1.y)):
    assert np.linalg.norm(ddp1.y[t] - ddp2.y[t]) < set_tol, "Test failed"