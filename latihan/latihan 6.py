list_nim = []
list_uts = []
list_uas = []
list_total = []
repeat = int(input('Banyak data yang akan dihitung : '))
for i in range(repeat):
    print('Data Ke -' + str (i+1))
    list_nim.append  (input("Masukan NIM Anda : "))
    list_uts.append  (int(input("Masukan Nilai UTS Anda : ")))
    list_uas.append  (int(input("Masukan Nilai UAS Anda : ")))
for i in range(repeat) :
    list_total.append (int((list_uts[i] + list_uas[i])/2))
print("=============================================================")
print("NIM\t\tNILAI UTS\tNILAI UAS\tTOTAL NILAI")
for i in range(repeat):
    print(f'{list_nim[i]}\t {list_uts[i]}\t\t {list_uas[i]}\t\t {list_total[i]}')  
print("=============================================================")  
   