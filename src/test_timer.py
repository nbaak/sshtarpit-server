
import time

def test():
    start = time.time()
    
    time.sleep(5)
    
    
    stop = time.time()
    print(stop-start)


if __name__ == "__main__":
    test()