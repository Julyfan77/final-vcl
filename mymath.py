import math
def getarc(x1,y1,xc,yc,x2,y2):
    vec1=[xc-x1,yc-y1]
    vec2=[xc-x2,yc-y2]
    length=math.sqrt((vec1[0]-vec2[0])*(vec1[0]-vec2[0])+(vec1[1]-vec2[1])*(vec1[1]-vec2[1]))
    cos=(vec1[0]*vec2[0]+vec1[1]*vec2[1])/length
    return math.cos(cos)