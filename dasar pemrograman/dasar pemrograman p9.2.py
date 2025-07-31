def faktorial(bilangan):
    if bilangan == 0 or bilangan == 1:
        return 1
    return bilangan * faktorial(bilangan - 1)

angka = int(input("Masukkan sebuah bilangan untuk menghitung faktorialnya: "))
if angka < 0:
    print("Faktorial tidak terdefinisi untuk bilangan negatif.")
else:
    print(f"Faktorial dari {angka} adalah {faktorial(angka)}.")