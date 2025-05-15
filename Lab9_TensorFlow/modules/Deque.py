from collections import deque
import threading
import time

class Deque:
    def __init__(self, maxlen=None):
        self.deque = deque(maxlen=maxlen)
        self.condition = threading.Condition()
    
    def append(self, item):
        with self.condition: # 加锁
            self.deque.append(item) # 添加元素
            self.condition.notify() # 通知
    
    def pop(self, timeout=1):
        with self.condition: # 加锁
            while len(self.deque) == 0: # 队列为空时
                if not self.condition.wait(timeout): # 等待
                    raise TimeoutError("等待超时")    # 超时
            return self.deque.popleft() # 弹出队首元素

    def __str__(self):
        with self.condition:
            return str(list(self.deque))

# 测试代码
if __name__ == "__main__":
    lock = threading.Lock()
    d = Deque(maxlen=3)
    
    def producer():
        for i in range(5):
            with lock:
                d.append(i)
                print(f"生产: {i}")
                print(f"队列: {d}\n")
            time.sleep(i)

    def consumer():
        try:
            for i in range(5):
                with lock:
                    item = d.pop()
                    print(f"消费: {item}")
                    print(f"队列: {d}\n")
        except TimeoutError:
            print("等待超时\n")
    
    
    consumer_thread = threading.Thread(target=consumer)
    producer_thread = threading.Thread(target=producer)
    producer_thread.start()
    consumer_thread.start()

    
