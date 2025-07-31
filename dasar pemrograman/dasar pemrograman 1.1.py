nama = input("Masukan Nama  : ")
Nis = input("Masukan Nis   : ")
Jurusan = input("Pilih Jurusan : [SI/SIA] : ")
SI = 2400000
SIA = 2000000
if Jurusan == "SI" or Jurusan == "si" or Jurusan == "Si":
    Harga = SI
elif Jurusan == "SIA" or Jurusan == "sia" or Jurusan == "Sia":
    Harga = SIA
else:
    Harga = 0
print(f"Harga jurusan yang anda pilih senilai : {Harga}")