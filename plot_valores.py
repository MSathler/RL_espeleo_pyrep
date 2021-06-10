import numpy as np
import matplotlib.pyplot as plt
from collections import deque




x = [129.0, 122.0, 149.6, 142.5, 164.57142857142858, 124.66666666666667, 145.6, 148.66666666666666, 118.0, 135.0, 123.33333333333333, 127.33333333333333, 147.0, 148.5, 148.5, 178.0, 152.66666666666666, 181.0, 192.0, 194.4, 207.0, 215.33333333333334, 223.66666666666666, 230.0, 239.71428571428572, 256.0, 253.42857142857142, 257.42857142857144, 270.6666666666667, 272.44444444444446, 290.0, 306.72727272727275, 329.875, 345.5]

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


