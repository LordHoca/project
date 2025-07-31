harga_ayam = {
    'D' : 2500,
    'P' : 2000,
    'S' : 1500
}
pajak = 0.1
def hitung_harga (jenis, jumlah_beli):
    return harga_ayam[jenis] * jumlah_beli
def main () :
  harga = 0
  while True : 
      print('''\nHarga ayam :
"D" - Dada  : RP.2500
"P" - Paha  : Rp.2000
"S" - Sayap : Rp.1500''')
      print("ketik 'selesai' untuk selesai \n")
      jenis = input('masukan jenis ayam (D/P/S) : ').upper()
      if jenis == 'SELESAI':
          break
      elif jenis not in harga_ayam :
          print("kode invalid coba lagi")
          continue
      jumlah_beli = int(input('masukan jumlah  : '))
      harga += hitung_harga(jenis, jumlah_beli)
  print(f"\nHarga sebelum pajak : Rp.{harga}")
  biaya_pajak = harga * pajak
  total_harga = harga + biaya_pajak
  print(f'Biaya pajak         : Rp.{biaya_pajak}')
  print(f"Total Harga         : Rp.{total_harga}")
main()
    