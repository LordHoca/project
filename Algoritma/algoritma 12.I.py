def InsertionSort(val):
    for index in range(1,len(val)):
       a = val[index]
       b = index
       while b>0 and val[b-1]>a:
         val[b]=val[b-1]
         b = b-1
       val[b]=a
Angka = [25, 20, 15, 3, 7, 2, 1]
InsertionSort(Angka)
print(Angka)
