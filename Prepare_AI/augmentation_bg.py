import os
import cv2
import numpy as np
import random

# --- KONFIGURASI ---
img_path = 'train/images'
lab_path = 'train/labels'
target_bg_total = 200  # Target jumlah foto background yang diinginkan

def augment_background():
    # Ambil daftar file background (yang namanya ada 'bg_bukan_bumbu')
    bg_files = [f for f in os.listdir(img_path) if 'bg_bukan_bumbu' in f]
    
    if not bg_files:
        print("Error: Tidak ditemukan file dengan nama 'bg_bukan_bumbu'.")
        return

    current_count = len(bg_files)
    to_augment = target_bg_total - current_count
    
    print(f"Menambah {to_augment} variasi background...")

    for i in range(to_augment):
        # Pilih foto background asli secara acak
        src_name = random.choice(bg_files)
        img = cv2.imread(os.path.join(img_path, src_name))
        
        # Lakukan manipulasi sederhana (Flip & Brightness)
        if random.random() > 0.5:
            img = cv2.flip(img, 1) # Flip horizontal
        
        # Ubah kecerahan secara acak
        value = random.randint(-50, 50)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = cv2.add(v, value)
        v[v > 255] = 255
        v[v < 0] = 0
        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

        # Simpan hasil
        new_name = f"aug_bg_{i}_{src_name}"
        cv2.imwrite(os.path.join(img_path, new_name), img)
        
        # Buat label kosongnya
        with open(os.path.join(lab_path, new_name.replace(os.path.splitext(new_name)[1], '.txt')), 'w') as f:
            pass

    print("Selesai memperbanyak data background!")

augment_background()