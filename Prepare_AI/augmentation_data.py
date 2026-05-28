import os
import shutil
import random
from collections import Counter
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import albumentations as A

# --- KONFIGURASI ---
dataset_dir = 'Final_Dataset'  # Ganti dengan path dataset kamu
images_dir = os.path.join(dataset_dir, 'images')
labels_dir = os.path.join(dataset_dir, 'labels')
augmented_output_dir = os.path.join(dataset_dir, 'augmented')

# Buat direktori output jika belum ada
os.makedirs(os.path.join(augmented_output_dir, 'images'), exist_ok=True)
os.makedirs(os.path.join(augmented_output_dir, 'labels'), exist_ok=True)

# ============ FUNGSI AUGMENTASI ============

def read_yolo_labels(label_path):
    """Membaca label YOLO dalam format (class_id center_x center_y width height)"""
    bboxes = []
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            for line in f:
                values = line.strip().split()
                if len(values) >= 5:
                    bboxes.append([float(v) for v in values])
    return bboxes

def write_yolo_labels(label_path, bboxes):
    """Menyimpan label YOLO"""
    with open(label_path, 'w') as f:
        for bbox in bboxes:
            f.write(' '.join(map(str, bbox)) + '\n')

def convert_yolo_to_albumentations(bboxes, img_height, img_width):
    """Konversi format YOLO ke format Albumentations"""
    alb_bboxes = []
    for bbox in bboxes:
        class_id = int(bbox[0])
        center_x, center_y, width, height = bbox[1], bbox[2], bbox[3], bbox[4]
        
        # Konversi dari center format ke corner format (x_min, y_min, x_max, y_max)
        x_min = center_x - width / 2
        y_min = center_y - height / 2
        x_max = center_x + width / 2
        y_max = center_y + height / 2
        
        alb_bboxes.append([x_min, y_min, x_max, y_max, class_id])
    return alb_bboxes

def convert_albumentations_to_yolo(bboxes, img_height, img_width):
    """Konversi format Albumentations kembali ke YOLO"""
    yolo_bboxes = []
    for bbox in bboxes:
        x_min, y_min, x_max, y_max, class_id = bbox
        
        center_x = (x_min + x_max) / 2
        center_y = (y_min + y_max) / 2
        width = x_max - x_min
        height = y_max - y_min
        
        yolo_bboxes.append([int(class_id), center_x, center_y, width, height])
    return yolo_bboxes

def augment_image_with_albumentations(image, bboxes, augmentation_type):
    """Augmentasi gambar menggunakan Albumentations"""
    
    h, w = image.shape[:2]
    alb_bboxes = convert_yolo_to_albumentations(bboxes, h, w)
    
    # Definisikan transformasi berdasarkan tipe augmentasi
    transforms = {
        'flip_h': A.HorizontalFlip(p=1.0),
        'flip_v': A.VerticalFlip(p=1.0),
        'rotate_15': A.Rotate(limit=15, p=1.0, border_mode=cv2.BORDER_REFLECT),
        'rotate_30': A.Rotate(limit=30, p=1.0, border_mode=cv2.BORDER_REFLECT),
      
    }
    
    transform = A.Compose(
        [transforms.get(augmentation_type, A.NoOp())],
        bbox_params=A.BboxParams(format='albumentations', min_visibility=0.3)
    )
    
    transformed = transform(image=image, bboxes=alb_bboxes)
    augmented_image = transformed['image']
    augmented_bboxes = transformed['bboxes']
    
    if augmented_bboxes:
        yolo_bboxes = convert_albumentations_to_yolo(augmented_bboxes, h, w)
    else:
        yolo_bboxes = []
    
    return augmented_image, yolo_bboxes

def simple_augment_brightness(image, factor=1.3):
    """Augmentasi brightness sederhana menggunakan PIL"""
    pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    enhancer = ImageEnhance.Brightness(pil_img)
    enhanced = enhancer.enhance(factor)
    return cv2.cvtColor(np.array(enhanced), cv2.COLOR_RGB2BGR)

def simple_augment_contrast(image, factor=1.3):
    """Augmentasi contrast sederhana menggunakan PIL"""
    pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    enhancer = ImageEnhance.Contrast(pil_img)
    enhanced = enhancer.enhance(factor)
    return cv2.cvtColor(np.array(enhanced), cv2.COLOR_RGB2BGR)

