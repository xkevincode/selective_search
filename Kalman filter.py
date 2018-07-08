# Kalman Filter exercises By Kevin X

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (10, 8)    # set size of pics

# initial params
n_iter = 500
sz = (n_iter, )     # size of array
x = -0.37727        # true value

# sample observations from norm distribution
z = np.random.normal(x, 0.1, size=sz)       # observations (normal about x, sigma=0.1)

Q = 1e-5    # process variance

# allocate space for arrays
xhat = np.zeros(sz)     # posteri estimate of x
P = np.zeros(sz)        # posteri error estimate
xhatminus = np.zeros(sz)    # prior estimate of x
Pminus = np.zeros(sz)       # prior error estimate
K = np.zeros(sz)            # gain or blending error


# estimate of measurement variance, change to see effect
R = 0.1

# posteri estimate is used as initial guess
xhat[0] = 0.0
P[0] = 1.0

for k in range(1, n_iter):
    # time update or prior update
    xhatminus[k] = xhat[k-1]
    Pminus[k] = P[k-1] + Q

    # measurement update
    K[k] = Pminus[k]/(Pminus[k]+R)
    xhat[k] = xhatminus[k] + K[k]*(z[k]-xhatminus[k])
    P[k] = (1-K[k])*Pminus[k]

plt.figure()
plt.plot(z,'k+', label = 'noisy measurement')
plt.plot(xhat,'b-', label = 'a posteri estimate')
plt.axhline(x, color='g', label='truth calue')
plt.legend()
plt.title('Estimate vs. iteration step', fontweight='bold')
plt.xlabel('Iteration')
plt.ylabel('Voltage')


# estimate of measurement variance, change to see effect
R = 1

# posteri estimate is used as initial guess
xhat[0] = 0.0
P[0] = 1.0

for k in range(1, n_iter):
    # time update or prior update
    xhatminus[k] = xhat[k-1]
    Pminus[k] = P[k-1] + Q

    # measurement update
    K[k] = Pminus[k]/(Pminus[k]+R)
    xhat[k] = xhatminus[k] + K[k]*(z[k]-xhatminus[k])
    P[k] = (1-K[k])*Pminus[k]

plt.figure()
plt.plot(z,'k+', label = 'noisy measurement')
plt.plot(xhat,'b-', label = 'a posteri estimate')
plt.axhline(x, color='g', label='truth calue')
plt.legend()
plt.title('Estimate vs. iteration step', fontweight='bold')
plt.xlabel('Iteration')
plt.ylabel('Voltage')


# plt.figure()
# valid_iter = range(1,n_iter) # Pminus not valid at step 0
# plt.plot(valid_iter,Pminus[valid_iter],label='a priori error estimate')
# # plt.title('Estimated $\it{\mathbf{a \ priori}}$ error vs. iteration step', fontweight='bold')
# plt.title('Estimated a  priori error vs. iteration step', fontweight='bold')
# plt.xlabel('Iteration')
# plt.ylabel('$(Voltage)^2$')
# plt.setp(plt.gca(),'ylim',[0,.01])

plt.show()








# print()