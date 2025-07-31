#Tunjangan Jabatan
gaji_pokok = 300000 
golongan_1 = 0.05
golongan_2 = 0.1
golongan_3 = 0.15
#Tunjangan Pendidikan
pdk_SMA = 0.025
pdk_D1 = 0.05
pdk_D3 = 0.2
pdk_S1 = 0.3
#Jam Kerja
jam_normal = 8
#hitung tunjangan jabatan
per_jam_lebih = 3500
nama_karyawan = input("Nama Karyawan    : ")
golongan = input("Golongan [1/2/3] : ")
if golongan == "1" :
  tunjangan_jbtn = golongan_1 * gaji_pokok
elif golongan == "2" :
    tunjangan_jbtn = golongan_2 * gaji_pokok
else :
    tunjangan_jbtn = golongan_3 * gaji_pokok
#hitung tunjangan pendidikan
pendidikan = input("Masukan Pendidikan Anda [SMA/D1/D3/S1] : ")
if pendidikan == "SMA" or pendidikan == "sma" :
    tunjangan_pdk = gaji_pokok * pdk_SMA
elif pendidikan == "D1" or pendidikan == "d1" :
    tunjangan_pdk = gaji_pokok * pdk_D1
elif pendidikan == "D3" or pendidikan == "d3" :
    tunjangan_pdk = gaji_pokok * pdk_D3 
elif pendidikan == "S1" or pendidikan == "s1" :
    tunjangan_pdk = gaji_pokok * pdk_S1
else :
    tunjangan_pdk = 0    
#hitung jam kerja
jam_lembur = int(input("Jam Lembur       : "))
if jam_lembur > jam_normal :
  honor_lembur = (jam_lembur - jam_normal) * per_jam_lebih
else :
   honor_lembur = 0
   
total_gaji = int(gaji_pokok + tunjangan_jbtn + tunjangan_pdk + honor_lembur) * 30   
total_jam_kerja = jam_normal + jam_lembur   
print(f'''Total Gaji       : {total_gaji}
Total Jam Kerja  : {total_jam_kerja}''') 
#Surat Gaji
print(f"Karyawan yang bernama : {nama_karyawan}")
print(f"Tunjangan Jabatan     : Rp.{tunjangan_jbtn}")
print(f"Tunjangan Pendidikan  : Rp.{tunjangan_pdk}")
print(f"Honor Lembur          : Rp.{honor_lembur}")
    



