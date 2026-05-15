import os
import random

# --- KONFIGURASI ---
images_path = 'train/images'
labels_path = 'train/labels'
TARGET = 1800

def get_stats():
    """Menghitung jumlah riil tiap objek bumbu."""
    stats = {}
    file_list = [f for f in os.listdir(labels_path) if f.endswith('.txt')]
    for f in file_list:
        with open(os.path.join(labels_path, f), 'r') as file:
            for line in file:
                parts = line.split()
                if len(parts) > 0: # Pastikan baris tidak kosong
                    cls = parts[0]
                    stats[cls] = stats.get(cls, 0) + 1
    return stats, file_list

def strict_balancing():
    print(f"Memulai penyeimbangan ketat ke target {TARGET}...")
    
    # Ambil statistik awal
    current_stats, all_files = get_stats()
    
    # Cari kelas yang sudah 'obesitas' (lebih dari target)
    over_classes = [cls for cls, count in current_stats.items() if count > TARGET]
    
    if not over_classes:
        print("Semua bumbu sudah pas atau di bawah target!")
        return

    # Acak daftar file agar penghapusan tidak berat sebelah
    random.shuffle(all_files)
    files_deleted = 0

    for f_txt in all_files:
        label_full_path = os.path.join(labels_path, f_txt)
        
        # Baca isi file dengan aman
        with open(label_full_path, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            
        # Cek apakah file ini mengandung bumbu yang jumlahnya berlebih
        is_culprit = False
        for line in lines:
            class_id = line.split()[0]
            if class_id in over_classes:
                is_culprit = True
                break
        
        # Jika mengandung bumbu berlebih, kita hapus filenya
        if is_culprit:
            base_name = os.path.splitext(f_txt)[0]
            
            # Hapus file teks
            if os.path.exists(label_full_path):
                os.remove(label_full_path)
            
            # Hapus file gambar (cek berbagai ekstensi)
            for ext in ['.jpg', '.jpeg', '.png']:
                img_p = os.path.join(images_path, base_name + ext)
                if os.path.exists(img_p):
                    os.remove(img_p)
            
            files_deleted += 1

            # Update statistik setiap 50 penghapusan agar tidak menghapus terlalu banyak
            if files_deleted % 50 == 0:
                current_stats, _ = get_stats()
                over_classes = [cls for cls, count in current_stats.items() if count > TARGET]
                if not over_classes:
                    break

    print("-" * 30)
    print(f"Misi Selesai! Menghapus {files_deleted} file.")
    print("Silakan jalankan script 'hitung jumlah' kamu lagi untuk cek hasil akhirnya.")

if __name__ == "__main__":
    strict_balancing()