from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.gate import Gate
from qiskit.circuit.library import QFT


N = 3
reg1 = QuantumRegister(N, '1st Register')
reg2 = QuantumRegister(N, '2nd Register')
qc = QuantumCircuit(reg1, reg2)

for i in range(N):
    qc.h(reg1[i])  # Hadamard on reg1 qubits
    # qc.cu(reg1[i], reg2[i])  # Controlled U gate

# Oracle gate over the whole register
class OracleGate(Gate):
    def __init__(self, num_qubits):
        super().__init__('Oracle', num_qubits, [])

# Add the oracle gate U to the circuit spanning both registers
U = OracleGate(2 * N)
qc.append(U, list(reg1) + list(reg2))

# IQFT gate on the 1st register only
qc.iqft = QFT(N, inverse=True)
qc.append(iqft, reg1)

print(qc.draw())
