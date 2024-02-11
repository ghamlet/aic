import socket

HOST = ("192.168.4.69", 8000)
print(HOST) 

eyecar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
eyecar.connect(HOST)  #connect to the server port
print("Connected to", HOST)

# msg = eyecar.recv(1024)
# print(msg.decode("UTF-8"))

eyecar.send('server,give_tasks|'.encode()) 

msg = ''
while True:
    symbol = eyecar.recv(1).decode()
    if symbol in ('|', ''): break
    msg += symbol    
print(msg)
#eyecar.send("server,reserve_task,1|".encode())#после того как нашли ближайшее задание везервируем его
msg=''
eyecar.close()
# while True:
#     symbol = eyecar.recv(1).decode()
#     if symbol in ('|', ''): break
#     msg += symbol
# print(msg)
# eyecar.send('hub,offload|'.encode())
# msg=''


# while True:
#     symbol = eyecar.recv(1).decode()
#     if symbol in ('|', ''): break
#     msg += symbol
# print(msg)
# msg=''

# eyecar.close()