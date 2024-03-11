import socket

# Defining server name and arbitrary port
serverName = socket.gethostbyname(socket.gethostname())
port = 12000
address = (serverName, port)

def upload_file(filename):
    # For the upload operation, create a socket and establish a new TCP connection to the target address and port number.
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(address)

    # A simple protocol for communicating with the server process.
    # 'UPLOAD' for upload operation.
    clientSocket.send("UPLOAD".encode("utf-8"))

    # Read the file to be uploaded and transmit the data in the file.
    with open(filename, "r") as file:
        data = file.read()
        clientSocket.send(data.encode("utf-8"))
        file.close()

    # Close the connection when uploading operation is done.
    clientSocket.close()


def download_file():
    # For the download operation, create a socket and establish a new TCP connection to the target address and port number.
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(address)

    # A simple protocol for communicating with the server process.
    # 'DOWNLOAD' for download operation.
    clientSocket.send("DOWNLOAD".encode("utf-8"))

    # Recieve the data in the requested file from the server.
    data = clientSocket.recv(1024).decode("utf-8")

    # Save the data in a new text file and complete download operation.
    with open("downloaded.txt", "w") as file:
        file.write(data)
        file.close()
    
    # Close the connection when downloading operation is done.
    clientSocket.close()

if __name__ == "__main__":

    # When client program starts executing, it first sends an upload request, followed by a download request.
    upload_file("upload.txt")
    download_file()

    # The uploaded file and downloaded file are compared and a report is generated based on the comparement of these two files.
    with open("upload.txt", "r") as uploaded_file, open("downloaded.txt", "r") as downloaded_file:
        if(uploaded_file.read() == downloaded_file.read()):
            with open("report.txt", "w+") as report:
                report.write("The message was successfully transmitted.")
                report.close()
        else:
            with open("report.txt", "w+") as report:
                report.write("The message was not successfully transmitted.")
                report.close()
        uploaded_file.close()
        downloaded_file.close()
