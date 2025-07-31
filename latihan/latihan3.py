#inputan pembeli atau penentuan harga tiket
print('''
      
======== Data Pembelian Tiket ========''')
Nama_Pembeli = input("Nama Pembeli : ")
Nomor_Hp = input("Nomor Hp     : ")
tujuan = input("Pilih Tujuan : [SBY, BL, LMP] : ")
jumlah_tiket = int(input("Jumlah Tiket yang Dibeli Anda : "))
if tujuan == "SBY" or tujuan == "sby" or tujuan == "Sby" :
      nama_jurusan = "surabaya"
      harga = 300000
elif tujuan == "BL" or tujuan == "bl" or tujuan == "Bl":
      nama_jurusan = "Bali"
      harga = 350000
else:
      tujuan == "LMP" or tujuan == "lmp" or tujuan == "Lmp"
      nama_jurusan = "Lampung"
      harga = 500000
#jumlah pembelian tiket
if jumlah_tiket >= 3 :
      diskon = (harga * jumlah_tiket)*0.1
else:
      diskon = 0
      
total_harga_tiket = (jumlah_tiket * harga) - diskon  
print(f"Harga Tiket                : {total_harga_tiket}")  
print(f"diskon yang didapat        : {diskon}") 
uang_bayar = int(input("Uang Bayar                 : "))
kembalian = uang_bayar - total_harga_tiket
print(F"Kembalian                  : {kembalian}")
print(
      
'''== Terima Kasih Atas Pembelian Anda ==''')