from modules import *
from scipy.optimize import minimize

def calc_and_print(n):
    L = 2 ** n
    list_1 = []
    counter = 0
    for i in range(L):
        if i == np.floor(L/2):
            list_1.append(0.0)
        else:
            list_1.append(counter - L/2 + 1)
            counter += 1

    guess = [-0.5]*n
    counter = 0

    print(f"For $l = {list_1[-1]}$, $n = {n}$:")

    def diag_cost(paras):
        hamiltonian = Hamiltonian(n)
        for i in range(len(paras)):
            Istring = list('I'*n)
            Istring[i] = 'Z'
            Istring = ''.join(Istring)
            hamiltonian.add_term(Istring, paras[i])
        H = hamiltonian.to_matrix()
        cost = 0
        for i in range(L):
            cost += abs(H[i,i] - list_1[i])
        return cost
    
    result = minimize(diag_cost, guess, method='BFGS')

    print(r"\begin{equation}")
    coeffs = result.x
    rounded_coeff = []
    for i in range(len(coeffs)):
        rounded_coeff.append(-1*round(coeffs[i] * 2) / 2)

    print(r"-\frac{1}{2}\left(", end = " ")
    for i in range(len(coeffs)): 
        if abs(2*rounded_coeff[i] != 1):
            print(f" + {int(2*rounded_coeff[i])}Z_{i}", end = " ")
        else:
            print(f"Z_{i}", end = " ")
    print(r"\right)")
    print(r"\end{equation}")

def set_find_error(n):
    L = 2 ** n
    list_1 = []
    counter = 0
    for i in range(L):
        if i == np.floor(L/2):
            list_1.append(0.0)
        else:
            list_1.append(counter - L/2 + 1)
            counter += 1

    guess = [-0.5]*n
    counter = 0

    def diag_cost(paras):
        hamiltonian = Hamiltonian(n)
        for i in range(len(paras)):
            Istring = list('I'*n)
            Istring[i] = 'Z'
            Istring = ''.join(Istring)
            hamiltonian.add_term(Istring, paras[i])
        H = hamiltonian.to_matrix()
        cost = 0
        for i in range(L):
            cost += abs(H[i,i] - list_1[i])
        return cost

    coeffs = []
    for q in range(n-1):
        coeffs.append(2**(q))
    coeffs.append(2**(n-1) - 1)
    coeffs = np.array(coeffs)
    coeffs = -0.5*coeffs

    print('-'*10)
    print("n:",n)
    cost = diag_cost(coeffs)
    print("error:",cost)

def find_links_before(lattice, n, direction):
    links_before = 0
    for j in range(n):
        links_before += len(lattice.directions[j])
    shift = 0

    if len(lattice.directions[n]) == 2 and direction == 2:
        return links_before + 1
    else:
        return links_before

