#####################################################
#####################################################
import time
import os
import pymysql
import socket
from multiprocessing import Process, Queue
from threading import Thread

## Cloud Server connect

def connect_server(q):
    HOST = "192.168.0.55"
    PORT = 9856
                    #소켓 객체를 생성 #IP4v에 사용되는 소캣 패밀리 #소켓 타입
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #(family=,type=)
    client_socket.connect((HOST, PORT)) #소켓 연결

    while True:
        # client_socket.send("hello3".encode())
        # print("hello4")s

        if q.empty():       #multi thread 를 사용 하여 q에 데이터를   받을 때까지 무한루프
            continue

        data = q.get()      #만약 q에 데이터가 있다면 q의 데이터를 get하여 data에 넣는다.
        client_socket.send(data.encode())





    client_socket.close()

## DB input data form

def database_format(recv_data):
    arr = recv_data.split()

    return (int(arr[0]), int(arr[1]))

## socket handler

def handle_client(client_socket, addr, q, file_cnt):  #A->GATE
    print("Client address : ", addr)

    # 디렉토리 만들기
    dirname = os.getcwd() + '\Read_value'

    if not os.path.exists(dirname):
        os.mkdir(dirname)

    # MySQL Connection 연결
    conn = pymysql.connect(host='192.168.0.63', user='root', password='1',
                           db='test2', charset='utf8')

    while True:
        recv_data = client_socket.recv(8).decode()
        print("Receive data : ", recv_data)

        #파일에 데이터 저장
        name = str(os.getcwd()) + '\Read_value\data' + str(file_cnt)+ '.txt'
        if not os.path.exists(name):
            f = open(name, 'w')  # 파일의 생성
            f.close()
        f=open(name, 'a')
        f.write(recv_data+"\n")    # send to server

        # Connection 으로부터 Cursor 생성
        curs = conn.cursor()

        sql = """insert into gateway_output_data(num, value)
                 values (%s, %s)"""

        curs.execute(sql, database_format(recv_data))

        conn.commit()


        q.put(recv_data)
        # print("jellow")
        # q.put("hello1")

        #time.sleep(1)
    # file sys out
    f.close()

    # DB sys out
    conn.close()

    # connetion out
    client_socket.close()

## Senser device Server

def create_gateway(q, file_cnt):  #아두이노와 연결
    HOST = ""
    PORT = 8866

    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    #     server_socket.bind((HOST, PORT))  # 주소 바인딩
    #     server_socket.listen()  # 클라이언트의 요청을 받을 준비
    #
    #     client_socket, client_addr = server_socket.accept()  # 수신대기, 접속한 클라이언트 정보 (소켓, 주소) 반환
    #
    #     # 무한루프 진입
    #     while True:
    #         msg = client_socket.recv(1024)  # 클라이언트가 보낸 메시지 반환
    #         print("[{}] message : {}".format(client_addr, msg))  # 클라이언트가 보낸 메시지 출력
    #
    #         client_socket.sendall("welcome!".encode())  # 클라이언트에게 응답
    #
    #     client_socket.close()  # 클라이언트 소켓 종료

    gateway_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    gateway_socket.bind((HOST, PORT))
    gateway_socket.listen()

    print(" waiting... ")

    while True:
        try:
            client_socket, addr = gateway_socket.accept()

            print("Accept")
        except:
            gateway_socket.close()

        file_cnt+=1

        client_thread = Thread(target=handle_client, args=(client_socket, addr, q, file_cnt))
        client_thread.daemon = True
        client_thread.start()

# main function

if __name__ == "__main__":

    q = Queue()

    process_list = []

    file_cnt = 1

    # Create multi processing
    process_connect_server = Process(target=connect_server, args=(q,))
    process_create_gateway = Process(target=create_gateway, args=(q, file_cnt))

    process_list.append(process_connect_server)
    process_list.append(process_create_gateway)

    process_connect_server.start()
    process_create_gateway.start()

    while True:
        pass