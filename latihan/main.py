print('''
      
      
                     ***Welcome To My Python Project***''')

print ('''      
      ===================
      Nama : Fauzan Fadhilah
      kelas : 15.1A.01
      Jurusan : Informatika
      ===================''')
import random
posisi_ucun = random.randint(1, 4)
print('''tebaklah dimana ucun berada! 
      
      ''')
pilihan_user = int(input("dimana kah ucun berada? [1 / 2 / 3 / 4] : "))
if pilihan_user == posisi_ucun :
      print(f"Jawaban Anda benar sekali ! ucun ada di {posisi_ucun} ")
else:
      print(f"Maaf jawaban Anda salah ! ucun ada di {posisi_ucun} ")






