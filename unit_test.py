from PyQt5.QtCore import QPointF
from copy import deepcopy

if __name__ == '__main__':
    p = []
    p.append(QPointF(0, 21))
    p.append(QPointF(10222, 210))
    q = deepcopy(p)
    q[0].setX(2.3)
    print(p)
    print(q)
