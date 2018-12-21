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

def oracle(program, bit0, bit1, bit2, bit3):
  # Invert the bits associated with a value of 0.
  if bit0 == 0:
    program.x(qr[0])
  if bit1 == 0:
    program.x(qr[1])
  if bit2 == 0:
    program.x(qr[2])
  if bit3 == 0:
    program.x(qr[3])

# Choose a random code for the oracle function.
bit0 = np.random.randint(2)
bit1 = np.random.randint(2)
bit2 = np.random.randint(2)
bit3 = np.random.randint(2)
password = str(bit3) + str(bit2) + str(bit1) + str(bit0)

print("The oracle password is " + password + ".")

# Create 2 qubits for the input array.
qr = QuantumRegister(4)
# Create 2 registers for the output.
cr = ClassicalRegister(4)
program = QuantumCircuit(qr, cr)

# Place the qubits into superposition to represent all possible values.
program.h(qr)

# Run oracle on key. Invert the 0-value bits.
oracle(program, bit0, bit1, bit2, bit3)

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
oracle(program, bit0, bit1, bit2, bit3)

# Amplification.
program.h(qr)
program.x(qr)

# cccZ
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
