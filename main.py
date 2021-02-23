from sys import exit,argv
from memory_manager import MemoryManager

def main(num):

    print("*"*30)
    print("""Welcome to this memory manager simulator :D Happy coding\n""")
    my_manager=MemoryManager(num)
    while True:
        my_input=input(">> ")
        my_input=my_input.upper()
        elems=my_input.split(" ")
        command=elems[0]
        if command=="SALIR":
            exit(0)
        elif command=="RESERVAR" and len(elems)>2:
            my_manager.reserve(str(elems[1]),int(elems[2]))

        elif command=="LIBERAR" and len(elems)>1:
            my_manager.remove(str(elems[1]))

        elif command=="MOSTRAR":
            print(my_manager)
        else:
            print_help()

def print_help():
    """ Print help for user """

    response="""RESERVAR <nombre> <cantidad>
        Representa una reserva de espacio de <cantidad> bloques,
        asociados al identificador <nombre>.

        LIBERAR <nombre>
        Representa una liberación del espacio que contiene el
        identificador <nombre>.
        
        MOSTRAR
        Debe mostrar una representación gráfica (en texto) de las
        listas de bloques libres, así como la información de nombres
        y la memoria que tienen asociada a los mismos.
        
        SALIR
        Debe salir del simulador.\n"""

    print(response)


if __name__ == "__main__":
    try:
        my_space=int(argv[1])
    except:
        my_space=input("¿Cuánta memoria desea?: ")
        my_space=int(my_space)
    
    main(my_space)