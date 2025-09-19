import socket
import threading


def receive_messages(client_socket):
    """接收客户端发送的消息并显示"""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print("连接已关闭")
                break
            print(f"客户端: {message}")
        except:
            print("接收消息时发生错误")
            break


def send_messages(client_socket):
    """向客户端发送消息"""
    while True:
        message = input("我: ")
        try:
            client_socket.send(message.encode('utf-8'))
            if message.lower() == 'exit':
                print("关闭连接")
                client_socket.close()
                break
        except:
            print("发送消息时发生错误")
            break


def main():
    # 创建TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 绑定IP和端口，0.0.0.0表示监听所有网络接口
    host = '0.0.0.0'
    port = 12345
    server_socket.bind((host, port))

    # 开始监听，最多允许1个连接
    server_socket.listen(1)
    print(f"服务器已启动，正在 {host}:{port} 等待连接...")

    # 接受客户端连接
    client_socket, client_address = server_socket.accept()
    print(f"已连接到 {client_address}")

    # 创建并启动接收消息的线程
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # 发送消息
    send_messages(client_socket)

    # 关闭服务器socket
    server_socket.close()


if __name__ == "__main__":
    main()
