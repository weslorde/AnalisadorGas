import serial
import struct
import time

def inv_bits(numero):
    # Inverter cada bit
    binario = bin(numero)[2:]  # Converte para binário, ignorando os dois primeiros caracteres ('0b')
    invertido = ''.join('1' if bit == '0' else '0' for bit in binario)
    # Somar 1 ao número invertido
    decimal = int(invertido, 2) + 1
    # Converte para hexadecimal
    hexa_final = hex(decimal)
    return hexa_final

def check_sum(data):
    # Ignora o primeiro byte
    data_to_sum = data[1:-1]
    
    # Inicializa o contador de bits
    checkSum = 0

    # Percorre cada byte
    for byte in data_to_sum:
        checkSum += byte
    
    teste = inv_bits(checkSum)
    return teste


# Configuração da porta serial
ser = serial.Serial(
    port='/dev/ttyS0',  # Porta serial no Raspberry Pi 3 B+
    baudrate=9600,      # Taxa de transmissão (baud rate)
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1           # Tempo limite de leitura em segundos
)

# Verifica se a porta serial está aberta
if ser.isOpen():
    print("Porta serial aberta com sucesso!")
else:
    print("Falha ao abrir a porta serial.")

try:
    # Enviar dados em hexadecimal
    #hex_data = b'\xFF\x01\x78\x03\x00\x00\x00\x00\x84'  # Comando to switch to Active upload mode
    #hex_data = b'\xFF\x01\x78\x04\x00\x00\x00\x00\x83'  # Comando to switch to Q&A mode
    #ser.write(hex_data)

    # Receber e imprimir dados em hexadecimal
    while(1):
        time.sleep(2)
        hex_data = b'\xFF\x01\x86\x00\x00\x00\x00\x00\x79'  # Comando to switch to Active upload mode
        ser.write(hex_data)
        
        receivedData = ser.read(9)  # Lê 4 bytes
        checkSum = check_sum(receivedData)
        print(receivedData, "   ", checkSum)
        print(int(receivedData[2]))
        print(int(receivedData[3]))
        print(int(receivedData[5]))
        val02 = (int(receivedData[2])*256+int(receivedData[3]))*0.1*10**(-int(receivedData[5]))
        print("Val de 02: ", val02, "%VOL")
        hexStr = receivedData.hex()  # Converte para string hexadecimal

except KeyboardInterrupt:
    print("Programa interrompido pelo usuário.")
    ser.close()  # Fecha a porta serial quando o programa é encerrado
