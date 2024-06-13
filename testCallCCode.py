import ctypes

# Carregar a biblioteca compartilhada
lib = ctypes.CDLL('./crc.so')

# Definir a assinatura da função em C
lib.Calculate_CRC.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t]

# Definir o array de entrada em hexadecimal
array_hex = [0x17, 0x03, 0x08, 0x53, 0x4D, 0x46, 0x43, 0x4F, 0x20, 0x20, 0x20, 0x00, 0x00]
length = len(array_hex)

# Converter para um array de uint8_t
array_uint8 = (ctypes.c_uint8 * length)(*array_hex)

# Chamar a função do código C
lib.Calculate_CRC(array_uint8, length)

# Imprimir o array com o CRC
print("Array dataBytes com CRC:")
for i in range(length):
    print("0x{:02X}".format(array_uint8[i]), end=' ')
print()
