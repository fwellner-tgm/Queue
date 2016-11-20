import threading, queue


class Producer(threading.Thread):
    """
    Diese Klasse ist ein Producer/Erzeuger,
    welcher Primzahlen sucht und diese and den
    ConsumerVerbraucher schickt.
    """

    def __init__(self, queue):
        """
        Initialisiert die Basisklasse Thread.
        :param queue: Die Queue, an welche die Zahlen geschickt werden.
        """
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        """
        Erzeugt Primzahlen und sendet sie an die Queue.
        :return: None
        """
        number = 1
        while True:
            number += 1
            if number in [2,3,5,7] or number % 2 != 0 and number % 3 != 0 and number % 5 != 0 and number % 7 != 0:
                self.queue.put(number)
            self.queue.join()


class Consumer(threading.Thread):
    """
    Diese Klasse ist ein Consumer/Verbraucher.
    """
    def __init__(self, queue):
        """
        Initialisiert die Basisklasse Thread.
        :param queue: Die geteilte Queue.
        """
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        """
        Gibt alle Zahlen aus, die aus der geteilten Queue
        empfangen werden.
        :return: None
        """
        #Liste zum speichern aller Zahlen
        num_list = []
        while True:
            number = self.queue.get()
            #Jede Zahl in der Liste hinzufügen
            num_list.append(str(number))
            #Textdatei erstellen und die Liste einfügen
            with open("output.txt", "r+") as f:
                f.write("\n".join(num_list))

            print("Empfangene Zahl: %s" % number)
            self.queue.task_done()



if __name__ == '__main__':
    queue = queue.Queue()
    t1 = Producer(queue)
    t2 = Consumer(queue)
    t1.start()
    t2.start()
    t1.join()
    t2.join()