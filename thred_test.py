from threading import Thread
import time


class Worker:
    def __init__(self):
        self.status = False
        self.task = False
        self.timer = 12

    def start(self):
        self.thread = Thread(target=self.cycle, daemon=True)
        self.status = True
        self.task = True
        self.thread.start()

    def stop(self):
        self.status = False
        self.task = False
        #self.t1.join()

    def restart(self):
        self.task = True

    def pause(self):
        self.task = False

    def cycle(self):
        try:
            print("I am Worker")

            while self.status:
                if self.task:
                    for i in range(self.timer):
                        print("I am Worker. I am alive")
                        time.sleep(0.25)
                    self.pause()
                else:
                    print("I am Worker. ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
                    time.sleep(0.25)
            print("I am extra Thread. BLEEEEE")
        except:
            self.status = False
            self.task = False
            print("BLEEE")



worker = Worker()
worker.start()

count = 0
res_time = 8
max_time = 80
for i in range(max_time):
    print("i am master thread. Worker status:", worker.status, "- Task status:", worker.task)

    if i == max_time-1:
        worker.stop()

    if worker.status:
        if not worker.task:
            if count >= res_time:
                print("i am master thread. Reviving...")
                count = 0
                worker.restart()
            elif count < res_time:
                print("i am master thread. Counter", count)
                count = count + 1
    else:
        print("i am master thread. Worker is no longer with us :(")
        if i != max_time-1:
            worker.start()

    time.sleep(1)
