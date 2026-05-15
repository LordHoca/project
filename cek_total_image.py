import os
import yaml
from collections import Counter

# --- KONFIGURASI ---
# Sesuaikan dengan lokasi file data.yaml dan folder labels kamu
YAML_PATH = 'bumbu_masak.yaml' 
LABELS_FOLDER = 'train/labels' 

# 1. Load nama kelas dari file YAML
with open(YAML_PATH, 'r') as f:
    data = yaml.safe_load(f)
    class_names = data['names']

# 2. Hitung kemunculan setiap ID kelas di semua file .txt
label_counts = Counter()

# List semua file .txt di folder labels
label_files = [f for f in os.listdir(LABELS_FOLDER) if f.endswith('.txt')]

for file in label_files:
    with open(os.path.join(LABELS_FOLDER, file), 'r') as f:
        for line in f:
            if line.strip():
                class_id = int(line.split()[0])
                label_counts[class_id] += 1

# 3. Tampilkan hasil secara rapi
print("-" * 30)
print(f"{'Nama Bumbu':<20} | {'Jumlah':<5}")
print("-" * 30)

total_instances = 0
if isinstance(class_names, list):
    for class_id, name in enumerate(class_names):
        count = label_counts.get(class_id, 0)
        print(f"{name:<20} | {count:<5}")
        total_instances += count
# Jika class_names adalah Dictionary (format lama)
else:
    for class_id, name in class_names.items():
        count = label_counts.get(class_id, 0)
        print(f"{name:<20} | {count:<5}")
        total_instances += count

print("-" * 30)
print(f"Total Seluruh Objek: {total_instances}")
print(f"Total File Gambar: {len(label_files)}")

print("-" * 30)
print(f"Total Seluruh Objek: {total_instances}")
print(f"Total File Gambar: {len(label_files)}")