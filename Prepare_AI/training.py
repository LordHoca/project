from ultralytics import YOLO

# 1. Gunakan model dasar YOLOv11 nano (cepat dan ringan)
model = YOLO('yolo26s.pt')

# 2. Mulai proses belajar
model.train(
    data='data.yaml',    # File yaml yang kita buat tadi
    epochs=100,            # Berapa kali model belajar ulang (bisa ditambah ke 100)
    imgsz=640,            # Ukuran standar gambar YOLO
    batch=12,             # Jumlah gambar per proses (sesuaikan dengan RAM/VRAM)
    patience=10,         # Berapa lama model menunggu sebelum berhenti jika tidak ada peningkatan
    name='model_bumbu_masak'    # Nama folder hasil training
)
