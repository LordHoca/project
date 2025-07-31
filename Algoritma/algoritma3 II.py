def hitung_kelereng(milik_aldi):
  
    kelereng_budi = milik_aldi - 15
    kelereng_anto = 2 * (milik_aldi + kelereng_budi)
    kelereng_agung = (milik_aldi + kelereng_budi + kelereng_anto) - 5
    
    return kelereng_budi,kelereng_anto,kelereng_agung

kelereng_aldi = int(input("Masukkan jumlah kelereng Aldi: "))
budi, anto, agung,  = hitung_kelereng(kelereng_aldi)

print(f"Jumlah kelereng Budi : {budi}")
print(f"Jumlah kelereng Anto : {anto}")
print(f"Jumlah kelereng Agung: {agung}")

