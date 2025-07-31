sepatu = 120000
tas    = 80000
seragam= 79000
 
print('''--- TOKO PERLENGKAPAN SEKOLAH ---
       --- MAJU JAYA ---\n''')
print('Pilih barang yang ingin anda beli :\n ')
print("Sepatu  - 'S'  : Rp 120.000")
print("Tas     - 'T'  : Rp 80.000")
print("Seragam - 'SE' : Rp 79.000\n")

barang = input('Masukan barang yang ingin Anda beli : ').upper()
jumlah = int(input('Masukan jumlah yang ingin Anda beli : '))
print('\n-------    Rincian Pembelian    --------')
if barang == 'S' :
    print('Barang yang dipilih        : Sepatu')
    print(f'Jumlah yang dibeli         : {jumlah}')
    harga = sepatu * jumlah
elif barang == 'T' :
    print('Barang yang dipilih        : Tas')
    print(f'Jumlah yang dibeli         : {jumlah}')
    harga = tas * jumlah
else :
    print('Barang yang dipilih        : Seragam')
    print(f'Jumlah yang dibeli         : {jumlah}')
    harga = seragam * jumlah
diskon = 0.10
if harga >= 200000 :
    total_diskon = harga * diskon
print(f'Diskon yang didapatkan 10% : {total_diskon}')    
harga_awal = (print(f'Harga sebelum diskon       : {harga}'))    
total_harga =(print(f'Harga setelah diskon       : {harga - total_diskon}\n'))    
print('------------ Terima Kasih ------------')
                
    