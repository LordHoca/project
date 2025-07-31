def bil_prima (bilangan):
    if bilangan < 2:
        return False
    for i in range(2, int(bilangan ** 0.5) + 1):
        if bilangan % i == 0:
            return False
    return True

angka = int(input("Masukkan sebuah bilangan untuk dicek: "))
if bil_prima(angka):
    print(f"{angka} adalah bilangan prima.")
else:
    print(f"{angka} bukan bilangan prima.")