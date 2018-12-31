#
# Grover's Search algorithm in quantum computing.
# Brute-force password cracking by taking an n-bit code and checking against an oracle function until the correct code is found.
# Unlike a traditional computer that would require 2^n-1 calls in the worst-case scenario, a quantum algorithm can solve this task in sqrt(2^n) calls.
# A code of 64 bits could take a classical computer hundreds of years to solve, while a quantum computer could solve it in just a few seconds.
#
# This example uses a simple code of just 2 bits: 00, 01, 10, 11
# In this case, we'll choose 01 as our secret code.
# The oracle function knows the code. How fast can your algorithm break it?
#
# Reference: http://kth.diva-portal.org/smash/get/diva2:1214481/FULLTEXT01.pdf
# Appendix A.2
#

import qiskit
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from qiskit import IBMQ
import numpy as np
import operator
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
    backend = qiskit.providers.ibmq.least_busy(qiskit.IBMQ.backends(simulator=False))

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

def oracle(program, password):
  # Find all bits with a value of 0.
  indices = np.where(password == 0)[0]

  # Invert the bits associated with a value of 0.
  for i in range(len(indices)):
    # We want to read bits, starting with the right-most value as index 0.
    index = int(len(password) - 1 - indices[i])
    # Invert the qubit.
    program.x(qr[index])

# Choose a random code for the oracle function.
password = np.random.randint(2, size=4)

# Convert the password array into an array of strings.
passwordStrArr = np.char.mod('%d', password)
# Convert the array of strings into a single string for display.
passwordStr = ''.join(passwordStrArr)
# Display the password.
print("The oracle password is " + passwordStr + ".")

# Create 2 qubits for the input array.
qr = QuantumRegister(4)
# Create 2 registers for the output.
cr = ClassicalRegister(4)
program = QuantumCircuit(qr, cr)

# Place the qubits into superposition to represent all possible values.
program.h(qr)

# Run oracle on key. Invert the 0-value bits.
oracle(program, password)

# Apply Grover's algorithm with a triple controlled Pauli Z-gate (cccZ).
program.cu1(np.pi / 4, qr[0], qr[3])
program.cx(qr[0], qr[1])
program.cu1(-np.pi / 4, qr[1], qr[3])
program.cx(qr[0], qr[1])
program.cu1(np.pi/4, qr[1], qr[3])
program.cx(qr[1], qr[2])
program.cu1(-np.pi/4, qr[2], qr[3])
program.cx(qr[0], qr[2])
program.cu1(np.pi/4, qr[2], qr[3])
program.cx(qr[1], qr[2])
program.cu1(-np.pi/4, qr[2], qr[3])
program.cx(qr[0], qr[2])
program.cu1(np.pi/4, qr[2], qr[3])

# Reverse the inversions by the oracle.
oracle(program, password)

# Amplification.
program.h(qr)
program.x(qr)

# Apply Grover's algorithm with a triple controlled Pauli Z-gate (cccZ).
program.cu1(np.pi/4, qr[0], qr[3])
program.cx(qr[0], qr[1])
program.cu1(-np.pi/4, qr[1], qr[3])
program.cx(qr[0], qr[1])
program.cu1(np.pi/4, qr[1], qr[3])
program.cx(qr[1], qr[2])
program.cu1(-np.pi/4, qr[2], qr[3])
program.cx(qr[0], qr[2])
program.cu1(np.pi/4, qr[2], qr[3])
program.cx(qr[1], qr[2])
program.cu1(-np.pi/4, qr[2], qr[3])
program.cx(qr[0], qr[2])
program.cu1(np.pi/4, qr[2], qr[3])

# Reverse the amplification.
program.x(qr)
program.h(qr)

# Measure the result.
program.barrier(qr)
program.measure(qr, cr)

print(run(program, type))