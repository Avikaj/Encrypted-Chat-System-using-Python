import socket
import threading
import rsa


public_key, private_key = rsa.newkeys(1024)
public_partner = None
choice = input('(1) If you want to be the host, (2)If you want to connect with the host')

# The host
if choice == '1':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("ip_address", 9999))
    server.listen()
    client, _ = server.accept()
    client.send(public_key.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))

# The other side
elif choice == '2':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("ip_address", 9999))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1("PEM"))
else:
    exit()


def sending_messages(c):
    while True:
        message = input("")
        c.send(rsa.encrypt(message.encode(), public_partner))  # encrypting the message
        print("You: " + message)


def receiving_messages(c):
    while True:
        print("Partner:" + rsa.decrypt(c.recv(1024), private_key).decode())  # decrypting the message


threading.Thread(target=sending_messages, args=(client,)).start()
threading.Thread(target=receiving_messages, args=(client,)).start()
