import zmq
import time

def main():
    # Cria o contexto ZMQ
    context = zmq.Context()
    # Cria um socket REQ (request)
    socket = context.socket(zmq.REQ)
    # Conecta ao servidor
    socket.connect("tcp://localhost:5555")

    for request in range(100):
        # Envia uma mensagem ao servidor
        print(f"Sending request {request}...")
        socket.send(b"Hello")

        # Espera por uma resposta do servidor
        message = socket.recv()
        print(f"Received reply {request} [ {message} ]")

        # Espera um pouco antes de enviar a próxima mensagem
        time.sleep(1)

if __name__ == "__main__":
    main()

