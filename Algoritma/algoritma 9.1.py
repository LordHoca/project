nilai = 4
matriks = [[0 for i in range (nilai)] for j in range(nilai)]
for i in range(nilai) :
    for j in range(nilai) :
        if i==j :
            matriks[i][j] = i + 1
        elif i < j : 
            matriks[i][j] = j + 1

for i in range(nilai) :
    print (matriks[i])                