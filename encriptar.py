from PIL import Image
import random
import numpy as np
from matplotlib import cm

long_extra = 2
def logistic(r,x): return r*x*(1-x)
def r_generator(): return random.uniform(3.57, 4)


original = Image.open('campus.jpg', 'r')
width, height = original.size
# Sacamos los pixeles
im = list(original.getdata())

# Paso 1: Lo ponemos todo en un solo vector
inf_original = [item for sublist in im for item in sublist]
copy = [item for sublist in im for item in sublist]
L = len(inf_original)
LM = L*long_extra
ubicacion_inicial = int(random.uniform(1, LM))
print('Paso 1')
# Paso 2: Dividimos entre 255 para pasar a [0,1]
inf_original = [x / 255 for x in inf_original]
print('Paso 2')
# Paso 3: Generamos LM y lo rellenamos de -1
inf_cifrada = np.zeros((1,LM))[0]
inf_cifrada = [-1 for i in range(LM)]
print('Paso 3')
# Paso 4: Encontrar una orbita de longitud L
key_1 = r_generator()
x0_1  = random.uniform(0, 1)
logistic_mezcla = np.zeros((1,L))[0] # Vector de ceros
print('Paso 4')
logistic_mezcla[0] = x0_1
for i in range(L-1):
    logistic_mezcla[i+1] = logistic(key_1,logistic_mezcla[i])
print('Paso 5')
# Paso 5: Conseguir el vector posiciones
posiciones = np.zeros((1,L))[0] # Vector de ceros

for i in range(L):
    posiciones[i] = round(LM*logistic_mezcla[i])
print('Paso 6')

# Paso 6: Guardamos la ubicacion inicial en ubicacion_inicial
ubicacion = ubicacion_inicial
print('Paso 7-10')
# Pasos 7-10: Metemos inf_original en inf_cifrada desordenadamente
for i in range(0,L):
    print(f'i = {i}  L = {L}')
    ubicacion = int(ubicacion + (posiciones[i]%L))
    if(ubicacion < LM): # Paso 8
        # Buscamos un hueco vacio
        while inf_cifrada[ubicacion] != -1:
            #print('c1')
            ubicacion = ubicacion + 1
            if(ubicacion == LM): ubicacion = 0

        inf_cifrada[ubicacion] = inf_original[i]

    else: # Paso 9 ubicacion > LM
        ubicacion = int(posiciones[i]%L)

        while inf_cifrada[ubicacion] != -1:
            #print(f'c2 ubicacion = {ubicacion}')
            ubicacion = ubicacion + 1
            if(ubicacion == LM): ubicacion = 0

        inf_cifrada[ubicacion] = inf_original[i]

print('Paso 11')
# Paso 11: creacion del vector relleno

key_2 = r_generator()
x0_2  = random.uniform(0, 1)
relleno = np.zeros((1,LM-L))[0]

relleno[0] = x0_2
for i in range(LM-L-1):
    relleno[i+1] = logistic(key_2,relleno[i])

print('Paso 12')
# Paso 12: Rellenao inf_cifrada con relleno
ubicacion = 0
index = 0
for number in inf_cifrada:
    if(inf_cifrada[ubicacion] == -1):
         inf_cifrada[ubicacion] = relleno[index]
         index = index + 1
    ubicacion = ubicacion + 1
print('Paso 13')
# Paso 13: Crear vector confusion
key_3 = r_generator()
x0_3  = random.uniform(0, 1)
confusion = np.zeros((1,LM))[0]

confusion[0] = x0_3
for i in range(LM-1):
    confusion[i+1] = logistic(key_3,confusion[i])
print('Paso 14')
# Paso 14: Aplicar confusion
for i in range(LM):
    inf_cifrada[i] = inf_cifrada[i] + confusion[i]



# Guardamos el Encriptado
# Reconstruimos la imagen
factor2RGB = 255/max(inf_cifrada) # Para poder darle color

photo = []
row = []
row_counter = 0
total_pixels = int(len(inf_cifrada)/3)
for i in range(0,total_pixels):
    if (row_counter == width):
        print(row)
        photo.append(row)
        row = []
        row_counter = 0
    row.append((inf_cifrada[i*3]*factor2RGB,inf_cifrada[i*3+1]*factor2RGB,inf_cifrada[i*3+2]*factor2RGB))
    row_counter = row_counter + 1
photo.append(row)




# Convert the pixels into an array using numpy
array = np.array(photo, dtype=np.uint8)

# Use PIL to create an image from the new array of pixels
new_image = Image.fromarray(array)
new_image.save('encriptado.jpg')


print('Encriptado, Pasamos a desencriptar')
# Empezamos la desincriptacion
print('Paso 1')
# Paso 1: recrear confusion
confusion = np.zeros((1,LM))[0]

confusion[0] = x0_3
for i in range(LM-1):
    confusion[i+1] = logistic(key_3,confusion[i])

# Paso 2: restar confusion
print('Paso 2')
for i in range(LM):
    inf_cifrada[i] = inf_cifrada[i] - confusion[i]

# Paso 3: Recrear logistic_mezcla y posiciones
print('Paso 3')
logistic_mezcla = np.zeros((1,L))[0] # Vector de ceros

logistic_mezcla[0] = x0_1
for i in range(L-1):
    logistic_mezcla[i+1] = logistic(key_1,logistic_mezcla[i])

posiciones = np.zeros((1,L))[0] # Vector de ceros
for i in range(L):
    posiciones[i] = round(LM*logistic_mezcla[i])

# Paso 4: Reasignar ubicacion_inicial
print('Paso 4')
ubicacion = ubicacion_inicial

# Paso 5: Volver a crear inf_original
print('Paso 5-9')
inf_original = np.zeros((1,L))[0]
for i in range(0,L):
    print(f'i = {i}  L = {L}')
    ubicacion = int(ubicacion + (posiciones[i]%L))

    if(ubicacion < LM): # Paso 6
        # Buscamos un hueco vacio
        while inf_cifrada[ubicacion] == -1:
            ubicacion = ubicacion + 1
            if(ubicacion == LM): ubicacion = 0

        inf_original[i] = round(255*inf_cifrada[ubicacion])
        inf_cifrada[ubicacion] = -1

    else: # Paso 7 ubicacion > LM
        ubicacion = int(posiciones[i]%L)

        while inf_cifrada[ubicacion] == -1:
            ubicacion = ubicacion + 1
            if(ubicacion == LM): ubicacion = 0

        inf_original[i] = int(round(255*inf_cifrada[ubicacion]))
        inf_cifrada[ubicacion] = -1

inf_original = inf_original.astype(int)
print('Desencriptado, reconstruyendo')
# Reconstruimos la imagen
photo = []
row = []
row_counter = 0
total_pixels = int(len(inf_original)/3)
for i in range(0,total_pixels):
    if (row_counter == width):
        photo.append(row)
        row = []
        row_counter = 0
    row.append((inf_original[i*3],inf_original[i*3+1],inf_original[i*3+2]))
    row_counter = row_counter + 1
photo.append(row)
row = []


# Convert the pixels into an array using numpy
array = np.array(photo, dtype=np.uint8)

# Use PIL to create an image from the new array of pixels
new_image = Image.fromarray(array)
new_image.save('new.jpg')
