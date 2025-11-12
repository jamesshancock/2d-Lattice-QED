# == Some notes ==
# Want to reproduce the results from https://arxiv.org/pdf/2411.05628 on using QC for (2+1)-QED

# Other modules
from modules import *

# My modules
from classes import *
# from QED_hamiltonian import *
from gauge_helpers import *
from circuit_helpers import *

def mass_term_n(hamiltonian, lattice, n, m): 
    gauge_string = 'I'*lattice.n_gauge_qubits
    fermion_before = 'I'*n
    fermion_after = 'I'*(lattice.n_fermion_qubits - n - 1)

    coordinates = lattice.get_coordinates(n)
    term = gauge_string + fermion_before + 'Z' + fermion_after
    coeff = m*(-1)**(coordinates[0] + coordinates[1]) / 2

    hamiltonian.add_term(term, coeff)
    hamiltonian.add_term('I'*lattice.n_qubits, coeff)

    return hamiltonian

def electric_field_term_n_direction(hamiltonian, lattice, n, direction, g):
    link_index = find_links_before(lattice, n, direction)
    coeff = g**2 / 2

    fermion_string = 'I' * lattice.n_fermion_qubits

    gauge_before = 'I' * (link_index * lattice.qubits_per_gauge)
    gauge_after = 'I' * (lattice.n_gauge_qubits - (link_index + 1) * lattice.qubits_per_gauge)

    if lattice.qubits_per_gauge == 2:
        hamiltonian.add_term(gauge_before + 'IZ' + gauge_after + fermion_string, -0.5 * coeff)
        hamiltonian.add_term(gauge_before + 'ZI' + gauge_after + fermion_string, -0.5 * coeff)

    elif lattice.qubits_per_gauge == 3:
        hamiltonian.add_term(gauge_before + 'IIZ' + gauge_after + fermion_string, -1.5 * coeff)
        hamiltonian.add_term(gauge_before + 'IZI' + gauge_after + fermion_string, -1.0 * coeff)
        hamiltonian.add_term(gauge_before + 'ZII' + gauge_after + fermion_string, -0.5 * coeff)
    
    h_sq = copy.copy(hamiltonian)
    hamiltonian.hamiltinian = h_sq.multiply_hamiltonians(hamiltonian)
    return hamiltonian

def electric_field_term_n(hamiltonian, lattice, n, g):
    for direction in lattice.directions[n]:
        E_temp = Hamiltonian(lattice.n_qubits)
        E_temp = electric_field_term_n(E_temp, lattice, n, direction, g)
        hamiltonian.add_hamiltonians(E_temp)
    return hamiltonian

def magnetic_term_n(hamiltonian, lattice, g, a, index):
    return hamiltonian

def kinetic_term_n(hamiltonian, lattice, n, a, index):
    return hamiltonian
 

L_x = 2
L_y = 2
gauge_truncation = 1
m = 1.0
g = 1.0

# Gauge qubits are ordered according to the lists in directions, i.e, site order, then 1 and/or 2 (dependant on site)

lattice = Lattice(L_x,L_y,gauge_truncation)
hamil = Hamiltonian(lattice.n_qubits)

# Mass term - WORKS
for n in range(lattice.n_fermion_qubits):
    hamil = mass_term_n(hamil, lattice, n, m)

# Electric field term - WORKS
for n in range(lattice.n_links):
    hamil = electric_field_term_n(hamil, lattice, n, g)

# Next I think I will work on the magnetic term
# This will involve taking the conjugate, as well as the product around a plaquette
