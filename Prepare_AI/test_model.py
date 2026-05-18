import cv2
from ultralytics import YOLO

# ==============================================================================
# 1. KONFIGURASI MODEL & GAMBAR
# ==============================================================================
path_model = r'runs\detect\model_bumbu_masak-3\weights\best.pt'
gambar_tes = r'Final_Dataset\images' 

model = YOLO(path_model)

# ==============================================================================
# 2. KAMUS INFORMASI TAMBAHAN
# ==============================================================================
# Tambahkan atau ubah informasi di bawah ini sesuai keinginanmu
INFO_BUMBU = {
    "jahe": "Fungsi: Penghilang bau amis & wedang",
    "kencur": "Fungsi: Obat batuk & bumbu seblak",
    "kunyit": "Fungsi: Pewarna alami kuning & jamu",
    "lada": "Fungsi: Memberikan rasa pedas hangat",
    "lengkuas": "Fungsi: Bumbu rendang & kuah kaldu",
    "bunga lawang": "Fungsi: Rempah aromatik masakan Asia",
    "kemiri": "Fungsi: Pengental kuah & penyedap",
    # Kamu bisa menambahkan bumbu lainnya di sini...
}

print("🤖 AI sedang mengamati gambar dan mencari informasi...")

# ==============================================================================
# 3. PREDIKSI (Tanpa memunculkan otomatis)
# ==============================================================================
hasil = model.predict(source=gambar_tes, conf=0.7)

# Ambil hasil pertama (karena kita hanya tes 1 gambar)
result = hasil[0]
gambar_asli = result.orig_img  # Mengambil gambar asli dalam bentuk matriks

# ==============================================================================
# 4. MENGGAMBAR KOTAK DAN INFORMASI
# ==============================================================================
for box in result.boxes:
    # Ambil koordinat kotak
    x1, y1, x2, y2 = map(int, box.xyxy[0])
    
    # Ambil nama bumbu yang terdeteksi
    id_kelas = int(box.cls[0])
    nama_bumbu = model.names[id_kelas]
    
    # Ambil informasi dari kamus (jika tidak ada, tampilkan pesan default)
    info_ekstra = INFO_BUMBU.get(nama_bumbu, "Informasi belum tersedia.")
    
    # Buat teks gabungan (Nama Bumbu + Informasi)
    teks_tampil = f"{nama_bumbu.upper()} - {info_ekstra}"
    
    # Gambar Kotak (Warna Hijau, ketebalan 2)
    cv2.rectangle(gambar_asli, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    # Background untuk teks agar mudah dibaca (Hitam)
    cv2.rectangle(gambar_asli, (x1, y1 - 30), (x1 + len(teks_tampil) * 10, y1), (0, 0, 0), -1)
    
    # Gambar Teks (Warna Putih)
    cv2.putText(gambar_asli, teks_tampil, (x1 + 5, y1 - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

# ==============================================================================
# 5. TAMPILKAN HASILNYA
# ==============================================================================
cv2.imshow("Kamus Pintar Bumbu AI", gambar_asli)
cv2.waitKey(0) # Menunggu kamu menekan tombol apa saja di keyboard untuk menutup gambar
cv2.destroyAllWindows()