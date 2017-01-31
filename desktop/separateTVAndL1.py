import numpy as np
import cvxpy as cvx
import matplotlib.pyplot as plt

def separateTVAndL1(M, sp, max_iters=30):
    """
    separate matrix m into smooth and sparse components
    M: 2-d ndarray
    sp:strength of sparseness
    max_iters: maximum number of iterations
    """
    
    m = M.shape[0]
    n = M.shape[1]

    L = cvx.Variable(m,n)
    S = cvx.Variable(m,n)

    #ob = cvx.Minimize(cvx.norm(L,'nuc') + 0.05*cvx.norm(S, 1))
    ob = cvx.Minimize(cvx.tv(L) + sp*cvx.norm(S, 1))

    co = [M == L + S]

    prob = cvx.Problem(ob, co)

    result = prob.solve(solver='SCS', max_iters=30);

    return L.value, S.value

if __name__ == "__main__":
    L, S = separateTVAndL1(np.ones((100,100)), 0.2, 30)
    plt.imshow(S, cmap='gray');
    plt.colorbar();
    plt.show();
