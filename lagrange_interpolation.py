import matplotlib.pyplot as plt
from scipy.signal import freqz

import numpy as np

window_len = 2**15

x = np.arange(window_len)
x = (4. * x / window_len) - 2
print(x)


y = 0*x
y += (x < -1) * (x+3) * (x+2) * (x+1) / 6
y += (x >= -1) * (x < 0) * (x+2) * (x+1) * (x-1) / -2
y += (x >= 0) * (x < 1) * (x+1) * (x-1) * (x-2) / 2
y += (x > 1) * (x-3) * (x-2) * (x-1) / -6

y2 = 0*x
y2 += (x >= -1) * (x < 0) * (x + 1)
y2 += (x >= 0) * (x < 1) * -1 * (x - 1)

f = np.linspace(0, 2)



plt.plot(x, y, label = "y")
plt.plot(x, y2, label = "y2")
plt.figure()

w,h = freqz(y, worN = f, fs = window_len/4)
h = 10 * np.log10(h * np.conjugate(h))
h /= h[0]
plt.plot(w,h, label = "y")

w,h = freqz(y2, worN = f, fs = window_len/4)
h = 10 * np.log10(h * np.conjugate(h))
h /= h[0]
plt.plot(w,h, label = "y2")

ls = [1024, 512,256,128,64,32,16,8,4]

for l in ls:
    f = 1./l

    ofs = np.array([-f, f])
    fs = np.array([-f, f])

    for i in range(1, 100):
        fs = np.concatenate((fs, ofs + i), axis = None)

    w,h = freqz(y, worN = fs, fs = window_len/4)
    h = h * np.conjugate(h)
    print("poly", l, 10 * np.log10((h[0] + h[1])/ np.sum(h[2:])))

    w,h = freqz(y2, worN = fs, fs = window_len/4)
    h = h * np.conjugate(h)
    print("tri", l, 10 * np.log10((h[0] + h[1])/ np.sum(h[2:])))

plt.show()