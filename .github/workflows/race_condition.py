import threading

available_setes = 2


class Movie:
    def __init__(self):
        self.lock = threading.RLock()

    def booking(self, number_of_seats):
        global available_setes

        with self.lock:
            try:
                if number_of_seats <= available_setes:
                    print(f"{number_of_seats} reserved seat for {threading.current_thread().name}")
                    available_setes -= number_of_seats
                elif number_of_seats > available_setes:
                    print(f'{threading.current_thread().name}seat not')
                else:
                    print("all seat")
            except Exception as e:
                print(e)
        # self.lock.acquire()
        # try:
        #     if number_of_seats <= available_setes:
        #         print(f"{number_of_seats} reserved seat for {threading.current_thread().name}")
        #         available_setes -= number_of_seats
        #     elif number_of_seats > available_setes:
        #         print(f'{threading.current_thread().name}seat not')
        #     else:
        #         print("all seat")
        # except Exception as e:
        #     print(e)
        # finally:
        #     self.lock.release()


movie = Movie()
threads = [
    threading.Thread(target=movie.booking, args=(2,), name="mom"),
    threading.Thread(target=movie.booking, args=(2,), name="ali"),
]
[t.start() for t in threads]
[t.join() for t in threads]
