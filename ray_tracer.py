import config as cf
import math

class Vector3:
    def __init__(self, data):
        self.d = []
        if isinstance(data, list):
            self.d = data
        elif isinstance(data, Vector3):
            self.d = data.d
        else:
            print("empty Vector3 constructor ")

    def length(self):
        return math.sqrt( pow(self.d[0],2) + pow(self.d[1],2) + pow(self.d[2],2))

    def normalize(self):
        ll = self.length()
        if(ll == 0.): 
            print("length is 0, normalization is not possible")
        else:
            ll = 1./ll
            for i in range(3):
                self.d[i] *= ll
    
    def x(self):
        return self.d[0]

    def y(self):
        return self.d[1]

    def z(self):
        return self.d[2]

    def __add__(self, other):
        elements = [x+y for x,y in zip(self.d, other.d)]
        return Vector3(elements)

    def __sub__(self, other):
        elements = [x-y for x,y in zip(self.d, other.d)]
        return Vector3(elements)

    def __mul__(self, other):
       if isinstance(other, Vector3):
           """ dot product """
           elements = [x*y for x,y in zip(self.d, other.d)]
           return Vector3(elements)
       else:
           """ scaling """
           elements = [x*other for x in self.d]

    def __lt__(self, other):
        islower = True
        for i in range(3):
            islower = islower and self.d[i] < other.d[i]
        return islower

    def dump(self):
        print("Vector3 : ", self.d[0], " ", self.d[1], " ", self.d[2])



class Ray:
    def __init__(self, in_point, out_point):
        self.origin = in_point
        self.direction = out_point - in_point
        self.direction.normalize()


        self.inv_direction = Vector3([1./self.direction.x(), 1./self.direction.y(), 1./self.direction.z()])
        self.sign = [1 if(x<0) else 0 for x in self.inv_direction.d]
        
    def set_tmin(self, t):
        self.tmin = t
    def set_tmax(self, t):
        self.tmax = t

class Box:
    def __init__(self, low, high):
        assert(low < high)
        self.par = [low, high]

    def intersect(self, r, t0, t1):
        """ this could be re-written in a more concise way """
        tmin = (self.par[r.sign[0]].x() - r.origin.x())*r.inv_direction.x()
        tmax = (self.par[1-r.sign[0]].x() - r.origin.x())*r.inv_direction.x()

        tymin = (self.par[r.sign[1]].y() - r.origin.y())*r.inv_direction.y()
        tymax = (self.par[1-r.sign[1]].y() - r.origin.y())*r.inv_direction.y()
    

        if( (tmin > tymax) or (tymin > tmax)):
            return False
        if( tymin > tmin):
            tmin = tymin
        if( tymax < tmax):
            tmax = tymax

        tzmin = (self.par[r.sign[2]].z() - r.origin.z())*r.inv_direction.z()
        tzmax = (self.par[1-r.sign[2]].z() - r.origin.z())*r.inv_direction.z()

        if( (tmin > tzmax) or (tzmin > tmax)):
            return False
        if(tzmin > tmin):
            tmin = tzmin
        if(tzmax < tmax):
            tmax = tzmax


        r.set_tmin(tmin)
        r.set_tmax(tmax)
        return (tmin < t1) and (tmax > t0)

    def get_points(self, r):
        rin = [0., 0., 0.]
        rout = [0., 0., 0.]
        
        for i in range(3):
            rin[i] = r.origin.d[i] + r.direction.d[i]*r.tmin
            rout[i] = r.origin.d[i] + r.direction.d[i]*r.tmax
        return rin, rout
          
    def get_point_in(self, r):
        return [o+d*r.tmin for o,d in zip(r.origin.d, r.direction.d)]

    def get_point_out(self, r):
        return [o+d*r.tmax for o,d in zip(r.origin.d, r.direction.d)]
