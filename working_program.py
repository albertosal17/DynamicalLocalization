import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, execute
from qiskit_aer import AerSimulator

from quantumCircuit import qft_dagger, qft_rotations


def theta_k(jdx, kk):
    return -2*(np.pi**2)*kk /2**jdx + np.pi**2*kk/2**(2*jdx-1)

def theta_T(jdx, TT, NN):
    return 2*NN**2*TT/2**(jdx+2) - NN**2*TT/2**(2*jdx+1)

def phi_k(jdx1, jdx2, kk):
    return 2*np.pi**2*kk/2**(jdx1+jdx2-1)

def phi_T(jdx1, jdx2, TT, NN):
    return - 2*NN**2*TT/2**(jdx1+jdx2+1)

def map_application(qc, params):
    nq = qc.num_qubits

    # QFT
    qft_rotations(qc, nq)
    qc.barrier()
    # Position map
    for idx in range(nq):
        for jdx in range(idx, nq, 1):
            if idx == jdx:
                qc.p(theta_k(idx+1, params["k"]), idx)
                #print("theta_k", idx+1)
            else:
                qc.cp( phi_k(idx+1, jdx+1, params["k"]), idx, jdx)
                #print("phi_k", idx+1, jdx+1)
    qc.barrier()
    # QFT DAGGER
    qft_dagger(qc, nq)
    qc.barrier()
    for idx in range(nq):
        inv_idx = nq - idx
        for jdx in range(idx, nq, 1):
            inv_jdx = nq - jdx
            if idx == jdx:
                qc.p( theta_T(inv_idx, params["T"], 2**nq), idx )
                #print("theta_T", inv_idx, idx)
            else:
                qc.cp( phi_T(inv_idx, inv_jdx, params["T"], 2**nq), idx, jdx)
                #print("phi_T", inv_idx, idx,  inv_jdx, jdx)
    qc.barrier()

    return qc

# Number of qubits
nn = 3
# Something
params = {
    "k" : 0.273,
    "K" : 1.5,
}
params["T"] = params["K"]/params["k"]
params["L"] = params["T"]*2**nn/(2*np.pi)
print( params )
num_iters = 1


qc = QuantumCircuit(nn)

# Initialize in 0 momentum
qc.x(nn-1)

for iter in range(num_iters):
    qc = map_application(qc, params)

if num_iters == 1 and nn < 6:
    qc.draw("mpl")
    plt.show()

qc.save_state()

# Modify backend to use noisy/real QC.
# In that case go back to shots and not statevector
backend = AerSimulator(method="statevector")
statevector = execute(qc, backend).result()
statevector = statevector.get_statevector().__array__()

fig, ax = plt.subplots(figsize=(10, 6))
xx = np.arange(-2**(nn-1), 2**(nn-1))
pp =  statevector*np.conjugate(statevector)
mask = pp > 1e-6
ax.plot(xx[mask],  pp[mask] )
ax.set_yscale("log")
ax.axvline(0, ls='--', color="red")
plt.show()
