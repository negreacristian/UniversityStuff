import numpy as np

def doolittle_lu_decomposition(A):
    n = len(A)
    L = np.zeros((n, n))
    U = np.zeros((n, n))

    for i in range(n):
        # Upper Triangular
        for k in range(i, n):
            # Summation of L(i, j) * U(j, k)
            sum = 0
            for j in range(i):
                sum += (L[i][j] * U[j][k])

            # Evaluating U(i, k)
            U[i][k] = A[i][k] - sum

        # Lower Triangular
        for k in range(i, n):
            if (i == k):
                L[i][i] = 1  # Diagonal as 1
            else:
                # Summation of L(k, j) * U(j, i)
                sum = 0
                for j in range(i):
                    sum += (L[k][j] * U[j][i])

                # Evaluating L(k, i)
                L[k][i] = (A[k][i] - sum) / U[i][i]

    return L, U

def solve_lu_decomposition(A, b):
    L, U = doolittle_lu_decomposition(A)

    # Ly = b
    n = len(A)
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i]
        for j in range(i):
            y[i] -= L[i][j] * y[j]

    # Ux = y
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = y[i]
        for j in range(i + 1, n):
            x[i] -= U[i][j] * x[j]
        x[i] /= U[i][i]

    return x

# Definirea matricei coeficienților A și a vectorului termenilor liberi b
A = np.array([[4, -1, 1], [8, 3, -1], [3, 1, 1]])
b = np.array([6, 10, 9])

# Rezolvarea sistemului
solution = solve_lu_decomposition(A, b)
print("Soluția sistemului este:", solution)
