import zmq

def main():
    # Cria o contexto ZMQ
    context = zmq.Context()
    # Cria um socket REP (reply)
    socket = context.socket(zmq.REP)
    # Liga o socket a uma porta
    socket.bind("tcp://*:5555")

    while True:
        # Espera por uma mensagem do cliente
        message = socket.recv()
        print(f"Received request: {message}")

        # Envia uma resposta de volta ao cliente
        socket.send(b"World")

if __name__ == "__main__":
    main()