import multiprocessing
def fun():
    while True:
        print("s")

        
if __name__ == "__main__":
    ps = multiprocessing.Process(target=fun,)
    ps.start()
    while True:
        print("m")