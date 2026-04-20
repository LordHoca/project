import cv2
import numpy as np
import tensorflow as tf
import os
import time

# 1. Pengaturan Awal
lokasi_dataset = "data_set_bunga" # Pastikan nama folder ini sesuai dengan milik Anda

print("Memuat model...")
model = tf.keras.models.load_model("model_bunga.h5")

with open("nama_kelas.txt", "r") as f:
    nama_kelas = [baris.strip() for baris in f.readlines()]

# 2. Menyalakan Kamera
kamera = cv2.VideoCapture(0)
print("=========================================")
print("Kamera menyala!")
print("- Tekan 'y' apabila gambar sudah sesuai")
print("- Tekan 'q' untuk KELUAR")
print("=========================================")

while True:
    ret, frame = kamera.read()
    if not ret:
        break

    # 3. Pra-pemrosesan gambar (termasuk perbaikan warna BGR ke RGB)
    gambar_resize = cv2.resize(frame, (224, 224))
    gambar_rgb = cv2.cvtColor(gambar_resize, cv2.COLOR_BGR2RGB) # Perbaikan warna
    gambar_array = np.expand_dims(gambar_rgb, axis=0)

    # 4. Melakukan Prediksi
    prediksi = model.predict(gambar_array, verbose=0)
    indeks_tertinggi = np.argmax(prediksi[0])
    kategori_ditebak = nama_kelas[indeks_tertinggi]
    tingkat_keyakinan = prediksi[0][indeks_tertinggi] * 100

    # 5. Menampilkan teks di layar
    teks_hasil = f"{kategori_ditebak} ({tingkat_keyakinan:.1f}%)"
    
    # Warna teks: Hijau jika yakin (>60%), Merah jika ragu (<60%)
    warna_teks = (0, 255, 0) if tingkat_keyakinan > 60.0 else (0, 0, 255)
    
    cv2.putText(frame, teks_hasil, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, warna_teks, 2)
    cv2.putText(frame, "Tekan 'y' untuk simpan data", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)

    # Menampilkan jendela video
    cv2.imshow("Deteksi Tanaman AI", frame)

    # 6. Menangkap input keyboard
    tombol = cv2.waitKey(1) & 0xFF
    
    if tombol == ord('q'):
        break # Keluar dari program
        
    elif tombol == ord('y'):
        # Fitur Auto-Save ke Dataset
        if tingkat_keyakinan > 50.0:
            # Membuat nama file unik berdasarkan waktu saat ini
            nama_file = f"{kategori_ditebak}_{int(time.time())}.jpg"
            
            # Memastikan folder tujuan ada
            folder_tujuan = os.path.join(lokasi_dataset, kategori_ditebak)
            os.makedirs(folder_tujuan, exist_ok=True)
            
            # Menyimpan gambar asli (frame) ke folder yang sesuai
            path_simpan = os.path.join(folder_tujuan, nama_file)
            cv2.imwrite(path_simpan, frame)
            
            print(f"✅ BERHASIL: Gambar sesuai prediksi {path_simpan}")
            
            # Memberikan efek visual (layar berkedip putih sejenak)
            cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), (255, 255, 255), -1)
            cv2.imshow("Deteksi Bunga AI", frame)
            cv2.waitKey(100)
        else:
            print("⚠️ PREDIKSI KURANG TEPAT: Model masih ragu dengan gambar ini (Akurasi di bawah 50%)")

# Membersihkan dan menutup kamera
kamera.release()
cv2.destroyAllWindows()