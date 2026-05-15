from ultralytics import YOLO
import cv2

# 1. Load model (Disarankan pakai best.pt jika training sudah selesai)
model = YOLO('detect/model_bumbu_masak-2/weights/last.pt')

# 2. Buka kamera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Jalankan deteksi
    # conf=0.6 adalah ambang batas keyakinan
    results = model.predict(frame, conf=0.6)

    # Cek apakah ada objek yang terdeteksi
    if len(results[0].boxes) > 0:
        # Jika ADA bumbu, gambar kotak asli dari YOLO
        annotated_frame = results[0].plot()
    else:
        # Jika TIDAK ADA bumbu yang dikenali (kosong), tampilkan teks manual
        annotated_frame = frame.copy()
        cv2.putText(
            annotated_frame, 
            "Tidak ada dalam daftar bumbu", 
            (50, 50),                   # Posisi teks (x, y)
            cv2.FONT_HERSHEY_SIMPLEX,   # Jenis font
            1,                          # Skala font
            (0, 0, 255),                # Warna (BGR) -> Merah
            2,                          # Ketebalan garis
            cv2.LINE_AA
        )

    # Tampilkan hasil di jendela
    cv2.imshow("Deteksi Bumbu Dapur YOLO", annotated_frame)

    # Tekan 'q' untuk berhenti
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()