# modul_nilai.py

def hitung_rata_rata(jumlah_data):
    # Membuat list untuk menyimpan nilai
    nilai_list = []
    
    # Meminta input nilai untuk setiap data
    for i in range(jumlah_data):
        while True:
            try:
                nilai = float(input(f"Masukkan nilai untuk data ke-{i+1}: "))
                nilai_list.append(nilai)
                break
            except ValueError:
                print("Input tidak valid. Harap masukkan angka.")
    
    # Menghitung rata-rata
    rata_rata = sum(nilai_list) / jumlah_data
    return rata_rata