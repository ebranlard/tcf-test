import numpy as np
import matplotlib.pyplot as plt

import yaml

with open('Main_Spar.SD.sum') as f:
    t=yaml.load(f)
for k,v in t.items():
    if isinstance(v,list):
        t[k]=np.array(t)
print(t)
import pdb; pdb.set_trace()





# N=np.loadtxt('Nodes.csv')
# PhiR=np.loadtxt('PhiR.csv')
# PhiM=np.loadtxt('PhiM.csv')
# 
# zz=N[:,2]
# z=np.concatenate((zz[0:2],zz[3:]))
# print(z)
# print(z.shape)
# print(PhiR.shape)
# print(PhiM.shape)
# 
# n=6
# Ux=PhiR[0::n,:]
# Uy=PhiR[1::n,:]
# Uz=PhiR[2::n,:]
# Vx=PhiR[3::n,:]
# Vy=PhiR[4::n,:]
# Vz=PhiR[5::n,:]
# 
# 
# nGuy =PhiR.shape[1]
# 
# fig=plt.figure()
# fig.set_size_inches(12, 4)
# for j in np.arange(nGuy):
#     ax=fig.add_subplot(1,nGuy,j+1)
#     ax.plot(z, Ux[:,j],'+', label='Ux')
#     ax.plot(z, Uy[:,j],'+', label='Uy')
#     ax.plot(z, Uz[:,j],'+', label='Ux')
#     ax.plot(z, Vx[:,j],'o', label='Vy')
#     ax.plot(z, Vy[:,j],'o', label='Vz')
#     ax.plot(z, Vz[:,j],'o', label='Vz')
#     ax.set_title('Guyan mode '+str(j+1))
#     ax.legend()
# fig.savefig('GuyanModes.png')
# 
# 
# nCB=np.max([4,PhiM.shape[1]])
# 
# 
# # --- CB modes
# n=6
# Ux=PhiM[0::n,:]
# Uy=PhiM[1::n,:]
# Uz=PhiM[2::n,:]
# Vx=PhiM[3::n,:]
# Vy=PhiM[4::n,:]
# Vz=PhiM[5::n,:]
# 
# 
# fig=plt.figure()
# fig.set_size_inches(12, 4)
# for j in np.arange(nCB):
#     ax=fig.add_subplot(1,nCB,j+1)
#     ax.plot(z, Ux[:,j],'+', label='Ux')
#     ax.plot(z, Uy[:,j],'+', label='Uy')
#     ax.plot(z, Uz[:,j],'+', label='Ux')
#     ax.plot(z, Vx[:,j],'o', label='Vy')
#     ax.plot(z, Vy[:,j],'o', label='Vz')
#     ax.plot(z, Vz[:,j],'o', label='Vz')
#     ax.set_title('CB mode '+str(j+1))
#     ax.legend()
# fig.savefig('CBModes.png')
# 
# plt.show()
