#
# Example of cloning a qubit that is currently in superposition to another qubit.
#

import qiskit
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from qiskit import IBMQ
from configparser import RawConfigParser

type = 'sim' # Run program on the simulator or real quantum machine.

def run(program, type, shots = 100):
  if type == 'real':
    global isInit
    if not run.isInit:
        # Setup the API key for the real quantum computer.
        parser = RawConfigParser()
        parser.read('config.ini')
        IBMQ.enable_account(parser.get('IBM', 'key'))
        run.isInit = True

    # Set the backend server.
    backend = qiskit.backends.ibmq.least_busy(qiskit.IBMQ.backends(simulator=False))

    # Execute the program on the quantum machine.
    print("Running on", backend.name())
    job = qiskit.execute(program, backend)
    return job.result().get_counts()
  else:
    # Execute the program in the simulator.
    print("Running on the simulator.")
    job = qiskit.execute(program, qiskit.Aer.get_backend('qasm_simulator'), shots=shots)
    return job.result().get_counts()

run.isInit = False

# Setup qubits.
qr = QuantumRegister(2)
cr = ClassicalRegister(2)
program = QuantumCircuit(qr, cr);

# Set the first qubit to 1; this is the value we want to clone to the second qubit.
program.x(qr[0]);

# Put the first qubit into superposition.
program.h(qr[0]);

# To clone this qubit to the second, first undo the superposition.
program.h(qr[0]);

# Perform a CNOT between the qubits to copy the value from the first to the second.
program.cx(qr[0], qr[1])

# Put the qubits back into superposition; the values are now cloned.
program.h(qr[0])
program.h(qr[1])

# Measure the value of the qubits to confirm they are equal. We do this by first taking them out of superposition to get the actual value, then measuring the result.
program.h(qr[0])
program.h(qr[1])
program.measure(qr, cr);

# Execute the program.
print(run(program, type))