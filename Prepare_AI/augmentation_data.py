import os
import shutil
import random
from collections import Counter

# --- KONFIGURASI ---
dataset_dir = 'Final_Dataset' # Ganti dengan path dataset kamu
images_dir = os.path.join(dataset_dir, 'images')
labels_dir = os.path.join(dataset_dir, 'labels')

def balance_only_minority(min_threshold=500):
    # 1. Hitung jumlah tiap kelas
    label_files = [f for f in os.listdir(labels_dir) if f.endswith('.txt')]
    class_stats = Counter()
    file_map = {} # Untuk mencatat file mana milik kelas mana

    for lf in label_files:
        with open(os.path.join(labels_dir, lf), 'r') as f:
            lines = f.readlines()
            if lines:
                cls = lines[0].split()[0] # Ambil ID kelas pertama
                class_stats[cls] += 1
                if cls not in file_map: file_map[cls] = []
                file_map[cls].append(lf)

    # 2. Proses penyeimbangan hanya untuk yang di bawah ambang batas (threshold)
    for cls, count in class_stats.items():
        if count < min_threshold:
            to_add = min_threshold - count
            print(f"Kelas {cls} hanya ada {count}. Menambah {to_add} data...")
            
            for i in range(to_add):
                src_label = random.choice(file_map[cls])
                base_name = os.path.splitext(src_label)[0]
                
                # Cari gambar pasangannya
                exts = ['.jpg', '.jpeg', '.png']
                found_img = False
                for ex in exts:
                    if os.path.exists(os.path.join(images_dir, base_name + ex)):
                        src_img = base_name + ex
                        found_img = True
                        break
                
                if found_img:
                    new_name = f"bal_min_{cls}_{i}_{base_name}"
                    shutil.copy(os.path.join(images_dir, src_img), os.path.join(images_dir, new_name + os.path.splitext(src_img)[1]))
                    shutil.copy(os.path.join(labels_dir, src_label), os.path.join(labels_dir, new_name + ".txt"))

    print("Proses penyeimbangan data minoritas selesai!")

balance_only_minority(min_threshold=500) # Angka 500 disesuaikan dengan Halia Keringmu