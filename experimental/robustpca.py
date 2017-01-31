import numpy as np
import numpy.linalg as alg
import matplotlib.pyplot as plt
import cvxpy as cvx

from PIL import Image
from PIL import ImageOps

orig_img = Image.open('looseleaf_ss.jpg')
gray_img = ImageOps.grayscale(orig_img);

m = gray_img.size[1]
n = gray_img.size[0]

L = cvx.Variable(m,n)
S = cvx.Variable(m,n)
#np.random.seed()
#M = np.random.rand(n,n) + np.ones((n,n))
M = np.array(gray_img)
M = M / np.max(M)

#ob = cvx.Minimize(cvx.norm(L,'nuc') + 0.05*cvx.norm(S, 1))
ob = cvx.Minimize(cvx.tv(L) + 0.2*cvx.norm(S, 1))

co = [M == L + S]

prob = cvx.Problem(ob, co)

result = prob.solve(solver='SCS', max_iters=30);

maxval = 1.0
imcolor = 'gray'

plt.figure(0)
plt.subplot(2,2,1)
plt.imshow(M, interpolation='nearest', vmin=0.0, vmax=maxval, cmap=imcolor)
plt.title('M')
plt.colorbar()

plt.subplot(2,2,2)
plt.imshow(L.value, interpolation='nearest', vmin=0.0, vmax=maxval,cmap=imcolor)
plt.title('L')
plt.colorbar()

plt.subplot(2,2,3)
plt.imshow(L.value+S.value, interpolation='nearest', vmin=0.0, vmax=maxval, cmap=imcolor)
plt.title('M (reconstructed)')
plt.colorbar()

plt.subplot(2,2,4)
plt.imshow(S.value, interpolation='nearest', vmin=np.min(S.value), vmax=np.max(S.value), cmap=imcolor)
plt.title('S')
plt.colorbar()


print("cond(L) = " + str(alg.cond(L.value)))
print("cond(S) = " + str(alg.cond(S.value)))


plt.show()
