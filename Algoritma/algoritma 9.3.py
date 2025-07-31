
n = 4
A = [[0 for j in range(n)] for i in range(n)]
for i in range(n):
    A[i][i] = 1  
for row in A:
    print(row)