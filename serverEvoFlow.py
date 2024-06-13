import zmq
import time

def main():
    # Cria o contexto ZMQ
    context = zmq.Context()
    # Cria um socket REP (reply)
    socket = context.socket(zmq.REP)
    # Liga o socket a um arquivo IPC
    #socket.bind("ipc:///tmp/evoflow")
    socket.bind("ipc:///tmp/Z03")
    
    message = socket.recv()
    print(f"Received: {message}")
    while True:
        socket.send(b"Read")
        # Espera por uma mensagem do cliente
        message = socket.recv()
        print(f"Received: {message}")
        time.sleep(5)

        # Envia uma resposta de volta ao cliente
        

if __name__ == "__main__":
    main()