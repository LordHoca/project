data = range(0,11,3)
data_list = list(data)
print(data_list)
list = [i for i in range(11) if i%2 == 0 ]
print(list)
baris = 7
kolom = 5
array = []
for i in range(baris) :
    array.append([])
    for j in range(kolom) :
        array[i].append(j)
array        
print(array)