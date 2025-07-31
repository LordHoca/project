def hitung_gaji (produk_terjual, harga_satuan):
    gaji_pokok = 5000000
    omset_jual = produk_terjual * harga_satuan
    
    if produk_terjual>100:
        bonus = 0.2 * omset_jual
    else:
        bonus = 0.1 * omset_jual
        
    gaji_total = gaji_pokok + bonus
    return omset_jual, gaji_total
produk_terjual = float(input("Produk Terjual = "))
harga_satuan = int(input("Harga satuan = "))
gaji_total, bonus = hitung_gaji(produk_terjual, harga_satuan)
print(f"Gaji Salesman = {gaji_total + bonus}")
