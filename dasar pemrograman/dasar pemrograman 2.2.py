# Daftar harga ayam
harga_ayam = {
    'D': 2500,  # Dada
    'P': 2000,  # Paha
    'S': 1500   # Sayap
}

def hitung_total(jenis, jumlah):
    return harga_ayam[jenis] * jumlah

def main():
    total_bayar = 0
    while True:
        print("\nDaftar Harga Ayam:")
        print("D - Dada : Rp. 2500")
        print("P - Paha : Rp. 2000")
        print("S - Sayap: Rp. 1500")
        print("Ketik 'selesai' untuk mengakhiri pembelian.")

        jenis = input("Masukkan kode jenis potong (D/P/S)  : ").upper()
        if jenis == 'SELESAI':
            break
        elif jenis not in harga_ayam:
            print("Kode jenis tidak valid. Silakan coba lagi.")
            continue

        jumlah = int(input(f"Masukkan banyak {jenis} yang ingin dibeli : "))
        
        # Hitung total untuk jenis yang dipilih
        total_bayar += hitung_total(jenis, jumlah)

    # Hitung pajak 10%
    pajak = total_bayar * 0.1
    total_akhir = total_bayar + pajak

    print("\nTotal Belanja:")
    print(f"Subtotal   : Rp. {total_bayar}")
    print(f"Pajak (10%): Rp. {pajak}")
    print(f"Total Akhir: Rp. {total_akhir}")

if __name__== "__main__":
    main()
