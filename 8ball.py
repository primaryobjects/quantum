import qiskit
from qiskit import IBMQ, ClassicalRegister, QuantumRegister, QuantumCircuit, execute, Aer
from qiskit.providers.ibmq import least_busy
from configparser import RawConfigParser

# Setup the API key for the real quantum computer.
parser = RawConfigParser()
parser.read('config.ini')
IBMQ.enable_account(parser.get('IBM', 'key'))

# Setup 3 qubits.
q = QuantumRegister(3)
c = ClassicalRegister(3)
qc = QuantumCircuit(q, c)

# Place the qubits into superposition so the qubits no longer hold a distinct value, but instead are both 0 and 1 at the same time (50% 0, 50% 1).
qc.h(q)
qc.measure(q, c)

# Using the qubits and their random value, form a response.
def answer(result):
	for key in result.keys():
		state = key
	print("The Quantum 8-ball says:")
	if state == '000':
		print('It is certain.')
	elif state == '001':
		print('Without a doubt.')
	elif state == '010':
		print('Yes - deinitely.')
	elif state == '011':
		print('Most likely.')
	elif state == '100':
		print("Don't count on it.")
	elif state == '101':
		print('My reply is no.')
	elif state == '110':
		print('Very doubtful.')
	else:
		print('Concentrate and ask again.')

# Execute the job on the simulator.
job = execute(qc, backend=Aer.get_backend('qasm_simulator'), shots=1)
result = job.result().get_counts(qc)
answer(result)

# Execute the program on a real quantum computer.
backend = least_busy(IBMQ.backends(simulator=False))
print("Running on", backend.name())
job = execute(qc, backend, shots=1)
result = job.result().get_counts(qc)
answer(result)