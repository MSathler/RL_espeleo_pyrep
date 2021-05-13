import numpy as np
import matplotlib.pyplot as plt
from collections import deque




x = [ 51.0, 54.0, 58.0, 66.0, 71.33333333333333, 82.5, 70.0, 67.33333333333333, 73.5, 61.5, 60.0, 56.666666666666664, 67.5, 70.5, 75.0, 74.0, 77.33333333333333, 88.66666666666667, 112.5, 110.66666666666667, 124.5, 115.33333333333333, 126.5, 120.0, 124.0, 92.66666666666667, 91.33333333333333, 92.66666666666667, 97.5, 93.0, 96.0, 88.66666666666667, 104.0, 115.5, 127.5, 150.4, 164.0, 177.6, 190.4, 204.0, 233.42857142857142, 248.28571428571428, 268.0, 293.6363636363636, 311.5, 332.93333333333334, 358.6923076923077]

p = 0

    
mean2 = deque(maxlen=800)
mean = deque(maxlen=100)
read = []
a = []
b = []
for i in range(len(x)):
    
	read.append(x[i])
	mean.append(x[i])
	mean2.append(x[i])
	a.append(np.mean(mean))
	b.append(np.mean(mean2))
 
	if x[i] > 900:
		p+=1

      
print(p)
print(len(x))
	
plt.rc('axes',labelsize = 18)
plt.rc('xtick',labelsize = 15)
plt.rc('ytick',labelsize = 15)
plt.rc('legend',fontsize = 15)
plt.rc('axes',titlesize = 25)
plt.rc('legend',loc = 'lower left')
plt.ylim((0,400))
# plt.title('Coleta do Sensor')
plt.xlabel('Número de Passos')
plt.ylabel('Leitura do Sensor')
plt.plot(np.linspace(0,len(x) ,len(x),endpoint=False), np.asarray(x), color = 'blue', linewidth=2, label='Recompensa')
# plt.plot(np.linspace(0,len(a) ,len(a),endpoint=False), np.asarray(a), color='orange', linewidth=2, label='Média móvel (período = 100)')
# plt.plot(np.linspace(0,len(b) ,len(b),endpoint=False), np.asarray(b), color='red', linewidth=2)
# plt.scatter(np.arange(len(x)),x,color='blue',linewidths=0.1)
# print(max(b))
# print(max(a))
# plt.rc('axes',labelsize = 50)
# leg = plt.legend(loc="lower right")
# leg_line = leg.get_lines()
# plt.setp(leg_line, linewidth=5)
plt.show()


