import os
import shutil

# ==============================================================================
# 1. KONFIGURASI FOLDER
# ==============================================================================
# Ganti dengan path dataset ORIGINAL kamu (Dataset A atau Dataset B)
DIR_IMAGES_ASAL = 'Dataset_Point/Dataset_B/train/images'
DIR_LABELS_ASAL = 'Dataset_Point/Dataset_B/train/labels'
# Ganti dengan path folder Master yang baru kamu buat di Langkah 1
DIR_IMAGES_TUJUAN = 'Final_Dataset/images'
DIR_LABELS_TUJUAN = 'Final_Dataset/labels'

# ==============================================================================
# 2. ATURAN PEMETAAN ID (UBAH SESUAI DATASET YANG SEDANG DIPROSES)
# ==============================================================================
# Format: {ID_DI_DATASET_ASAL : ID_DI_KAMUS_MASTER}

# CONTOH UNTUK DATASET B (Dataset Lama yang ada Daun Salam-nya):
MAPPING_ID = {
    0: 8,   # jahe
    1: 9,   # kemiri
    2: 10,  # kencur

}


# (Nanti saat menjalankan script untuk Dataset B, ganti MAPPING_ID 
# sesuai dengan urutan asli bumbu di Dataset B menuju Kamus Master)

def copy_dan_remap_dataset():
    print("Memulai proses pemindahan dan remapping...\n")
    os.makedirs(DIR_IMAGES_TUJUAN, exist_ok=True)
    os.makedirs(DIR_LABELS_TUJUAN, exist_ok=True)

    file_txt_list = [f for f in os.listdir(DIR_LABELS_ASAL) if f.endswith('.txt')]
    berhasil = 0

    for file_txt in file_txt_list:
        path_label_asal = os.path.join(DIR_LABELS_ASAL, file_txt)
        path_label_tujuan = os.path.join(DIR_LABELS_TUJUAN, file_txt)
        
        # Cari file gambar pasangannya (.jpg, .jpeg, .png)
        nama_file_tanpa_ext = os.path.splitext(file_txt)[0]
        file_gambar_ditemukan = None
        for ext in ['.jpg', '.jpeg', '.png']:
            path_img_asal = os.path.join(DIR_IMAGES_ASAL, nama_file_tanpa_ext + ext)
            if os.path.exists(path_img_asal):
                file_gambar_ditemukan = path_img_asal
                break
        
        # Jika gambarnya tidak ada, lewati
        if not file_gambar_ditemukan:
            continue

        # Proses baca dan ubah label
        with open(path_label_asal, 'r') as file:
            lines = file.readlines()

        new_lines = []
        label_valid = False

        for line in lines:
            parts = line.split()
            if len(parts) > 0:
                try:
                    old_id = int(parts[0])
                    # Hanya proses ID yang ada di MAPPING_ID (Daun salam akan tersaring dibuang)
                    if old_id in MAPPING_ID:
                        parts[0] = str(MAPPING_ID[old_id])
                        new_lines.append(" ".join(parts) + "\n")
                        label_valid = True
                except ValueError:
                    continue

        # Jika ada label yang valid (bukan daun salam), copy gambar dan simpan label baru
        if label_valid:
            with open(path_label_tujuan, 'w') as file:
                file.writelines(new_lines)
            
            path_img_tujuan = os.path.join(DIR_IMAGES_TUJUAN, os.path.basename(file_gambar_ditemukan))
            shutil.copy2(file_gambar_ditemukan, path_img_tujuan)
            berhasil += 1

    print(f"✅ Selesai! Berhasil memproses {berhasil} pasangan gambar & label.")

if __name__ == "__main__":
    copy_dan_remap_dataset()