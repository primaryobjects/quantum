#
# A quantum random number generator.
# Generates a random number of 2^x-bits in length by using x qubits.
# 2 qubits = 4-bit random value
# 3 qubits = 8-bit random value (1 byte)
# 4 qubits = 16-bit random value (1 short, int16)
# 5 qubits = 32-bit random value (int32)
#
# We can determine how many bits are required for a maximum integer value via: log2(n) + 1
# Random number generation occurs with just a single CPU cycle on the quantum computer (no loops required).
#

import qiskit
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from qiskit import IBMQ
from configparser import RawConfigParser
import math

type = 'sim' # Run program on the simulator or real quantum machine.

def run(program, type, shots = 1, silent = False):
  if type == 'real':
    # Setup the API key for the real quantum computer.
    parser = RawConfigParser()
    parser.read('config.ini')
    IBMQ.enable_account(parser.get('IBM', 'key'))
    run.isInit = True

    # Set the backend server.
    backend = qiskit.providers.ibmq.least_busy(qiskit.IBMQ.backends(simulator=False))

    # Execute the program on the quantum machine.
    if not silent:
      print("Running on", backend.name())
    job = qiskit.execute(program, backend)
    return job.result().get_counts()
  else:
    # Execute the program in the simulator.
    if not silent:
      print("Running on the simulator.")
    job = qiskit.execute(program, qiskit.Aer.get_backend('qasm_simulator'), shots=shots)
    return job.result().get_counts()

def bitCount(value):
  # Returns the number of bits needed to represent the integer value.
  return math.floor(math.log(value, 2)) + 1

def bitsToInt(bits):
  # Convert a list of bits into an integer.
  out = 0
  for bit in bits:
    out = (out << 1) | bit

  return out

def random(max):
  # Number of shots when we run the quantum program.
  shots = 1000

  # Determine how many bits are required for the maximum value.
  bits = bitCount(max)

  # Determine how many qubits are required to represent the number of bits, using the formula: 2^x = bits (where x is the number of qubits). For example, a value of 10 requires 4 bits which can be represented with 2 qubits (since 2^2 = 4). A value of 100 requires 7 bits which can be represented with 3 qubits (since 2^3 = 8).
  x = math.ceil(math.log(bits, 2))

  # Create x qubits for the input array.
  qr = QuantumRegister(x)
  # Create x registers for the output.
  cr = ClassicalRegister(x)
  program = QuantumCircuit(qr, cr)

  # Place all qubits into superposition.
  program.h(qr)

  # Measure all qubits.
  program.measure(qr, cr)

  # Run the program for 1000 shots.
  results = run(program, type, shots, True)

  # Since the qubits are in superposition, they will have a 50% probability of returning 0 or 1 within each state.
  # We will get back 2^x results (with counts for the number of times each combination of 0s and 1s was measured).
  # Go through each result and determine a final 0 or 1 value for each bit by checking if the count is greater than the average probability.
  # The average probability = shots / outcomes (outcomes = 2^x).
  averageProbability = shots / math.pow(2, x)

  # Create an array to hold the random generated bits.
  randomBits = []
  for key,value in results.items():
    randomBits.append(1 if value > averageProbability else 0)

  return randomBits

# Generate a random value from 0-100+. Note, this actually produces a max value of the max bits that can be represented for the specified number. For example, 10 uses 4 bits or 2 qubits with a max value of 15.
randomValues = []
for i in range(500):
  randomValues.append(bitsToInt(random(100)))

print(randomValues)