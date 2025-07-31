#hexadecimal
data = {1:'dada ayam',"pala": 'ayam',
        2:'sayap ayam',
        3:'paha ayam'}
print(data)
angka = 15//2 #pembagian bulat
print(angka)
a = False
b = True
c = not a
print(f'a not false = {c}')
uang = 500 
uang += 20
print(uang)
huruf = ('abcdefghij')
kata = len(huruf)
print(kata)
print(huruf.index('j'))#mengetahui index ke berapa harus menggukan fungsi index dan harus pakai huruf
print(huruf.index('a'))
print(huruf[9])#mengetahui daftar index tanpa perlu pakai fungsi index harus menggunakan angka
brt = 5
hrg = 26000
ongkos = 3500
uang = 200000
hrg_tlr = (hrg * brt)
total_ongkos = (ongkos * 2)
sisa = (uang - hrg_tlr - total_ongkos)
print(f'Harga telor : Rp.{hrg_tlr}')
print(f'Ongkos : Rp.{total_ongkos}')
print(f"Sisa uang Ibu : Rp.{sisa}") 
loop = int(input('masukan data : '))
for i in range(loop) :
        print(f'nilai : {i}')
count = int(input('Masukan angka : '))
while count < 15 :
        print(count)
        count = count + 3        
apa = int(input("masukan angka lagi : "))
while apa > 0 :
        print(f'angka sekarang : {apa}')
        apa = apa - 2
bilangan = int(input('masukan bilangan : '))
for i in range(2,bilangan):
  if (bilangan % i) == 0:
    print(bilangan, "bukan bilangan prima")
    print(i, "kali", bilangan//i, "=", bilangan)
    break                
k = 14%5
print(k)
n = int(input('masukan nilai : '))
i = 1
while n >= i :
        print("  ")
        j = 7
        while j >= n :
         print('*',end=" ")
         j -= 1
        print("  ")
        n-=1   
print()        