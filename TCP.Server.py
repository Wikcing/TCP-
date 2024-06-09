import socket

def reverse_text(text):
    return text[::-1]

def handle_client_connection(client_socket):
    while True:
        type_data = client_socket.recv(2)
        if not type_data:
            break
        msg_type = int.from_bytes(type_data, byteorder='big')

        if msg_type == 1:
            n_data = client_socket.recv(4)
            n = int.from_bytes(n_data, byteorder='big')
            print(f"接收到 {n} 块需要反转的请求。")

            client_socket.send((2).to_bytes(2, byteorder='big'))
            print("已发送同意响应。")
        elif msg_type == 3:
            length_data = client_socket.recv(4)
            length = int.from_bytes(length_data, byteorder='big')
            data = client_socket.recv(length).decode('ascii')

            reversed_data = reverse_text(data)
            response = (4).to_bytes(2, byteorder='big') + len(reversed_data).to_bytes(4, byteorder='big') + reversed_data.encode('ascii')
            client_socket.send(response)
            print(f"反转后的文本: {reversed_data}")

    client_socket.close()


def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"服务器正在 {host}:{port} 监听")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"接受到来自 {addr} 的连接")
        handle_client_connection(client_socket)


if __name__ == "__main__":
    start_server("127.0.0.1", 8888)
