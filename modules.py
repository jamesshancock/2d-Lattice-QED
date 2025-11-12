import numpy as np
import qiskit
import qiskit_aer
import cmath
import time
import copy

NOISELESS_SIMULATOR = qiskit_aer.AerSimulator()
PAULI_PHASES = {
    'I': {
        'I': ('I', 1),
        'X': ('X', 1),
        'Y': ('Y', 1),
        'Z': ('Z', 1),
    },
    'X': {
        'I': ('X', 1),
        'X': ('I', 1),
        'Y': ('Z', 1j),
        'Z': ('Y', -1j),
    },
    'Y': {
        'I': ('Y', 1),
        'X': ('Z', -1j),
        'Y': ('I', 1),
        'Z': ('X', 1j),
    },
    'Z': {
        'I': ('Z', 1),
        'X': ('Y', 1j),
        'Y': ('X', -1j),
        'Z': ('I', 1),
    },
}