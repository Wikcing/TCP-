import socket
import random

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def send_initialization(client_socket, n_blocks):
    message = (1).to_bytes(2, byteorder='big') + n_blocks.to_bytes(4, byteorder='big')
    client_socket.send(message)
    print(f"发送初始化请求，共 {n_blocks} 块。")

def send_reverse_request(client_socket, text_block):
    length = len(text_block)
    message = (3).to_bytes(2, byteorder='big') + length.to_bytes(4, byteorder='big') + text_block.encode('ascii')
    client_socket.send(message)

def receive_reverse_answer(client_socket):
    type_data = client_socket.recv(2)
    if not type_data:
        return None
    msg_type = int.from_bytes(type_data, byteorder='big')

    if msg_type == 4:
        length_data = client_socket.recv(4)
        length = int.from_bytes(length_data, byteorder='big')
        reversed_data = client_socket.recv(length).decode('ascii')
        return reversed_data
    return None

def client_program(file_path, server_ip, server_port, min_len, max_len):
    text = read_file(file_path)
    text_length = len(text)

    if text_length < min_len:
        print("文本长度小于最小块长度。")
        return

    if min_len >= max_len:
        print("最小长度必须小于最大长度。")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    blocks = []
    while text:
        remaining_length = len(text)
        if remaining_length <= max_len:
            block_len = remaining_length  # 最后一个块的长度等于剩余文本的长度
        else:
            block_len = random.randint(min_len, max_len)
        blocks.append(text[:block_len])
        text = text[block_len:]

    send_initialization(client_socket, len(blocks))

    type_data = client_socket.recv(2)
    if int.from_bytes(type_data, byteorder='big') == 2:
        print("收到同意响应。")

        reversed_text = ""
        for i, block in enumerate(blocks):
            send_reverse_request(client_socket, block)
            reversed_block = receive_reverse_answer(client_socket)
            if reversed_block is not None:
                print(f"反转后的文本块 {i+1}: {reversed_block}")
                reversed_text += reversed_block

        with open('output.txt', 'w') as output_file:
            output_file.write(reversed_text)

    client_socket.close()

if __name__ == "__main__":
    server_ip = input("请输入服务器IP地址：")
    server_port = input("请输入服务器端口号：")
    min_len = int(input("请输入最小文本块长度（大于5）："))
    max_len = int(input("请输入最大文本块长度（小于400）："))
    client_program("tcp.txt", server_ip, int(server_port), min_len, max_len)
