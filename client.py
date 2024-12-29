import socket
import sys
import threading

def get_server_message(client_socket):
    while True:
        print('现在可以从服务器接收消息，您也可以向服务端发送消息，再次回车以退出')
    # 接收来自服务器的消息
        data = client_socket.recv(1024).decode("utf-8")  # 接收数据并解码
        print(f"从服务器端接收到消息: {data}")

        # 回复服务器
        response = "成功收到!"
        client_socket.sendall(response.encode("utf-8"))


def read_binary_in_chunks(chunk_size=1024):
    while True:
        chunk = sys.stdin.buffer.read(chunk_size)
        if not chunk:
            break
        yield chunk

def start_client(host, port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
    except Exception as e:
        print(f"无法连接至 {host}:{port}: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        if not sys.stdin.isatty():#如果是管道传入
            # 缓冲区处理
            for chunk in read_binary_in_chunks():
                client_socket.sendall(chunk)
        else:
            try:
                threading.Thread(target=get_server_message, args=(client_socket,), daemon=True).start()
            except:
                print('收听服务器的线程创建失败！')
            while True:
                line = input()
                if line=='':
                    break
                client_socket.sendall(line.encode("utf-8"))
                print('成功发送!')

    except Exception as e:
        print(f"通讯中错误: {e}", file=sys.stderr)
    finally:
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("输入不合法，应为python client.py <host> <port>", file=sys.stderr)
        sys.exit(1)

    host = sys.argv[1]
    try:
        port = int(sys.argv[2])
        if port<=0:
            print("端口数字不合法", file=sys.stderr)
            sys.exit(1)
    except ValueError:
        print("端口数字不合法", file=sys.stderr)
        sys.exit(1)

    start_client(host, port)
