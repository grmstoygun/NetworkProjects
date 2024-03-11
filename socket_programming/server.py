import socket

# Defining server name and arbitrary port
serverName = socket.gethostbyname(socket.gethostname())
port = 12000
address = (serverName, port)

def upload_request():
    # If an upload request has been recieved from the client, the data is recieved.
    data = connectionSocket.recv(1024).decode("utf-8")

    # A new file containing the incoming data has been generated, to be stored in the host device of the server.
    with open("server_file.txt", "w+") as file:
        file.write(data)
        file.close()

def download_request():
    # If a download request has been recieved from the client, the data is retrieved from the file stored in the server host device.
    with open("server_file.txt", "r") as file:
        data = file.read()
        file.close()
        # The data is sent through the socket into the TCP connection with the client process.
        connectionSocket.send(data.encode("utf-8"))

if __name__ == "__main__":
    # When server program is executed, the server initiates a new socket for incoming connection requests.
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # The name and port number is assigned to the socket and the server is starting to listen for requests. 
    serverSocket.bind(address)
    serverSocket.listen()
    print("Server up and listening.")

    while 1:
        # When there is an incoming connection request, the connection is accepted and the information is print to the console.
        connectionSocket, addr = serverSocket.accept()
        print(f"New connection: {addr} connected.")
        # The operation name for our simple protocol has been recieved. According to the operation the corresponding function is called.
        request_action = connectionSocket.recv(1024).decode("utf-8")
        if(request_action == "UPLOAD") : upload_request()
        elif(request_action == "DOWNLOAD") : download_request()
        # The TCP connections between the server and client is closed when the request of the client is met.
        connectionSocket.close()
