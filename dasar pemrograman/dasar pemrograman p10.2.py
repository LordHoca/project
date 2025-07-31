import quis_dasar_pemrograman 

def main():
    try:
        jumlah_data = int(input("Masukkan jumlah data: "))
        
        if jumlah_data <= 0:
            print("Jumlah data harus lebih besar dari 0.")
            return
        
        rata_rata = quis_dasar_pemrograman.hitung_rata_rata(jumlah_data)
        print(f"Rata-rata nilai dari {jumlah_data} data adalah: {rata_rata:.2f}")
    
    except ValueError:
        print("Input tidak valid. Harap masukkan angka untuk jumlah data.")

if __name__ == "__main__":
    main()