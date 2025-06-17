from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.gate import Gate
from qiskit.circuit.library import QFT


# Set up two registers of equal size
n_qubits = 4
reg1 = QuantumRegister(n_qubits, '|x⟩')
reg2 = QuantumRegister(n_qubits, '|y⟩')

# Classical register only for the first register
c_reg = ClassicalRegister(n_qubits, 'meas')

# Create circuit with both quantum registers and one classical register
qc = QuantumCircuit(reg1, reg2, c_reg)

for i in range(n_qubits):
    qc.h(reg1[i])  # Hadamard on reg1 qubits

# Oracle gate over the whole register
class OracleGate(Gate):
    def __init__(self, num_qubits):
        # Label showing the transformation: |x⟩|y⟩ → |x⟩|y⊕f(x)⟩
        label = "Oracle U\n|x⟩|y⟩ → |x⟩|y⊕f(x)⟩"
        super().__init__('Oracle', num_qubits, [], label=label)

# Add the oracle gate U to the circuit spanning both registers
U = OracleGate(2 * n_qubits)
qc.append(U, list(reg1) + list(reg2))

# IQFT gate on the 1st register only
qc.iqft = QFT(n_qubits, inverse=True)
qc.append(qc.iqft, reg1)

# Measure the first register
qc.measure(reg1, c_reg)

# Draw the circuit and save to images
qc.draw(output='mpl', filename='images/quantum_circuit.png')
