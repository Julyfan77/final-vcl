import math


def getarc(x1, y1, xc, yc, x2, y2):
    vec1 = [x1 - xc, y1 - yc]
    vec2 = [x2 - xc, y2 - yc]
    sin = (vec1[0] * vec2[1] - vec2[0] * vec1[1]) / (
                math.sqrt(vec1[0] ** 2 + vec1[1] ** 2) * math.sqrt(vec2[0] ** 2 + vec2[1] ** 2))
    cos = (vec1[0] * vec2[0] + vec1[1] * vec2[1]) / (
                math.sqrt(vec1[0] ** 2 + vec1[1] ** 2) * math.sqrt(vec2[0] ** 2 + vec2[1] ** 2))
    if sin < 0:
        return -math.acos(cos)
    else:
        return math.acos(cos)


if __name__ == '__main__':
    print(getarc(1, 0, 0, 0, -1, 1) / math.pi)
