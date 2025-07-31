nama = "Fauzan Fadhilah"
n = int(input('Masukan bilangan : '))
for i in range(0, n) :
    for i in range(0, i + 1) :
        print('^ ', end="")
    print("")   
print(f'Nama : {nama}')                              