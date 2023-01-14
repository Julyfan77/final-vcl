
class mypoint():
    def __init__(self,x,y,col,wid,pb):
        self.type=6
        #1-straight,2-circle,3-rec,4-fillrec,5-fillcircle,6-curve
        self.Gx=x
        self.Gy=y
        self.col=col
        self.wid=wid
        self.pb=pb
        
    def updateG(self):
        pass
    def draw(self):
        self.pb.draw_point(self.x,self.y,self.col,self.wid)
class rec_drawitem():
    def __init__(self,points,col,wid,style,pb):
        self.type=3
        #1-straight,2-circle,3-rec,4-fillrec,5-fillcircle,6-curve
        self.points=points
        self.Gx=0
        self.Gy=0
        self.col=col
        self.wid=wid
        self.style=style
        n=len(self.points)
        self.pb=pb
        for i in range(n):
            self.Gx+=self.points[i][0]
            self.Gy+=self.points[i][1]
        self.Gx/=n
        self.Gy/=n
    def updateG(self):
        n=len(self.points)
        self.Gx=0
        self.Gy=0
        for i in range(n):
            self.Gx+=self.points[i][0]
            self.Gy+=self.points[i][1]
        self.Gx/=n
        self.Gy/=n
    def draw(self):
        nowwid=self.wid
        nowcol=self.col
        for iter in range(len(self.points)):
            self.pb.style=self.style
            
            self.pb.draw_line(self.points[(iter)%len(self.points)][0],
            self.points[(iter)%len(self.points)][1],
            self.points[(iter+1)%len(self.points)][0],
            self.points[(iter+1)%len(self.points)][1])
                
class line_drawitem():
    def __init__(self,points,col,wid,style,pb):
        self.type=1
        #1-straight,2-circle,3-rec,4-fillrec,5-fillcircle,6-curve
        self.points=points
        self.Gx=0
        self.Gy=0
        self.col=col
        self.wid=wid
        self.style=style
        self.pb=pb
        n=len(self.points)
        for i in range(n):
            self.Gx+=self.points[i][0]
            self.Gy+=self.points[i][1]
        self.Gx/=n
        self.Gy/=n
    def updateG(self):
        n=len(self.points)
        self.Gx=0
        self.Gy=0
        for i in range(n):
            self.Gx+=self.points[i][0]
            self.Gy+=self.points[i][1]
        self.Gx/=n
        self.Gy/=n
    def draw(self):
        nowwid=self.wid
        nowcol=self.col
        self.pb.style=self.style
        self.pb.draw_line(self.points[0][0],self.points[0][1],
            self.points[1][0],self.points[1][1])
class circle_drawitem():
    def __init__(self,xc,yc,r,col,wid,pb):
        self.type=2
        #1-straight,2-circle,3-rec,4-fillrec,5-fillcircle,6-curve
        self.xc=xc
        self.yc=yc
        self.r=r
        self.Gx=self.xc
        self.Gy=self.yc
        self.col=col
        self.wid=wid
        self.pb=pb
    def updateG(self):
        self.Gx=self.xc
        self.Gy=self.yc
    def draw(self):
        nowwid=self.wid
        nowcol=self.col
        self.pb.drawRound(self.xc,self.yc,self.r)
class fill_rec_drawitem():
    def __init__(self,x1,y1,x2,y2,col,wid,style,pb):
        self.type=4
        #1-straight,2-circle,3-rec,4-fillrec,5-fillcircle,6-curve
        self.x1=x1
        self.x2=x2
        self.y1=y1
        self.y2=y2
        self.style=style
        self.Gx=(self.x1+self.x2)/2
        self.Gy=(self.y1+self.y2)/2
        self.col=col
        self.wid=wid
        self.pb=pb
    def updateG(self):
        self.Gx=(self.x1+self.x2)/2
        self.Gy=(self.y1+self.y2)/2
    def draw(self):
        nowwid=self.wid
        nowcol=self.col
        self.pb.brushstyle=self.style
        self.pb.draw_fill_rec(self.x1,self.x2,self.y1,self.y2)
class fill_circle_drawitem(circle_drawitem):
    def __init__(self,xc,yc,r,col,wid,style,pb):
        self.type=5
        self.style=style
        super().__init__(xc,yc,r,col,wid,pb)
    def updateG(self):
        self.Gx=self.xc
        self.Gy=self.yc
    def draw(self):
        nowwid=self.wid
        nowcol=self.col
        self.pb.brushstyle=self.style
        self.pb.draw_fill_circle(self.xc,self.yc,self.r,pb)
def getdis_2(x1,y1,x2,y2):
    return (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)