def apply_augmentations(input_images_dir, input_labels_dir, output_images_dir, output_labels_dir, 
                        augmentation_types=None, multiplier=1):
    """
    Terapkan augmentasi ke semua gambar dalam dataset
    
    Args:
        multiplier: Berapa kali lipat data akan di-augmentasi (default: 1, berarti setiap gambar di-augmentasi 1x)
    """
    
    if augmentation_types is None:
        augmentation_types = ['flip_h', 'flip_v', 'rotate_15', 'brightness', 'contrast']
    
    image_files = [f for f in os.listdir(input_images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"Total gambar ditemukan: {len(image_files)}")
    print(f"Tipe augmentasi: {augmentation_types}")
    print(f"Multiplier: {multiplier}x\n")
    
    aug_count = 0
    
    for idx, img_file in enumerate(image_files):
        base_name = os.path.splitext(img_file)[0]
        img_ext = os.path.splitext(img_file)[1]
        label_file = base_name + '.txt'
        
        img_path = os.path.join(input_images_dir, img_file)
        label_path = os.path.join(input_labels_dir, label_file)
        
        # Baca gambar dan label
        image = cv2.imread(img_path)
        bboxes = read_yolo_labels(label_path)
        
        if image is None:
            print(f"[{idx+1}/{len(image_files)}] Gagal membaca: {img_file}")
            continue
        
        # Simpan gambar original
        output_img_path = os.path.join(output_images_dir, img_file)
        output_label_path = os.path.join(output_labels_dir, label_file)
        shutil.copy(img_path, output_img_path)
        shutil.copy(label_path, output_label_path)
        
        print(f"[{idx+1}/{len(image_files)}] Mengaugmentasi: {img_file}")
        
        # Terapkan augmentasi sesuai multiplier
        for mult in range(multiplier):
            for aug_type in augmentation_types:
                try:
                    augmented_img, augmented_bboxes = augment_image_with_albumentations(image, bboxes, aug_type)
                    
                    # Buat nama file baru
                    new_name = f"aug_{aug_type}_{mult}_{base_name}"
                    new_img_path = os.path.join(output_images_dir, new_name + img_ext)
                    new_label_path = os.path.join(output_labels_dir, new_name + '.txt')
                    
                    # Simpan gambar augmented
                    cv2.imwrite(new_img_path, augmented_img)
                    
                    # Simpan label augmented
                    write_yolo_labels(new_label_path, augmented_bboxes)
                    aug_count += 1
                    
                except Exception as e:
                    print(f"  Error saat augmentasi {aug_type}: {e}")
    
    print(f"\n✓ Proses augmentasi selesai!")
    print(f"Total gambar augmented: {aug_count}")

# ============ FUNGSI PENYEIMBANGAN ============

def balance_only_minority(min_threshold=500):
    """Penyeimbangan data dengan duplikasi sederhana"""
    label_files = [f for f in os.listdir(labels_dir) if f.endswith('.txt')]
    class_stats = Counter()
    file_map = {}

    for lf in label_files:
        with open(os.path.join(labels_dir, lf), 'r') as f:
            lines = f.readlines()
            if lines:
                cls = lines[0].split()[0]
                class_stats[cls] += 1
                if cls not in file_map:
                    file_map[cls] = []
                file_map[cls].append(lf)

    print("Statistik Kelas:")
    for cls, count in sorted(class_stats.items()):
        print(f"  Kelas {cls}: {count} gambar")
    print()

    for cls, count in class_stats.items():
        if count < min_threshold:
            to_add = min_threshold - count
            print(f"Kelas {cls} hanya ada {count}. Menambah {to_add} data...")
            
            for i in range(to_add):
                src_label = random.choice(file_map[cls])
                base_name = os.path.splitext(src_label)[0]
                
                exts = ['.jpg', '.jpeg', '.png']
                found_img = False
                for ex in exts:
                    if os.path.exists(os.path.join(images_dir, base_name + ex)):
                        src_img = base_name + ex
                        found_img = True
                        break
                
                if found_img:
                    new_name = f"bal_min_{cls}_{i}_{base_name}"
                    shutil.copy(os.path.join(images_dir, src_img), 
                              os.path.join(images_dir, new_name + os.path.splitext(src_img)[1]))
                    shutil.copy(os.path.join(labels_dir, src_label), 
                              os.path.join(labels_dir, new_name + ".txt"))

    print("✓ Proses penyeimbangan data minoritas selesai!\n")

# ============ MAIN EXECUTION ============

if __name__ == "__main__":
    # Pilihan 1: Hanya penyeimbangan data
    # balance_only_minority(min_threshold=500)
    
    # Pilihan 2: Augmentasi dengan berbagai teknik
    augmentation_types = [
        'flip_h',      # Flip horizontal
        'flip_v',      # Flip vertikal
        'rotate_15',   # Rotasi 15 derajat
        'rotate_30',   # Rotasi 30 derajat
       
    ]
    
    apply_augmentations(
        input_images_dir=images_dir,
        input_labels_dir=labels_dir,
        output_images_dir=os.path.join(augmented_output_dir, 'images'),
        output_labels_dir=os.path.join(augmented_output_dir, 'labels'),
        augmentation_types=augmentation_types,
        multiplier=1  # Setiap gambar akan di-augmentasi 1 kali untuk setiap tipe augmentasi
    )
