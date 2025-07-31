def biaya_sewa_warnet(lama_pemakaian):
     tiga_jam_pertama = 6000
     jam_berikutnya = 5000
     batas_jam = 3
     if lama_pemakaian <= batas_jam :
          biaya = lama_pemakaian * tiga_jam_pertama
     else:
          biaya = (batas_jam * tiga_jam_pertama) + (lama_pemakaian - batas_jam) * jam_berikutnya
          return biaya
lama_pemakaian = int(input("Durasi Sewa = "))
biaya = biaya_sewa_warnet(lama_pemakaian)
print(f"Total Biaya sewa {lama_pemakaian} jam , adalah Rp.{biaya}")