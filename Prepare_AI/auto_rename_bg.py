import os

# --- KONFIGURASI PATH ---
images_path = 'train/images'
labels_path = 'train/labels'

def process_background_images():
    # Pastikan folder labels ada
    if not os.path.exists(labels_path):
        os.makedirs(labels_path)

    # Ambil semua file gambar
    image_files = [f for f in os.listdir(images_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    counter = 1
    count_processed = 0
    
    print("Mulai memproses gambar background baru...")
    print("-" * 40)

    for img_file in image_files:
        base_name, ext = os.path.splitext(img_file)
        txt_path = os.path.join(labels_path, f"{base_name}.txt")
        
        # LOGIKA: Jika gambar ini TIDAK PUNYA file .txt, berarti ini gambar baru dari HP-mu
        if not os.path.exists(txt_path):
            
            # Cari nomor urut yang belum dipakai agar tidak menimpa file lama
            while True:
                new_base_name = f"bg_bukan_bumbu_{counter:03d}" # Contoh: bg_bukan_bumbu_001
                new_img_name = new_base_name + ext
                new_img_path = os.path.join(images_path, new_img_name)
                
                if not os.path.exists(new_img_path):
                    break
                counter += 1
            
            old_img_path = os.path.join(images_path, img_file)
            new_txt_path = os.path.join(labels_path, new_base_name + ".txt")
            
            # 1. Ganti nama gambar
            os.rename(old_img_path, new_img_path)
            
            # 2. Buat file label kosong
            with open(new_txt_path, 'w') as f:
                pass
                
            print(f"Berhasil: {img_file}  -->  {new_img_name}")
            count_processed += 1
            counter += 1

    print("-" * 40)
    print(f"SELESAI! {count_processed} gambar berhasil diubah namanya dan dibuatkan label kosong.")

if __name__ == "__main__":
    process_background_images()