from modules import *
from classes import *

def initiate_circuit_observables(L_x,L_y,n_fermion_layers,gauge_truncation):

    measurer = Measurements()
    lattice = Lattice(L_x,L_y,gauge_truncation)
    observables = ObservableCalculator(lattice,measurer)    
    
    builder = CircuitBuilder(lattice.n_fermion_qubits, lattice.n_links*lattice.qubits_per_gauge)
    builder.initialize_fermions()
    n_slice = builder.iSwap_block_calculate()

    fermion_thetas = [np.random.uniform(0,2*np.pi) for x in range(n_slice*n_fermion_layers)]
    gauge_thetas = [0 for x in range(lattice.qubits_per_gauge*lattice.n_links)]
    thetas = fermion_thetas + gauge_thetas

    for j in range(n_fermion_layers):
        builder.iSwap_block(fermion_thetas[n_slice*j:n_slice*j+(n_slice)])
    builder.gauge_block(gauge_thetas, gauge_truncation)

    circuit = builder.build()

    return circuit, observables

def circuit_caller():
    shots = 1024
    L_x = 2
    L_y = 2
    n_fermion_layers = 1
    gauge_truncation = 1

    circuit, observables = initiate_circuit_observables(L_x,L_y,n_fermion_layers,gauge_truncation)

    charge_total = observables.charge_total(circuit)

    print("Total_charge:",charge_total)
