# Fungsi untuk menghitung gaji berdasarkan gaji pokok dan jam kerja
def hitung_gaji(gaji_pokok, jam_kerja):
    # Konstanta
    tunjangan_rate = 20  # Tunjangan 20% dari gaji pokok
    lembur_rate = 20000  # Rp 20000 per jam lembur
    jam_normal = 200  # Maksimal jam kerja normal
    pajak_rate = 0.10  # Pajak 10%

    # Menghitung tunjangan
    tunjangan = tunjangan_rate * gaji_pokok

    # Menghitung lembur
    jam_lembur = max(0, jam_kerja - jam_normal)
    lembur = jam_lembur * lembur_rate

    # Menghitung total gaji sebelum pajak
    total_gaji = gaji_pokok + tunjangan + lembur

    # Menghitung pajak
    pajak = total_gaji * pajak_rate

    # Menghitung total gaji setelah pajak
    total_gaji_setelah_pajak = total_gaji - pajak

    return total_gaji_setelah_pajak, tunjangan, lembur, pajak

# Contoh input
gaji_pokok = int(input("Masukkan gaji pokok: "))
jam_kerja = int(input("Masukkan total jam kerja: "))

# Menghitung gaji
total_gaji_setelah_pajak, tunjangan, lembur, pajak = hitung_gaji(gaji_pokok, jam_kerja)

# Menampilkan hasil
print(f"Gaji Pokok: Rp {gaji_pokok}")
print(f"Tunjangan: Rp {tunjangan}")
print(f"Lembur: Rp {lembur}")
print(f"Pajak: Rp {pajak}")
print(f"Total Gaji Setelah Pajak: Rp {total_gaji_setelah_pajak}")