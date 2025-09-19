import socket
import threading


def receive_messages(server_socket):
    """接收服务器发送的消息并显示"""
    while True:
        try:
            message = server_socket.recv(1024).decode('utf-8')
            if not message:
                print("连接已关闭")
                break
            print(f"服务器: {message}")
        except:
            print("接收消息时发生错误")
            break


def send_messages(server_socket):
    """向服务器发送消息"""
    while True:
        message = input("我: ")
        try:
            server_socket.send(message.encode('utf-8'))
            if message.lower() == 'exit':
                print("关闭连接")
                server_socket.close()
                break
        except:
            print("发送消息时发生错误")
            break


def main():
    # 创建TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 服务器的IP地址和端口，请替换为实际服务器的IP
    server_host = '127.0.0.1'  # 这里替换为服务器的实际IP地址
    server_port = 12345

    try:
        # 连接到服务器
        client_socket.connect((server_host, server_port))
        print(f"已连接到服务器 {server_host}:{server_port}")

        # 创建并启动接收消息的线程
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        # 发送消息
        send_messages(client_socket)

    except Exception as e:
        print(f"连接服务器失败: {e}")


if __name__ == "__main__":
    main()
