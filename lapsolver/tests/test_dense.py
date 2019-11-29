import pytest
import numpy as np
import lapsolver as lap

def test_small():
    costs = np.array([[6, 9, 1],[10, 3, 2],[8, 7, 4.]], dtype=np.float32)    
    r = lap.solve_dense(costs)
    expected = np.array([[0, 1, 2], [2, 1, 0]])
    np.testing.assert_allclose(r, expected)

    costs = np.array([[6, 9, 1],[10, 3, 2],[8, 7, 4.]], dtype=float)    
    r = lap.solve_dense(costs)
    expected = np.array([[0, 1, 2], [2, 1, 0]])
    np.testing.assert_allclose(r, expected)

    costs = np.array([[6, 9, 1],[10, 3, 2],[8, 7, 4.]], dtype=int)    
    r = lap.solve_dense(costs)
    expected = np.array([[0, 1, 2], [2, 1, 0]])
    np.testing.assert_allclose(r, expected)

def test_plain_array():
    costs = [[6, 9, 1],[10, 3, 2],[8, 7, 4.]]
    r = lap.solve_dense(costs)
    expected = np.array([[0, 1, 2], [2, 1, 0]])
    np.testing.assert_allclose(r, expected)

def test_nonsquare():
    costs = np.array([[6, 9],[10, 3],[8, 7]], dtype=float)
    
    r = lap.solve_dense(costs)
    expected = np.array([[0, 1], [0, 1]])
    np.testing.assert_allclose(r, expected)

    r = lap.solve_dense(costs.T) # view test
    expected = np.array([[0, 1], [0, 1]])
    np.testing.assert_allclose(r, expected)

    costs = np.array(
        [[ -17.13614455, -536.59009819],
        [ 292.64662837,  187.49841358],
        [ 664.70501771,  948.09658792]])

    expected = np.array([[0, 1], [1, 0]])
    r = lap.solve_dense(costs)
    np.testing.assert_allclose(r, expected)

def test_views():
    costs = np.array([[6, 9],[10, 3],[8, 7]], dtype=float)
    np.testing.assert_allclose(lap.solve_dense(costs.T[1:, :]), [[0], [1]])

def test_large():
    costs = np.random.uniform(size=(5000,5000))
    r = lap.solve_dense(costs)

def test_solve_nan():
    costs = np.array([[5, 9, np.nan],[10, np.nan, 2],[8, 7, 4.]])
    r = lap.solve_dense(costs)
    expected = np.array([[0, 1, 2], [0, 2, 1]])
    np.testing.assert_allclose(r, expected)

def test_solve_inf():
    costs = np.array([[5, 9, np.inf],[10, np.inf, 2],[8, 7, 4.]])
    r = lap.solve_dense(costs)
    expected = np.array([[0, 1, 2], [0, 2, 1]])
    np.testing.assert_allclose(r, expected)

def test_missing_edge_negative():
    costs = np.array([[-1000, -1], [-1, np.nan]])
    r = lap.solve_dense(costs)
    # The optimal solution is (0, 1), (1, 0) with cost -1 + -1.
    # If the implementation does not use a large enough constant, it may choose
    # (0, 0), (1, 1) with cost -1000 + L.
    expected = np.array([[0, 1], [1, 0]])
    np.testing.assert_allclose(r, expected)

def test_missing_edge_positive():
    costs = np.array([
        [np.nan, 1000, np.nan],
        [np.nan, 1, 1000],
        [1000, np.nan, 1],
    ])
    costs_copy = costs.copy()
    r = lap.solve_dense(costs)
    # The optimal solution is (0, 1), (1, 2), (2, 0) with cost 1000 + 1000 + 1000.
    # If the implementation does not use a large enough constant, it may choose
    # (0, 0), (1, 1), (2, 2) with cost (L + 1 + 1) instead.
    expected = np.array([[0, 1, 2], [1, 2, 0]])
    np.testing.assert_allclose(r, expected)
