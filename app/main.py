# Uncomment this to pass the first stage
import socket
import threading
import os
import sys


directory_path = ""
for i, arg in enumerate(sys.argv):
    if arg == "--directory" and i + 1 < len(sys.argv):
        directory_path = sys.argv[i + 1]
        break

def handle_client(client_socket):
    try:
        request_data = client_socket.recv(1024).decode('utf-8')
        parsed_request = parse_request(request_data)

        status = "200 OK"
        headers = {
            "Content-Type": "text/plain",
            "Content-Length": "0"
        }
        body = ""

        if request_data["method"] == "POST":
            filename = parsed_request["path"].split("/files/")[1]
            content_type = parsed_request["headers"].get("Content-Type")
            content_length = int(parsed_request["headers"].get("Content-Length", 0))

            if content_type == "application/octet-stream":
                file_path = os.path.join(directory_path, filename)
                body_data = client_socket.recv(content_length)

                with open(file_path, "wb") as file:
                    file.write(body_data)

                status = "201 Created"
                headers = {
                    "Content-Type": "text/plain",
                    "Content-Length": "0"
                }
                body = ""
                response(client_socket, status, headers, body)
            else:
                status = "400 Bad Request"
                headers = {
                    "Content-Type": "text/plain",
                    "Content-Length": "0"
                }
                body = "Invalid Content-Type"
                response(client_socket, status, headers, body)


        if parsed_request['path'] == "/":
            response(client_socket, status, headers, body)
        elif "/echo/" in parsed_request["path"]:
            body = parsed_request["path"].replace("/echo/", "")
            headers["Content-Length"] = str(len(body))
            response(client_socket, status, headers, body)
        elif "/user-agent" in parsed_request["path"]:
            body = parsed_request["headers"].get("User-Agent", "")
            headers["Content-Length"] = str(len(body))
            response(client_socket, status, headers, body)
        elif "/files/" in parsed_request["path"]:
            file_path = os.path.join(directory_path, parsed_request["path"].replace("/files/", "", 1))
            try:
                with open(file_path, "rb") as f:
                    body = f.read()
                    headers["Content-Type"] = "application/octet-stream"
                    headers["Content-Length"] = str(len(body))
                    response(client_socket, status, headers, body)
            except FileNotFoundError:
                status = "404 Not Found"
                response(client_socket, status, headers, body)
        else:
            status = "404 Not Found"
            response(client_socket, status, headers, body)
    finally:
        client_socket.close()

def parse_request(request_data):
    lines = request_data.split('\r\n')
    request_line = lines[0].split(' ')
    method, path, version = request_line

    headers = {}
    body = None
    for line in lines[1:]:
        if line == '':
            body_index = lines.index(line) + 1
            body = '\r\n'.join(lines[body_index:])
            break
        header_key, header_value = line.split(': ', 1)
        headers[header_key] = header_value

    return {
        "method": method,
        "path": path,
        "version": version,
        "headers": headers,
        "body": body
    }

def response(client_socket, status, headers, body):
    response_line = f"HTTP/1.1 {status}\r\n"
    headers_str = ''.join(f'{key}: {value}\r\n' for key, value in headers.items())
    # Prepare the headers and the separator as bytes
    headers_bytes = (response_line + headers_str + '\r\n').encode('utf-8')
    # Ensure the body is in bytes. If it's already bytes, this has no effect.
    if isinstance(body, str):
        body = body.encode('utf-8')
    # Concatenate headers and body as bytes and send
    client_socket.sendall(headers_bytes + body)

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    # server_socket.accept() # wait for client
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


if __name__ == "__main__":
    main()
