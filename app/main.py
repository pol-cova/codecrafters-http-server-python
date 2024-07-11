# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    # server_socket.accept() # wait for client
    client_socket, addr = server_socket.accept()  # Unpack the tuple
    request_data = client_socket.recv(1024).decode('utf-8')

    lines = request_data.split("\r\n")
    request_line = lines[0].split(" ")
    method = request_line[0]
    path = request_line[1]
    version = request_line[2]

    status_ok = "HTTP/1.1 200 OK\r\n\r\n"
    status_not_found = "HTTP/1.1 404 Not Found\r\n\r\n"
    if method == "GET":
        if path == "/":
            client_socket.sendall(status_ok.encode('utf-8'))
        else:
            client_socket.sendall(status_not_found.encode('utf-8'))




if __name__ == "__main__":
    main()
