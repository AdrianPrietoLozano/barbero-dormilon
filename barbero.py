import threading
import time
import random


NUM_SILLAS = 3 # sillas de espera (sin contar la del barbero)
semaforo_barbero = threading.Semaphore(0)
semaforo_sillas_ocupadas = threading.Semaphore(1)
semaforo_clientes = threading.Semaphore(0)
sillas_ocupadas = []

class Barbero(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global sillas_ocupadas

        while True:
            semaforo_clientes.acquire()
            semaforo_sillas_ocupadas.acquire()
            cliente = sillas_ocupadas.pop(0)
            print("Cliente {} pasa a la silla del barbero. SILLAS DISPONIBLES: {}"\
                .format(cliente, NUM_SILLAS - len(sillas_ocupadas)))
            semaforo_barbero.release()
            semaforo_sillas_ocupadas.release()
            self.cortar_pelo(cliente)


    def cortar_pelo(self, id_cliente):
        print("Cortando el pelo al cliente {}".format(id_cliente))
        time.sleep(random.randint(0, 4))
        print("Se terminó de cortar el pelo al cliente {}".format(id_cliente))



class Cliente(threading.Thread):

    def __init__(self, id_cliente):
        super().__init__()
        self.id_cliente = id_cliente

    def run(self):
        global sillas_ocupadas

        semaforo_sillas_ocupadas.acquire()
        if len(sillas_ocupadas) < NUM_SILLAS:
            sillas_ocupadas.append(self.id_cliente)
            self.sentar_cliente()
            semaforo_clientes.release()
            semaforo_sillas_ocupadas.release()
            semaforo_barbero.acquire()
        else:
            semaforo_sillas_ocupadas.release()
            print("Cliente {} se fue porque no habia espacio".format(self.id_cliente))
        

    def sentar_cliente(self):
        print("Cliente {} se sentó en una silla. SILLAS DISPONIBLES: {}" \
            .format(self.id_cliente, NUM_SILLAS - len(sillas_ocupadas)))
    



print("BARBERO DORMILÓN")
print("Hay {} sillas de espera más la silla del barbero".format(NUM_SILLAS))
print("-----------------------------------------------------------------\n")

lista_clientes = []

NUM_CLIENTES = 100

# crea al barbero
barbero = Barbero()

# crea los clientes
for i in range(NUM_CLIENTES):
    lista_clientes.append(Cliente(i+1))

# inicia al barbero
barbero.start()

# inicia a los clientes
for cliente in lista_clientes:
    time.sleep(random.randint(0, 2))
    cliente.start() 


for cliente in lista_clientes:
    cliente.join() 

barbero.join()