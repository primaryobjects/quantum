Quantum Computing Tutorial
==========================

A set of simple programs for learning how to program a quantum computer.

Read the tutorial [An Introduction to Quantum Computing]([http://www.primaryobjects.com/2019/01/07/an-introduction-to-quantum-computing/)

## What is it?

Quantum computing is a technology based upon quantum physics and its inherent properties of superposition and entanglement. It brings a new paradigm to programming, where algorithms can be created that can process exponentially more data than classical computers that rely on transistor-based technology.

This project contains a set of basic example programs to learn about programming a quantum computer.

Several tutorial examples are included in this repository including the projects listed below.

## Quick Start

To get started with quantum programming and the examples in this project, follow the steps below.

1. Install [Python3](https://www.python.org/downloads/).

2. Install [pip](https://pip.pypa.io/en/stable/installing/) if needed. To install pip, download [get-pip.py](https://bootstrap.pypa.io/get-pip.py) and execute it with the following command.

    ```bash
    python get-pip.py
    ```

3. Install the required libraries for QisKit and the examples.

    ```bash
    pip install qiskit
    pip install ConfigParser
    ```

### Hello World

[hello.py](hello.py)

A simple "Hello World" program in quantum computing. The program uses 1 qubit and simply measures it, finally printing out the text, "Hello World" and the measurement appended.

### Fly Unicorn

[unicorn.py](unicorn.py)

A game written on a quantum computer!

Your magestic unicorn is ready for flight!
After a long night of preparation and celebration, it's time to visit the castle in the clouds.
Use your keyboard to fly up or down on a quantum computer, as you ascend your way into the castle.

```text
===============
  Fly Unicorn
===============

Your majestic unicorn is ready for flight!
After a long night of preparation and celebration, it’s time to visit the castle in the clouds.
Use your keyboard to fly up or down on a quantum computer, as you ascend your way into the castle.


=====================
-[ Altitude 0 feet ]-
Your unicorn is waiting for you on the ground.
[up,down,quit]: u
You soar into the sky.
Running on the simulator.
{'0': 945, '1': 55}

=====================
-[ Altitude 55 feet ]-
Your unicorn is floating gently above the ground.
[up,down,quit]: u
You soar into the sky.
Running on the simulator.
{'0': 886, '1': 114}

=====================
-[ Altitude 114 feet ]-
Your unicorn is hovering just above the evergreen sea of trees.
[up,down,quit]:
```

### Superposition

[superposition.py](superposition.py)

An example of using superposition in quantum programming. This program contains three examples to demonstrate the properties of quantum superposition and entanglement.

The first example measures 2 qubits in their initial states (all zeros) and prints the results.

The second example creates a [Bell state](https://en.wikipedia.org/wiki/Bell_state) (|00> + |11>), (|00> - |11>), (|01> + |10>), (|01> - |10>). This is done by entangling 2 qubits, placing the first qubit into superposition (existing as 0 and 1 simulataneously with 50% chance of measuring either value), and finally measuring the results. The output should be half 00 and half 11.

The third example demonstrates [superdense coding](https://en.wikipedia.org/wiki/Superdense_coding). This involves sending two classical bits of information (for example: 01) by only manipulating a single qubit. Suppose Alice wants to send Bob the message 01. This can be done by entangling the two qubits to create a Bell state of `00`. One qubit is given to Alice and the other is given to Bob. Alice can now manipulate her qubit to alter the resulting Bell state to indicate the value `01`. She can do this by inverting the value of her qubit (which is in superposition). She then sends Bob her qubit. Bob now reverses the entanglement and reverses the superposition of Alice's qubit. Bob can now measure the two qubits and obtain the value of `01`. In this case, Bob's qubit miraculously turns from a `0` into a `1`.

### Cloning a Qubit

[clone.py](clone.py)

An example of cloning a qubit that is currently in superposition to another qubit.

This process involves setting the first qubit to a value of 1 (the value we want to clone to the second qubit). We then place the first qubit into superposition. To clone, we first reverse the superposition on the first qubit. Next, we perform a controlled-not operation between the two qubits, establishing an entanglement. We then put both qubits into superposition, effectively cloning their values.

### The Deutsch Jozsa Algorithm

[deutsch_jozsa.py](deutsch_jozsa.py)

An example of the Deutsch Jozsa Algorithm. This algorithm demonstrates how a quantum computer substantially differs from a classical computer by solving a problem in 1 cycle, that would take a classical computer much longer.

License
----

MIT

Author
----
Kory Becker
http://www.primaryobjects.com/kory-becker
