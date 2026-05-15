import pandas as pd
import matplotlib.pyplot as plt

# Baca file hasil training
results = pd.read_csv('detect/model_bumbu_masak-2/results.csv')

# Bersihkan nama kolom (menghapus spasi)
results.columns = results.columns.str.strip()

# Plot mAP50 (Akurasi)
plt.figure(figsize=(10, 5))
plt.plot(results['metrics/mAP50(B)'], label='Akurasi (mAP50)')
plt.title('Performa Model per Epoch')
plt.xlabel('Epoch')
plt.ylabel('Akurasi')
plt.legend()
plt.grid()
plt.show()