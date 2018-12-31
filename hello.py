import qiskit
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from qiskit import IBMQ
from configparser import RawConfigParser

# Setup the API key for the real quantum computer.
parser = RawConfigParser()
parser.read('config.ini')
IBMQ.enable_account(parser.get('IBM', 'key'))

# Setup a qubit.
qr = QuantumRegister(1)
cr = ClassicalRegister(1)
program = QuantumCircuit(qr, cr);

# Measure the value of the qubit.
program.measure(qr, cr);

# Execute the program in the simulator.
print("Running on the simulator.")
job = qiskit.execute(program, qiskit.Aer.get_backend('qasm_simulator'), shots=100)
counts = job.result().get_counts()
print('Hello World! ' + str(counts))

# Execute the program on a real quantum computer.
backend = qiskit.providers.ibmq.least_busy(qiskit.IBMQ.backends(simulator=False))
print("Running on", backend.name())
job = qiskit.execute(program, backend, shots=100)
counts = job.result().get_counts()
print('Hello World! ' + str(counts))
