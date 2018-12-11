import qiskit
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from qiskit import IBMQ
from configparser import RawConfigParser

type = 'sim' # Run program on the simulator or real quantum machine.

def run(program, type):
  if type == 'real':
    # Setup the API key for the real quantum computer.
    parser = RawConfigParser()
    parser.read('config.ini')
    IBMQ.enable_account(parser.get('IBM', 'key'))
    # Set the backend server.
    backend = qiskit.backends.ibmq.least_busy(qiskit.IBMQ.backends(simulator=False))
    # Execute the program on the quantum machine.
    print("Running on", backend.name())
    job = qiskit.execute(program, backend)
    return job.result().get_counts()
  else:
    # Execute the program in the simulator.
    print("Running on the simulator.")
    job = qiskit.execute(program, qiskit.Aer.get_backend('qasm_simulator'))
    return job.result().get_counts()

#
# Example 1: Measure 2 qubits in their initial state, all zeros.
#

# Setup qubits.
qr = QuantumRegister(2)
cr = ClassicalRegister(2)
program = QuantumCircuit(qr, cr);

# Measure the value of the qubits in their initial state, they should be all zeros.
program.measure(qr, cr);

# Execute the program.
print(run(program, type))

#
# Example 2: Create a Bell state (|00> + |11>), (|00> - |11>), (|01> + |10>), (|01> - |10>): Entangle 2 qubits, with the first in superposition (existing as 0 and 1 simulataneously or 50% chance of either value) and measure the results, they should be half 00 and half 11.
#

# Setup qubits.
qr = QuantumRegister(2)
cr = ClassicalRegister(2)
program = QuantumCircuit(qr, cr);

# Place the first qubit into a superposition, existing as both 0 and 1 simultaneously.
program.h(qr[0])

# Entangle the two qubits with a controlled NOT operator. If the first qubit is 1, the second qubit will be inverted. Depending on the initial qubit states, this results in the 4 Bell states (|00> + |11>), (|00> - |11>), (|01> + |10>), (|01> - |10>).
program.cx(qr[0], qr[1])

# Sender: Invert the first qubit to set it from 0 to 1 (remember, we're trying to represent 01 by manipulating only a single qubit q[0]).
# 00  I  - Identity nothing to do
# 01  X  - program.x(qr[0])
# 10  Z  - program.z(qr[0])
# 11  XZ - program.x(qr[0]) program.z(qr[0])
program.x(qr[0])

# Measure the value of the qubits, they should be equally 00 and 11, one of the Bell states.
program.measure(qr, cr);

# Execute the program.
print(run(program, type))

#
# Example 3: Superdense coding: send two classical bits of information (01) by only manipulating a single qubit: Reverse a Bell state: Entangle 2 qubits, with the first in superposition, then reverse the steps and measure the results, they should be all zeros.
# The first qubit is owned by Alice.
# The second qubit is owned by Bob.
# Alice will modify her qubit qr[0] in order to end up representing 01 to Bob, then send her qubit to him.
# Bob will reverse the entanglement and superposition of Alice's qubit and read the results, getting 01 from the qubits (his qubit miraculously turns into a 1).

# Setup qubits.
qr = QuantumRegister(2)
cr = ClassicalRegister(2)
program = QuantumCircuit(qr, cr);

# Sender: Place the first qubit into a superposition, existing as both 0 and 1 simulateneously.
program.h(qr[0])

# Sender: Entangle the two qubits with a controlled NOT operator. If the first qubit is 1, the second qubit will be inverted, otherwise it remains the same.
program.cx(qr[0], qr[1])

# Sender: Invert the first qubit to set it from 0 to 1 (remember, we're trying to represent 01 by manipulating only a single qubit q[0]).
# 00  I  - Identity nothing to do
# 01  X  - program.x(qr[0])
# 10  Z  - program.z(qr[0])
# 11  XZ - program.x(qr[0]) program.z(qr[0])
program.x(qr[0])

# Receiver: Repeat the controlled NOT operator, reversing the entanglement.
program.cx(qr[0], qr[1])

# Receiver: Repeat the Hadamard, reversing the superposition state.
program.h(qr[0])

# Receiver: Measure the value of the qubits, we should get back the original values.
program.measure(qr, cr);

# Execute the program.
print(run(program, type))