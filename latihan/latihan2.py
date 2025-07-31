# Program Toko Buku Cerdas Selalu
# Quis_NIM

# Data buku dan harga
buku = {'DP': 150000, 'PP': 170000, 'WP': 200000}
judul_buku = {'DP': 'DASAR PEMROGRAMAN', 'PP': 'PHYTON PROGRAMMING', 'WP': 'WEB PROGRAMMING'}

print("Toko Buku Cerdas Selalu\n")
print("DAFTAR BUKU")
print("=" * 43)
print("KODE | JUDUL BUKU           | HARGA")
print("=" * 43)
print("DP   | DASAR PEMROGRAMAN    | Rp. 150.000")
print("PP   | PHYTON PROGRAMMING   | Rp. 170.000")
print("WP   | WEB PROGRAMMING      | Rp. 200.000")
print("=" * 43)

# Input nama pembeli
nama_pembeli = input("Masukan Nama Pembeli: ")

# Variabel untuk total pembelian
total_sub = 0
no = 1  # Nomor urut pembelian
total_harga1, total_harga2, total_harga3 = 0, 0, 0  # Menyimpan total harga per item

# Variabel untuk jumlah beli per buku
jumlah_beli1, jumlah_beli2, jumlah_beli3 = 0, 0, 0

while True:
    kode_buku = input("Masukan Kode Buku [DP/PP/WP]: ").upper()
    
    if kode_buku == 'DP':
        jumlah_beli = int(input("Masukan jumlah beli: "))
        total_harga1 = buku['DP'] * jumlah_beli
        jumlah_beli1 = jumlah_beli
        total_sub += total_harga1
    elif kode_buku == 'PP':
        jumlah_beli = int(input("Masukan jumlah beli: "))
        total_harga2 = buku['PP'] * jumlah_beli
        jumlah_beli2 = jumlah_beli
        total_sub += total_harga2
    elif kode_buku == 'WP':
        jumlah_beli = int(input("Masukan jumlah beli: "))
        total_harga3 = buku['WP'] * jumlah_beli
        jumlah_beli3 = jumlah_beli
        total_sub += total_harga3
    else:
        print("Kode buku tidak valid. Pilih DP, PP, atau WP.")
        continue
    
    lanjut = input("Lanjut beli (Y/T)? ").upper()
    if lanjut != 'Y':
        break

# Menghitung diskon dan pajak
diskon = 0
if total_sub > 500000:
    diskon = total_sub * 0.10
pajak = total_sub * 0.11
total_bayar = total_sub - diskon + pajak

# Menampilkan hasil pembelian
print("\nNama Pembeli:", nama_pembeli)
print("Toko Buku Cerdas Selalu")
print("=" * 65)
print("No | Judul Buku         | Jumlah Beli | Harga      | Total")
print("=" * 65)

if jumlah_beli1 > 0:
    print(f"{no:<3} | DASAR PEMROGRAMAN | {jumlah_beli1:<7}     | Rp. 150000 | Rp. {total_harga1:<7}")
    no += 1
if jumlah_beli2 > 0:
    print(f"{no:<3} | PHYTON PROGRAMMING| {jumlah_beli2:<7}     | Rp. 170000 | Rp. {total_harga2:<7}")
    no += 1
if jumlah_beli3 > 0:
    print(f"{no:<3} | WEB PROGRAMMING   | {jumlah_beli3:<7}     | Rp. 200000 | Rp. {total_harga3:<7}")
    no += 1

print("=" * 65)
print(f"Sub total          : Rp. {total_sub:,.0f}")
print(f"Diskon             : Rp. {diskon:,.0f}")
print(f"Pajak              : Rp. {pajak:,.0f}")
print(f"Total Bayar        : Rp. {total_bayar:,.0f}")

# Input uang bayar dan hitung kembalian
uang_bayar = int(input("Masukan uang bayar : Rp. "))
uang_kembali = uang_bayar - total_bayar
print(f"Uang Kembali       : Rp. {uang_kembali:,.0f}\n")
print("========== TERIMA KASIH TELAH BERBELANJA DI TOKO KAMI ! =========\n")
