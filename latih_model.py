import tensorflow as tf
from tensorflow.keras import layers, models


lokasi_data_set_training = "data_set_bunga/Training"
lokasi_data_set_validasi = "data_set_bunga/Validate"
uk_gambar = (224, 224)
batch_size = 32

print ("Mempersiapkan data set...")
train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    lokasi_data_set_training,
    image_size = uk_gambar,
    batch_size = batch_size
)

validasi_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    lokasi_data_set_validasi,
    image_size = uk_gambar,
    batch_size = batch_size
)

nama_kelas = train_dataset.class_names
print("Termasuk Kelas : ", nama_kelas)

data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal_and_vertical"),
    layers.RandomRotation(0.2),
    layers.RandomZoom(0.2),
])

print("Membuat model CNN...")
model = models.Sequential([
    layers.Rescaling(1./255, input_shape=(224, 224, 3)),
    
    layers.Conv2D(16, 6, padding ='same', activation = 'relu'),
    layers.MaxPooling2D(),
    
    layers.Conv2D(32, 6, padding ='same', activation = 'relu'),
    layers.MaxPooling2D(),
    
    layers.Conv2D(64,6, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(len(nama_kelas), activation='softmax')
])

print("Menyusun Model...")
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(),
              metrics=['accuracy'])

penghenti_otomatis = tf.keras.callbacks.EarlyStopping(
    monitor='val_accuracy',       # Yang dipantau adalah akurasi dari tebakan data baru
    patience=5,                   # Berapa putaran AI diberi toleransi tidak ada peningkatan sebelum disetop
    restore_best_weights=True     # SANGAT PENTING: Mengembalikan memori AI ke putaran dengan akurasi tertinggi
)

print('Melatih Model...')
epochs=100
history = model.fit(
    train_dataset,
    validation_data = validasi_dataset,
    epochs= epochs,
    callbacks= [penghenti_otomatis]
)

print('Menyimpan Model...')
model.save('model_bunga.h5')
with open("nama_kelas.txt", "w") as f:
    for nama in nama_kelas:
        f.write(nama + "\n")
        
print("Pelatihan Selesai!, Model disimpan sebagai 'model_bunga.h5'")        

