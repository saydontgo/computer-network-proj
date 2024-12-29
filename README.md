计网实验大作业，实现socket套接字编程。   
使用方法(linux环境下)：   
Client：在client.py文件所在目录中输入命令python3 client.py <ip address> <port>启动。       
1.传输短文本：根据启动后的提示直接在标准输入 输入你想传给服务器端的内容即可          
2.传输文件：需要使用管道，具体用法为cat <file> | python3 client.py <ip address> <port>.          
3.退出方式：按两次回车即可          
             
Server：在server.py文件所在目录中输入命令python3 server.py <port>启动。      
1.向指定客户端传输消息：根据提示在标准输入中输入：<用户编号> <你的消息>       
(用户编号会在用户连接成功时告知服务端，所有用户编号为正整数)                
(用户编号0表示广播，向所有客户端发送消息)          
2.退出方式：Ctrl+c           
