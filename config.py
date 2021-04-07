import socket
import os

# constantes importantes
IP = socket.gethostbyname(socket.gethostname())
PORT = "5000"

PATH = os.getcwd()

DATABASE = PATH + "/database.db"

NAME = "PaperLand"