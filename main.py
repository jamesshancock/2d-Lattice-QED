# == Some notes ==
# Want to reproduce the results from https://arxiv.org/pdf/2411.05628 on using QC for (2+1)-QED

# External modules
from modules import *

# My modules
from classes import *
from circuit_helpers import *
from QED_hamiltonian import *

parameters = {
    'L_x': 2,
    'L_y': 2,
    'gauge_truncation': 1,
    'n_fermion_layers' : 1,
    'shots': 10000,
    'm': 1.0,
    'g': 1.0,
    'a': 1.0
}

print("RUNNING")


# Now need to build a nice VQE
circuit, observables, thetas, total_thetas = initiate_circuit_observables(parameters['L_x'],parameters['L_y'],parameters['n_fermion_layers'],parameters['gauge_truncation'])
thetas_values = [1.0]*total_thetas

hamiltonian = generate_qed_hamiltonian(parameters)

def thetas_only_wrapper(thetas_values):
    return qed_vqe(thetas_values, thetas, hamiltonian, circuit, observables, parameters['shots'])

for _ in range(10):
    value = thetas_only_wrapper(thetas_values)
    print(value)
    
