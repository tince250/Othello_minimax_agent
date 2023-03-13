from game import Game
import time

def main():
    g = Game()
    stime = time.time()
    g.play()
    etime = time.time()
    print("time:", etime-stime)
    #print(g.heuristics())

if __name__ == '__main__':
    main()
