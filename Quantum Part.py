import numpy as np
from random import randint
from math import log2, ceil
from scipy.linalg import block_diag

N = 4
n_qubits = ceil(log2(N))  # 2 ** n_qubits > N
M = 2 ** n_qubits
#a = randint(2, N)  # Random integer between 2 and N
a = 3
print(a)

phi = np.zeros(M, dtype=float)
phi[0] = 1.0  # Initial state |0⟩|0⟩


Hadamard = np.matrix([[1, 1], [1, -1]], dtype=float) / np.sqrt(2)
H = Hadamard
for i in range(0, n_qubits - 1):
    Hadamard = np.kron(Hadamard, H)

phi = np.dot(Hadamard, phi)
second_register = np.zeros(M, dtype=float)  # The size of the register is 2 * n_qubits
second_register[0] = 1
phi = np.kron(phi, second_register)


U = np.zeros((M*M, M*M))
for x in range(M):
    for y in range(M):
        input_state = x * M + y  # |x⟩|y⟩
        output_y = (y + pow(a, x, N)) % N
        output_state = x * M + output_y  # |x⟩|y ⊕ f(x)⟩
        U[output_state, input_state] = 1.0
print(U)

phi = phi.reshape((M ** 2, 1))
phi = np.dot(U, phi)
print(phi)
# phi = phi.reshape((M, M))
# phi = phi[:, 0]


def inverse_qft(m):
    IQFT = np.zeros((m, m), dtype=complex)
    for k in range(m):
        for l in range(m):
            theta = 2j * np.pi * k * l
            IQFT[k, l] = (1 / np.sqrt(m)) * np.exp(theta / m)
    return IQFT

I_second = np.eye(M)  # 4x4 identity for second register
IQFT_first = inverse_qft(M)  # 4x4 IQFT for first register
IQFT_total = np.kron(IQFT_first, I_second)  # 16x16 total IQFT operation

phi = IQFT_total @ phi
print("Final state:", phi)
print("Probabilities:", np.abs(phi))