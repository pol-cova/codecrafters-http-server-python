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

    lines = request_data.split('\r\n')
    request_line = lines[0].split(' ')
    method = request_line[0]
    path = request_line[1]
    version = request_line[2]

    headers = {}
    body = None

    for line in lines[1:]:
        if line == '':
            body_index = lines.index(line) + 1
            body = '\r\n'.join(lines[body_index:])
            break
        header = line.split(': ')
        headers[header[0]] = header[1]

    status_ok = "HTTP/1.1 200 OK\r\n"
    status_not_found = "HTTP/1.1 404 Not Found\r\n\r\n"

    req_param = path.split("/echo/")[1]

    # response
    response_line = status_ok
    headers = {
        "Content-Type": "text/plain",
        "Content-Length": len(req_param)
    }

    response_body = req_param

    # Construct headers string
    headers_str = ''.join(f'{key}: {value}\r\n' for key, value in headers.items())

    # Construct final response
    response = response_line + headers_str + '\r\n' + response_body

    client_socket.sendall(response.encode('utf-8'))





if __name__ == "__main__":
    main()
