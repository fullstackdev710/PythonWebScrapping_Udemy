import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np

x = np.array([1, 2, 3, 4, 5])
y = [1, 4, 9, 16, 25]

slope, intercept, r_value, p_value, std_err = linregress(x, y)

plt.scatter(x, y)
plt.plot(x, slope * x + intercept, color='red')
plt.show()