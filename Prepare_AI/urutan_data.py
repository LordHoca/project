import os

# ==============================================================================
# 1. KONFIGURASI FOLDER
# ==============================================================================
# Ganti dengan path folder Master milikmu
DIR_IMAGES = r'Final_Dataset\images'
DIR_LABELS = r'Final_Dataset\labels'

# ==============================================================================
# 2. KAMUS MASTER BUMBU (URUTAN ID 0 - 14)
# ==============================================================================
BUMBU_MAP = {
    0: "biji ketumbar", 1: "bunga cengkih", 2: "bunga lawang", 
    3: "cili kering", 4: "jintan manis", 5: "jintan putih", 
    6: "kayu manis", 7: "lada hitam", 8: "jahe", 
    9: "kemiri", 10: "kencur"

}

def validasi_total_dataset():
    print("\n" + "="*70)
    print("🔍 TAHAP 1: MEMERIKSA KESEHATAN FILE GAMBAR & LABEL...")
    print("="*70)
    
    if not os.path.exists(DIR_IMAGES) or not os.path.exists(DIR_LABELS):
        print("❌ ERROR: Folder tidak ditemukan! Periksa kembali jalur (path) foldernya.")
        return

    images = [f for f in os.listdir(DIR_IMAGES) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    labels = [f for f in os.listdir(DIR_LABELS) if f.lower().endswith('.txt')]

    img_names = set([os.path.splitext(f)[0] for f in images])
    lbl_names = set([os.path.splitext(f)[0] for f in labels])

    img_tanpa_label = img_names - lbl_names
    lbl_tanpa_img = lbl_names - img_names

    dataset_sehat = True

    if img_tanpa_label:
        print(f"⚠️ Ditemukan {len(img_tanpa_label)} gambar tanpa file .txt (label): {list(img_tanpa_label)[:3]}...")
        dataset_sehat = False
    
    if lbl_tanpa_img:
        print(f"⚠️ Ditemukan {len(lbl_tanpa_img)} file .txt tanpa gambar: {list(lbl_tanpa_img)[:3]}...")
        dataset_sehat = False

    if dataset_sehat:
        print("✅ AMAN: Semua gambar dan label memiliki pasangan yang tepat.\n")
    else:
        print("🛑 PERINGATAN: Ada file yang tidak berpasangan. Sebaiknya hapus file tersebut agar tidak error saat training.\n")

    print("="*70)
    print("📊 TAHAP 2: MENGHITUNG URUTAN DATA (JUMLAH OBJEK BUMBU)")
    print("="*70)

    # Inisialisasi dictionary untuk menghitung objek
    stats_bumbu = {id_kelas: 0 for id_kelas in BUMBU_MAP}
    total_objek = 0
    total_objek_tidak_dikenal = 0

    # Mulai menghitung isi file txt
    for file_txt in labels:
        path_label = os.path.join(DIR_LABELS, file_txt)
        
        # Abaikan file kosong
        if os.path.getsize(path_label) == 0:
            continue

        with open(path_label, 'r') as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split()
                if len(parts) > 0:
                    try:
                        id_kelas = int(parts[0])
                        if id_kelas in stats_bumbu:
                            stats_bumbu[id_kelas] += 1
                            total_objek += 1
                        else:
                            total_objek_tidak_dikenal += 1
                    except ValueError:
                        continue

    # Tampilkan tabel hasil
    print(f"{'NAMA BUMBU MASAKAN':<20} | {'ID':<4} | {'JUMLAH OBJEK'}")
    print("-" * 50)
    for id_kelas, nama_bumbu in BUMBU_MAP.items():
        jumlah = stats_bumbu[id_kelas]
        peringatan = " ⚠️ (KOSONG)" if jumlah == 0 else ""
        print(f"{nama_bumbu:<20} | {id_kelas:<4} | {jumlah}{peringatan}")
    
    print("-" * 50)
    print(f"Total Keseluruhan Objek  : {total_objek}")
    print(f"Total File Gambar        : {len(images)}")
    
    if total_objek_tidak_dikenal > 0:
        print(f"⚠️ Ada {total_objek_tidak_dikenal} objek dengan ID tidak dikenal (di luar 0-14).")

    print("="*70 + "\n")

if __name__ == "__main__":
    validasi_total_dataset()