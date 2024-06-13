import serial #Usar UART TX RX
import time
import RPi.GPIO as GPIO

import zmq #Comunicacao entre processos

import ctypes #Chamar codigo em C

def calcCRC(array_hex):
    # Carregar a biblioteca compartilhada
    lib = ctypes.CDLL('./crc.so')
    # Definir a assinatura da função em C
    lib.Calculate_CRC.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t]
    #array_hex = [0x17, 0x03, 0x08, 0x53, 0x4D, 0x46, 0x43, 0x4F, 0x20, 0x20, 0x20, 0x00, 0x00]
    array_hex.extend([0x00,0x00]) #Adiciona na lista os indices para receberem o CRC
    length = len(array_hex)
    # Converter para um array de uint8_t
    array_uint8 = (ctypes.c_uint8 * length)(*array_hex)
    # Chamar a função do código C
    lib.Calculate_CRC(array_uint8, length)
    return array_uint8

def main():
    pin = 11
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(1)
    
    ser = serial.Serial("/dev/ttyS0",baudrate=2400, timeout=0.5)
    
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("ipc:///tmp/evoflow")
    socket.send_string("SensorStart")
    
    while(1):
        msg = socket.recv_string()
        print(f"Recebido: {msg}")
        try:
            print("Start")
            hexID = 0x17
            
            #hex_data = b'\x3A\xF8\x03\x00\x86\x00\x04\xB1\x89' #Manda comando para todos os slaves
            #hex_data = b'\x17\x03\x00\x86\x00\x04\xA7\x16' #Manda comando para o slave Decimal 23 - hex17
            #hex_data = b'\x17\x03\x00\x80\x00\x04\x47\x17' #Manda comando para o slave Decimal 23 - hex17
            hex_data = calcCRC([hexID,0x03,0x00,0x80,0x00,0x04])
            ser.write(hex_data)
            ser.flush()
            ser.reset_input_buffer()
            
            receivedData = ser.read(30) #Termina com Timout pois o tamanho varia
            dataHexList = [byte for byte in receivedData] #Lista cada hexa
            #Remove 2 ultimos itens recebidos para calcular CRC e compara o dado recebico com o comparado.
            if (dataHexList[:] == calcCRC(dataHexList[:-2])[:]):
                print('Data_EvoFlow_OK')
                print(dataHexList)
                socket.send_string(f"{dataHexList}")
            else:
                print('Data_EvoFlow_CRC_FALHA!')

        except:
            print("EvoFlow_FalhaPrograma!")
        

if __name__ == "__main__":
    main()
