def luas_persegi_pajang (panjang, lebar) :
    luas = panjang * lebar
    return luas
panjang = 7
lebar = 4
luas = luas_persegi_pajang(panjang, lebar)
print(f'\nLuas dari persegi panjang tersebut adalah : {luas}')
x = 19
y = 5
angka = x==y
bilangan = x > y
print(angka)
print(bilangan)        
nama = "Fauzan"
nama2 = "Fadhilah"
print(nama +(" ") + nama2)
print(len(nama + nama))
print('what\'s')
x = 12.345678910
print('nilai x = %3.2f'%x)
print('nilai x = %3.3f'%x)
print('nilai x = %3.4f'%x)
print('nilai x = %3.5f'%x)
print('|{:<8} |{:^8}| {:>8}|'.format('sepeda', 'motor', 'mobil'))
print('fauzan fadhilah'.startswith('f'))
print('fauzan fadhilah'.endswith('h'))
list = ['saya' ,[1,2,3], 'fauzan']
print(list[0][2])
my_list = ['f','a','u','z','a','n']
print(my_list[3:])
mapel = ['aqidah', 'hadits']
for i in range(len(mapel)) :
    print(f'saya suka mapel' , mapel[i])
my_list[1] = 'd'
print(my_list)    
my_list.append('fauzan')
print(my_list)
my_list.extend(['fadhilah'])
print(my_list)