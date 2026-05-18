import os
import random
import shutil

# --- KONFIGURASI FOLDER ---
# Tentukan di mana folder data mentahmu berada saat ini
src_images = 'train1/train/images'
src_labels = 'train1/train/labels'

# Tentukan folder tujuan hasil split
output_base = 'dataset_final'

# --- PROPORSI SPLIT ---
TRAIN_RATIO = 0.70
VAL_RATIO = 0.20
# Sisa 10% otomatis menjadi TEST_RATIO

def buat_folder_yolo():
    """Membuat struktur folder standar YOLOv8/YOLO11."""
    for split in ['train', 'val', 'test']:
        os.makedirs(os.path.join(output_base, split, 'images'), exist_ok=True)
        os.makedirs(os.path.join(output_base, split, 'labels'), exist_ok=True)

def split_dataset():
    buat_folder_yolo()
    
    # Ambil semua file teks di folder labels mentah
    all_labels = [f for f in os.listdir(src_labels) if f.endswith('.txt')]
    
    # Acak urutan file agar distribusinya adil
    random.shuffle(all_labels)
    
    total_files = len(all_labels)
    train_bound = int(total_files * TRAIN_RATIO)
    val_bound = int(total_files * (TRAIN_RATIO + VAL_RATIO))
    
    print(f"Total file berpasangan ditemukan: {total_files}")
    print(f"Membagi data: Train ({train_bound}), Val ({val_bound - train_bound}), Test ({total_files - val_bound})")
    print("-" * 50)
    
    for idx, f_txt in enumerate(all_labels):
        base_name = os.path.splitext(f_txt)[0]
        
        # Cari file gambar yang cocok dengan nama file teks tersebut
        img_file = None
        for ext in ['.jpg', '.jpeg', '.png']:
            if os.path.exists(os.path.join(src_images, base_name + ext)):
                img_file = base_name + ext
                break
                
        # Jika gambar pasangannya tidak ditemukan, lewati file ini
        if not img_file:
            print(f"Peringatan: Gambar untuk {f_txt} tidak ditemukan. Dilewati.")
            continue
            
        # Tentukan target folder berdasarkan index rasio
        if idx < train_bound:
            target_split = 'train'
        elif idx < val_bound:
            target_split = 'val'
        else:
            target_split = 'test'
            
        # Tentukan path tujuan yang baru
        dest_img_dir = os.path.join(output_base, target_split, 'images')
        dest_lbl_dir = os.path.join(output_base, target_split, 'labels')
        
        # Pindahkan file (gunakan shutil.copy jika ingin menduplikasi, gunakan shutil.move jika ingin memindahkan)
        shutil.copy(os.path.join(src_images, img_file), os.path.join(dest_img_dir, img_file))
        shutil.copy(os.path.join(src_labels, f_txt), os.path.join(dest_lbl_dir, f_txt))
        
    print("PROSES SELESAI! Folder 'dataset_final' kamu sudah siap digunakan untuk training.")

if __name__ == "__main__":
    split_dataset()