# actividad3a-redes
Se requiere el paquete de python paramiko. 

Primero se corre ssh_server con los parametros localhost 22

Luego se corre ssh_client con los parametros localhost -u horst -p 22 -a redes4340 -c pwd

De ser erronea la contraseña o el nombre de usuario (de momento solo se acepta horst con contraseña redes4340) esta será añadida a failed_attempts.txt, que poseerá mayor detalle
