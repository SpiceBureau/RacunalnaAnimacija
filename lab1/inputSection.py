import numpy as np


class processInput:
    def __init__(self):
        pass

    @staticmethod
    def getVF(file):
        openedFile = open(file, 'r')
        v = []
        f = []
        for line in openedFile.readlines():
            if line[0] == "v":
                vectorV = line[2:-1]
                v.append(vectorV.split(" "))

            if line[0] == "f":
                vectorF = line[2:-1]
                f.append(vectorF.split(" "))


        v = np.asarray(v).astype(float)

        return v, f

