def jumlah_siswa_hafidz(siswa_baru):
    kelas_12 = siswa_baru + 12
    kelas_11 = siswa_baru - 21
    total_seluruh_siswa = kelas_12 + kelas_11 + siswa_baru
    return kelas_12, kelas_11,total_seluruh_siswa

siswa_baru = int(input("jumlah siswa baru    : "))
siswa_12,siswa_11,total_seluruh_siswa = jumlah_siswa_hafidz(siswa_baru)
print(f"jumlah kelas 11     : {siswa_11} siswa yang sudah hafidz")
print(f"jumlah kelas 12     : {siswa_12} siswa yang sudah hafidz")
print(f"total seluruh siswa : {total_seluruh_siswa}")
