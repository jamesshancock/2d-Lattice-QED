from modules import *
from classes import *

def mass_term_n(hamiltonian, lattice, n, m, index): 
    gauge_string = 'I'*lattice.n_gauge_qubits
    fermion_before = 'I'*n
    fermion_after = 'I'*(lattice.n_fermion_qubits - n - 1)

    coordinates = lattice.get_coordinates(n)
    term = gauge_string + fermion_before + 'Z' + fermion_after
    coeff = m*(-1)**(coordinates[0] + coordinates[1]) / 2

    hamiltonian.add_term(term, coeff)
    hamiltonian.add_term('I'*lattice.n_qubits, coeff)

    return hamiltonian

def electric_field_term_n(hamiltonian, lattice, n, direction, g, index):

    link_index = 2 * n + (direction - 1)
    coeff = g**2 / 2

    fermion_string = 'I' * lattice.n_fermion_qubits

    gauge_before = 'I' * (link_index * lattice.qubits_per_gauge)
    gauge_after = 'I' * (lattice.n_gauge_qubits - (link_index + 1) * lattice.qubits_per_gauge)

    if lattice.qubits_per_gauge == 2:
        hamiltonian.add_term(fermion_string + gauge_before + 'IZ' + gauge_after, -0.5 * coeff)
        hamiltonian.add_term(fermion_string + gauge_before + 'ZI' + gauge_after, -0.5 * coeff)

    elif lattice.qubits_per_gauge == 3:
        hamiltonian.add_term(fermion_string + gauge_before + 'IIZ' + gauge_after, -1.5 * coeff)
        hamiltonian.add_term(fermion_string + gauge_before + 'IZI' + gauge_after, -1.0 * coeff)
        hamiltonian.add_term(fermion_string + gauge_before + 'ZII' + gauge_after, -0.5 * coeff)

    return hamiltonian

def test_electric_field_term_n(qubits_per_gauge, g):
    coeff = g**2 / 2
    hamiltonian = Hamiltonian(qubits_per_gauge)
    
    if qubits_per_gauge == 2:
        hamiltonian.add_term('IZ', -0.5 * coeff)
        hamiltonian.add_term('ZI', -0.5 * coeff)
    elif qubits_per_gauge == 3:
        hamiltonian.add_term('IIZ', -1.5 * coeff)
        hamiltonian.add_term('IZI', -1.0 * coeff)
        hamiltonian.add_term('ZII', -0.5 * coeff)
    
    return hamiltonian

def magnetic_term_n(hamiltonian, lattice, g, a, index):
    return hamiltonian

def kinetic_term_n(hamiltonian, lattice, n, a, index):
    return hamiltonian

