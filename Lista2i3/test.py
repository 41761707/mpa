import numpy as np

def main():
    for i in range(100000):
        a = np.random.normal(10,1)
        if a<0:
            print('ALERT')
if __name__ == '__main__':
    main()