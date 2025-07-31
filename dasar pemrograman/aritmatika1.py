jarak_gardu = 15
jarak_desa = 1500
harga_gardu = 3500000
bayar_tukang = 100000*3
harga_trafo =  15500000
biaya_tekinisi = 500000
total_gardu = int(jarak_desa/jarak_gardu)
harga_semua_gardu = int(harga_gardu*total_gardu)
masang_trafo = 1
#perhitungan biaya keseluruhan
hari_pemasangan = total_gardu + masang_trafo
biaya_pasang_trafo = harga_trafo + biaya_tekinisi
biaya_tukang = bayar_tukang*100
print(f"Biaya pasang trafo      : {biaya_pasang_trafo}")
print(f"Biaya bayar tukang      : {biaya_tukang}")
print(f"Estimasi waktu jadi     : {hari_pemasangan} hari ")
print(f"Total keseluruhan biaya : {harga_semua_gardu + biaya_pasang_trafo + biaya_tukang}")
