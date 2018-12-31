#
# Fly Unicorn
# A simple quantum game where the player has to fly a unicorn to the castle.
#

import math
import qiskit
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from qiskit import IBMQ
from configparser import RawConfigParser

# Selects the environment to run the game on: simulator or real
device = 'sim';

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

# Get the status for the current state of the unicorn.
def status(altitude):
  if altitude == 0:
    return 'Your unicorn is waiting for you on the ground'
  elif altitude <= 100:
    return 'Your unicorn is floating gently above the ground'
  elif altitude <= 200:
    return 'Your unicorn is hovering just above the evergreen sea of trees'
  elif altitude <= 300:
    return 'Your unicorn is approaching the first misty cloud layer'
  elif altitude <= 400:
    return 'Your unicorn has soared through the misty pink clouds'
  elif altitude <= 500:
    return 'Your unicorn is well above the misty clouds'
  elif altitude <= 600:
    return 'You can barely see the evergreen sea of trees from this high up'
  elif altitude <= 700:
    return 'Your unicorn is soaring through the sky'
  elif altitude <= 800:
    return 'You can see the first glimpse of the golden castle gates just above you'
  elif altitude <= 900:
    return 'Your unicorn is nearly at the mystical castle gates'
  elif altitude < 1000:
    return 'Your unicorn swiftly glides through the mystical castle gate. You\'re almost there'
  else:
    return 'A roar emits from the crowd of excited sky elves, waiting to greet you'

def action(command):
  command = command.lower()[0]

  switcher = {
    'u': 150,
    'd': -150,
    'q': 0
  }

  return switcher.get(command, -1)

run.isInit = False # Indicate that we need to initialize the IBM Q API in the run() method.
isGameOver = False # Indicates when the game is complete.
altitude = 0 # Current altitude of player. Once goal is reached, the game ends.
goal = 1000 # Max altitude for the player to reach to end the game.
shots = goal + (125 if device == 'real' else 0) # Number of measurements on the quantum machine; when shots == goal, the player reached the goal; we include a buffer on physical quantum computers to account for natural error.

print('===============')
print('  Fly Unicorn')
print('===============')
print('')
print('Your majestic unicorn is ready for flight!')
print('After a long night of preparation and celebration, it\'s time to visit the castle in the clouds.')
print('Use your keyboard to fly up or down on a quantum computer, as you ascend your way into the castle.')
print('')

# Begin main game loop.
while not isGameOver:
  # Setup a qubit to represent the unicorn.
  unicorn = QuantumRegister(1)
  unicornClassic = ClassicalRegister(1)
  program = QuantumCircuit(unicorn, unicornClassic);

  # Get input from the user.
  command = ''
  while not command.lower() in ['u', 'd', 'q', 'up', 'down', 'quit']:
    # Read input.
    command = input("\n=====================\n-[ Altitude " + str(altitude) + " feet ]-\n" + status(altitude) + ".\n[up,down,quit]: ").lower()

  # Process input.
  modifier = action(command)
  if modifier == 0:
    isGameOver = True
  elif modifier == -1:
    print("What?")
  else:
    if modifier > 0:
      print("You soar into the sky.")
    elif modifier < 0:
      if altitude > 0:
        print("You dive down lower.")
      else:
        print("Your unicorn can't fly into the ground!")

    # Calculate the amount of NOT to apply to the qubit, based on the percent of the new altitude from the goal.
    frac = (altitude + modifier) / goal
    if frac >= 1:
      # The unicorn is at or beyond the goal, so just invert the 0-qubit to a 1-qubit for 100% of goal.
      # Note: On a real quantum machine the error rate is likely to cause NOT(0) to not go all the way to 1, staying around 1=862 and 0=138, etc.
      program.x(unicorn)
    elif frac > 0:
      # Apply a percentage of the NOT operator to the unicorn (qubit), cooresponding to how high the unicorn is.
      program.u3(frac * math.pi, 0.0, 0.0, unicorn)

    # Collapse the qubit superposition by measuring it, forcing it to a value of 0 or 1.
    program.measure(unicorn, unicornClassic);

    # Execute on quantum machine.
    counts = run(program, device, shots)
    print(counts)

    # Set the altitude based upon the number of 1 counts in the quantum results.
    altitude = counts['1'] if '1' in counts else 0

    # Did the player reach the castle?
    if altitude >= goal:
      print('Congratulations! Your unicorn soars into the castle gates!')
      isGameOver = True
