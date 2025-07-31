import pandas as pd
list_nim =  []
list_nama = []
list_uts =  []
list_uas =  []
list_total= []

ulang = 1
for i in range(ulang) :
    print("data ke - " + str (i + 1))
    list_nim.append(input("NIM   : "))
    list_nama.append(input('NAMA : '))
    list_uts.append(int(input('Nilai UTS : ')))
    list_uas.append(int(input('Nilai UAS : ')))

for i in range(ulang) :
    list_total.append(list_uts[i] + list_uas[i]/2)
tamu = {
    "NIM" : list_nim,
    "NAMA": list_nama,
    "UTS" : list_uts,
    "UAS" : list_uas,
    "Rata - rata " : list_total
}        
data_tamu = pd.DataFrame(tamu)
print("=" * 30)
print(data_tamu)
print("=" * 30)
