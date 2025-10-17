import threading
import time
import threading


def main():
    threads = [
        threading.Thread(target=greeter, args=("mohammad",), daemon=True),
        threading.Thread(target=greeter, args=("mohammad",), daemon=True),
        threading.Thread(target=greeter, args=("mohammad",), daemon=True),
    ]
    [t.start() for t in threads]
    print("another job")
    [t.join() for t in threads]
    print("task done")


def greeter(name: str, count: int = 10):
    for i in range(count):
        print(f'{i + 1}hello {name}')
        time.sleep(1)


if __name__ == '__main__':
    main()
