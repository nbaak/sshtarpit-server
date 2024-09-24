
import time
import random 


class DeltaTimer:

    def __init__(self):
        self.time = int(time.time())
        
    def delta_now(self):
        now = int(time.time())
        delta_now = now - self.time
        self.time = now
        return delta_now
        
        
def test():
    dt = DeltaTimer()
    
    while True:
        time.sleep(random.randint(1, 5))
        print(dt.delta_now())    
    
    
if __name__ == "__main__":
    test()
