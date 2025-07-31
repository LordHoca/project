menu = {
    'BAKSO' : 12000,
    'MIE AYAM' : 15000,
    'JUS' : 10000
}
diskon = 0.10
def total (pilih,jumlah) :
    return menu[pilih] * jumlah
def belanja() :
    print('--- Selamat Datang di warung Suka Makmur ---')
    
   
    daftar = []
    while True :
        transaksi = input('Apakah Anda ingin belanja (YA/TIDAK)? : ').upper()
        if transaksi == 'YA' :
            print('Silahkan pilih menu dibawah ini !')
            break
        elif transaksi == 'TIDAK' :
            print('Terima Kasih sudah mengunjungi kami !')
            break
        else :
            print('kode tidak valid masukan kembali !')
            continue
    harga = 0
    while True :
          print('Daftar Menu : ')
          print("BAKSO    : Rp 12.000")
          print("MIE AYAM : Rp 15.000")
          print("JUS      : RP 10.000")
          print("Ketik 'SELESAI' untuk menyelesaikan pesanan Anda !")
          pilih = input('\nMasukan menu pilihan Anda (BAKSO/MIE AYAM/JUS) : ').upper()  
          if pilih == 'SELESAI' : 
              break
          elif pilih not in menu :
              print('masukan kode dgn benar')
              continue
          jumlah = int(input('Jumlah Porsi : '))
          harga += total(pilih,jumlah)
          if harga >= 30000 :
              diskon = 0.10 * harga
    total_harga = harga - diskon    
    print('   \n --- Selamat Datang di warung Suka Makmur ---')         
    print('\n          --- Rincian pembelian ---\n')
    print(f'Harga sebelum diskon       : {harga}')  
    print(f'Diskon yang didapatkan 10% : Rp {diskon}')
    print(f'Total Harga                : Rp {total_harga}\n') 
    bayar = int(input("Masukan Uang Bayar Anda    : Rp ")) 
    kembalian = bayar - total_harga
    print(f'Kembalian Anda             : Rp {kembalian}')
    print('\n--- Terima Kasih Telah Berbelanja di Warung Kami ! ---\n')
belanja()
        