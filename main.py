import os

import socket

# 통신 정보 설정
IP = ''             # "--" 입력시 해당 ip만 통신 가능
PORT = 9855       # client와 통신 포트
SIZE = 1024         # 버퍼의 크기
ADDR = (IP, PORT)   # 튜플로 묶기

#file_cnt = 0

# 서버 소켓 설정
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(ADDR)  # 주소 바인딩
    server_socket.listen()  # 클라이언트의 요청을 받을 준비

    client_socket, client_addr = server_socket.accept()  # 수신대기, 접속한 클라이언트 정보 (소켓, 주소) 반환

    file_cnt = 1     # 각 라즈베리에 따라서 파일을 구분

    dirname = os.getcwd() + '\Read_value'

    if not os.path.exists(dirname):
        os.mkdir(dirname)

    # 무한루프 진입
    while True:

        msg = client_socket.recv(SIZE)  # 클라이언트가 보낸 메시지 반환
        print("[{}] message : {}".format(client_addr, msg))  # 클라이언트가 보낸 메시지 출력

        # 파일에 데이터 저장

        name = str(os.getcwd()) + '\Read_value\data' + str(file_cnt) +'.txt'
        if not os.path.exists(name):
            f = open(name, 'w')  # 파일의 생성
            f.close()
        f = open(name, 'a')
        f.write(msg.decode())    # python에서 유니코드를 다룰때(unicond <--> str 상호 변환)

        client_socket.sendall("welcome!".encode())  # 클라이언트에게 응답

    server_socket.close()  # 클라이언트 소켓 종료
