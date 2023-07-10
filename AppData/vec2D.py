import math
import copy

PI = math.pi 

class vec2D :
    def __init__(self, dx = 0, dy = 0):
        self.x = dx
        self.y = dy
    
    def __copy__(self) :
        return vec2D(self.x, self.y)

    def set(self,dx,dy,length=0):
        l,r = 0.0,1e6
        for i in range(100):
            mid=(l+r)/2
            if (mid*dx)**2+(mid*dy)**2 < length**2:
                l=mid
            else:
                r=mid
        self.x=l*dx
        self.y=l*dy
    
    def set_angle(self, a, length=0):
        self._x = length*math.cos(a/180*PI)
        self._y = length*math.sin(a/180*PI)

    def __iadd__(self,other):
        self.x+=other.x
        self.y+=other.y
        return self
    def __isub__(self,other):
        self.x-=other.x
        self.y-=other.y
        return self
    def __imul__(self,other):
        self.x*=other
        self.y*=other
        return self
    def __add__(a,b):
        ret=vec2D(float(a.x),float(a.y))
        ret.x+=b.x
        ret.x+=b.y
        return ret
    def __sub__(a,b):
        ret=vec2D(float(a.x),float(a.y))
        ret.x-=b.x
        ret.x-=b.y
        return ret
    def __mul__(a,b):
        ret=vec2D(float(a.x),float(a.y))
        ret.x*=b
        ret.y*=b
        return ret
    def __eq__(self,other):
        return self.x==other.x and self.y==other.y
    def __ne__(self,other):
        return ~(self==other)
    def get_tuple(self):
        return (self.x,self.y)

def dis(a,b):
    return math.sqrt((a.x-b.x)**2+(a.y-b.y)**2)

def dot(a,b):
    return a.x*b.x+a.y*b.y