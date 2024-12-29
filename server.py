import socket
import threading
import sys
client_nums=1
client_max_num=100
clients={}
lock=threading.Lock()

def message_parser(message:str):
    flag=False
    client_num=''
    text=''
    for c in message:
        if c==' ':
            flag=True
        if flag:
            text+=c
        else:
            client_num+=c
    return (client_num,text)

def get_client_socket(client_num):
    if client_num in clients:
        return clients[client_num]
    return None

def send_all(message:str):
    if len(clients)==0:
        print('无用户连接，故无法发送')
        return
    print('正在向所有客户端发送信息...')
    for client_num in clients:
        clients[client_num].send(message.encode("utf-8"))  # 发送字节数据

def from_server():
    while True:
        try:
            # 发送消息到客户端
            print('现在可以向控制台输入任何内容发送至相应客户端:<用户编号（0表示所有用户）> <your_message>')
            message = input()
            client_num,response=message_parser(message)
            if response=='':
                print('不能发送空消息!')
                continue
            if client_num=='0':
                send_all(response)
                continue
            client_socket=get_client_socket(client_num)
            if client_socket==None:
                print('该编号无效!')
                continue
            client_socket.send(response.encode("utf-8"))  # 发送字节数据
        except:
            pass

def is_text(data):
    try:
        # 尝试解码为 UTF-8，若成功则认为是文本
        data.decode('utf-8')
        return True
    except UnicodeDecodeError:
        # 解码失败则认为是二进制数据
        return False
    
def handle_client(client_socket, client_address):
    print('成功连接到一个用户！')
    lock.acquire()
    global clients
    global client_nums
    this_clientnum=client_nums
    clients[str(this_clientnum)]=client_socket
    client_nums+=1
    lock.release()
    print(f'该用户编号为{this_clientnum},用户地址为{client_address}')
    try:
        with client_socket:
            while True:
                data = client_socket.recv(1024)
                message=data.decode('utf-8')
                if message =='':
                    break
                print(f'来自{this_clientnum}号用户的消息:\t {message}',flush=True)


    except:
        pass
    del clients[str(this_clientnum)]
    print(f'{this_clientnum}号用户退出')

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind(('', port))
        server_socket.listen(client_max_num)
        print(f"正在监听端口 {port}", flush=True)
    except Exception as e:
        print(f"无法绑定端口 {port}: {e}", file=sys.stderr)
        sys.exit(1)
    #创建循环读取用户输入的线程，向客户发送消息
    threading.Thread(target=from_server,daemon=True).start()
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
    except KeyboardInterrupt:
        print("服务器已退出", flush=True)
    finally:
        server_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("输入不合法，应为python3 server.py <port>", file=sys.stderr)
        sys.exit(1)

    try:
        port = int(sys.argv[1])
    except ValueError:
        print("端口数字不合法", file=sys.stderr)
        sys.exit(1)

    start_server(port)
