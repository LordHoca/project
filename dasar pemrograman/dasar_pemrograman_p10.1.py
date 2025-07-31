import calendar

def tampilkan_kalender(bulan, tahun):
    print(calendar.month(tahun, bulan))

def main():
    try:
        bulan = int(input("Masukkan bulan (1-12): "))
        tahun = int(input("Masukkan tahun: "))
        
        if bulan < 1 or bulan > 12:
            print("Bulan harus antara 1 dan 12.")
        else:
            tampilkan_kalender(bulan, tahun)
    except ValueError:
        print("Input tidak valid. Harap masukkan angka yang benar.")

if __name__ == "__main__":
    main()