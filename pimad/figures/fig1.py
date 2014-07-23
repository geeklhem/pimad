import numpy as np
import matplotlib.pyplot as plt
import scipy.misc as sp

f = plt.gcf()
f.set_size_inches((4,2))
ax = plt.gca()

T=1000
x = np.linspace(0,T,T)

z=1/3.0
y = [(sp.comb(T,k) * z**k * (1-z)**(T-k)) for k in x]
y[1] = 1-z
plt.plot(x,y,color="red",label="$\hat{z}_1=1/3$")

ax.annotate(r'$1-\hat{z}_1$', xy=(0,1-z),xycoords="data", textcoords="offset points", xytext=(+40,0),
arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))


z=2/3.0
y = [(sp.comb(T,k) * z**k * (1-z)**(T-k)) for k in x]
y[1] = 1-z
plt.plot(x,y,color="blue",label="$\hat{z}_2=2/3$")

ax.annotate(r'$1-\hat{z}_2$', xy=(0,1-z),xycoords="data", textcoords="offset points", xytext=(+40,0),
arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
#ax.annotate(r'$\hat{z}T$', xy=(z*T,0),xycoords="data", textcoords="offset points", xytext=(-5,-20),
#arrowprops=dict(arrowstyle="-", connectionstyle="arc3,rad=.2"))

ax.axis([-5,T,0,1-0.33+0.1])
ax.spines['right'].set_color("none")
ax.spines['top'].set_color("none")
ax.xaxis.set_ticks([1/3.0*T,2/3.0*T])
ax.set_xticklabels([r'$\hat{z}_1T$',r'$\hat{z}_2T$'])
ax.yaxis.set_ticks([])
ax.xaxis.set_ticks_position('bottom')
ax.xaxis.set_label_coords(.45, -0.025)
ax.set_xlabel("Group size")
ax.set_ylabel("Density")
plt.legend()
plt.show()

