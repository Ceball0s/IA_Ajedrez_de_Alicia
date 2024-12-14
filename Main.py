import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interfaz.server import server  # Importar servidor
#from Proyecto.pruebas import *

if __name__ == "__main__":
    if "--performance-test" in sys.argv:
        # ejecutar_tests()
        pass
    else:
        print("Iniciando el servidor minimax...")
        server()
