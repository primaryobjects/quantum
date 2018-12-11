#
# The Deutsch Jozsh Algorithm: querying a oracle function that returns either 0 or 1 for all input values (constant) or returns exactly half 1 and half 0 for all input values (balanced).
# A single cpu cycle on a quantum computer can solve this problem, compared with the best classical computing algorithm solution.
#

import qiskit
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from qiskit import IBMQ
import numpy as np
from configparser import RawConfigParser

type = 'sim' # Run program on the simulator or real quantum machine.

def run(program, type, shots = 100):
  if type == 'real':
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

# Set the length of the input array to check.
n = 3

# Choose a random type and value for the oracle function.
oracleType = np.random.randint(2)
oracleValue = np.random.randint(2)

print("The oracle is constant.") if oracleType == 0 else print("The oracle is balanced.")

# Create n + 1 qubits for the input array, all initialized to zero, with an extra qubit for storing the answer.
qr = QuantumRegister(n + 1)
# Create n registers for the output.
cr = ClassicalRegister(n)
program = QuantumCircuit(qr, cr)

# Put all input qubits into superposition.
for i in range(n):
  program.h(qr[i])

# Invert the last qubit (which stores the answer) and place it into superposition.
program.x(qr[n])
program.h(qr[n])

# Apply a barrier to signify the start of the oracle process.
program.barrier()

if oracleType == 0:
  # This oracle is constant and returns oracleValue for all inputs.
  if oracleValue == 1:
    # Invert the answer qubit.
    program.x(qr[n])
  else:
    # Keep the answer qubit as-is.
    program.iden(qr[n])
else:
  # The oracle is balanced and returns equal counts of 0 and 1.
  for i in range(n):
    # Set the qubit to return the inner product of the input with a non-zero bitstring.
    if (n & (1 << i)):
      # Apply a controlled-not between the input qubit and the answer qubit.
      program.cx(qr[i], qr[n])

# Apply a barrier to signify the end of the oracle process.
program.barrier()

# Undo the superposition for all input qubits.
for i in range(n):
  program.h(qr[i])

# Measure the result of each input qubit. ???
program.barrier()
for i in range(n):
  program.measure(qr[i], cr[i])

# The outputs (of length n) will be all 0 for a constant oracle, otherwise they will contain 1's for balanced. On a real quantum machine, the majority vote will be all 0's (due to error noise) for a constant oracle, likewise contain a mix balance of 1's for a balanced.
# Simulator - The oracle is constant.
# {'000': 1024}
# Simulator - The oracle is balanced.
# {'011': 1024}
# Real quantum computer - The oracle is constant.
# {'110': 2, '000': 879, '100': 75, '010': 29, '101': 5, '011': 1, '001': 33}
# Real quantum computer - The oracle is balanced.
# {'100': 163, '111': 238, '010': 88, '101': 73, '011': 264, '001': 69, '110': 69, '000': 60}
print(run(program, type))
