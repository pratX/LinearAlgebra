import math
import decimal

decimal.getcontext().prec = 30

class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError           
            self.dimension = len(coordinates)
            for i in range(0, self.dimension, 1):
                coordinates[i] = decimal.Decimal(coordinates[i])    
            self.coordinates = tuple(coordinates)
        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')
        self.CANNOT_NORMALIZE_ZERO_VECTOR = "Cannot normalize zero vector"
        self.PROJECTION_TO_ZERO_VECTOR_UNDEFINED = "Projection to zero vector undefined"
        self.CROSS_PRODUCT_DEFINED_ONLY_IN_THREE_DIMENSIONS = "Cross product defined only in three dimensions"        

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def __add__(self, v):
        w = []
        if self.dimension == v.dimension:
            for i in range(0,len(self.coordinates)):
                w.append(self.coordinates[i] + v.coordinates[i])
            return Vector(w)
        raise Exception("Dimension Mismatch")
    
    def __sub__(self, v):
        w = []
        if self.dimension == v.dimension:
            for i in range(0,len(self.coordinates)):
                w.append(self.coordinates[i] - v.coordinates[i]) 
            return Vector(w)
        raise Exception("Dimension Mismatch")   
        
    def scale(self, a):
        a = decimal.Decimal(a)
        w = []
        for i in range(0, len(self.coordinates)):
            w.append(self.coordinates[i] * a)
        return Vector(w)

    def magnitude(self):
        mag = 0
        for i in self.coordinates:
          mag = mag + (i*i)
        return mag.sqrt()         

    def normalize(self):
        try:
            return self.scale(1/(self.magnitude()))
        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR) 

    def dotProduct(self, v):
        dp = 0
        if self.dimension != v.dimension:
            raise Exception("Dimension Mismatch")
        for i in range(0,self.dimension,1):
            dp = dp + (self.coordinates[i]*v.coordinates[i])  
        return dp

    def angle(self, v, degrees=False):
        mag_self = self.magnitude()
        mag_v = v.magnitude()
        mag_vw = mag_self * mag_v
        if mag_vw == 0:
            raise Exception("Zero magnitude vector doesn't have any direction") 
        dp = self.dotProduct(v)
        if not degrees:
            return math.acos(dp/mag_vw)
        else:
            return math.degrees(math.acos(dp/mag_vw))
                    
    def isParallel(self, v, tolerance=decimal.Decimal(1e-10)):
        if self.dimension != v.dimension:
            raise Exception("Dimension Mismatch")
        if (self.magnitude() == 0) or (v.magnitude() == 0):
            return True
        idx = 0
        while self.coordinates[idx] == 0:
            if v.coordinates[idx] != 0:
                return False
            idx += 1
        if v.coordinates[idx] == 0:
            return False
        n = self.coordinates[idx]/v.coordinates[idx]
        for i in range(idx, self.dimension, 1):
            if v.coordinates[i] == 0:
                if self.coordinates[i] != 0:
                    return False
                else:
                    continue
            if decimal.getcontext().abs(n - self.coordinates[i]/v.coordinates[i]) > tolerance:
                return False
        return True

    def isOrthogonal(self, v, tolerance = decimal.Decimal(1e-10)):
        dp = self.dotProduct(v)
        if decimal.getcontext().abs(dp -  decimal.Decimal(0)) > tolerance:
            return False
        else:
            return True   

    def projection(self, base):
        try:
            n_base = base.normalize()       
            return n_base.scale(self.dotProduct(n_base))
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR:
                raise Exception(self.PROJECTION_TO_ZERO_VECTOR_UNDEFINED)
            else:
                raise e 

    def projection_perp(self, base):
        p = self.projection(base)
        return self.__sub__(p)


    def crossProduct(self, v):
        if self.dimension != 3 or v.dimension != 3: 
            raise Exception(self.CROSS_PRODUCT_DEFINED_ONLY_IN_THREE_DIMENSIONS)
        res = []
        # x coordinate
        res.append( (self.coordinates[1] * v.coordinates[2]) - (v.coordinates[1] * self.coordinates[2]) )
        # y coordinate
        res.append( -1 * ((self.coordinates[0] * v.coordinates[2]) - (v.coordinates[0] * self.coordinates[2])) )
        # z coordinate
        res.append( (self.coordinates[0] * v.coordinates[1]) - (v.coordinates[0] * self.coordinates[1]) )
        return Vector(res)


    def area_parallelogram(self, v):
        try:
            cp = self.crossProduct(v) 
            return cp.magnitude()
        except Exception as e:
            if str(e) == self.CROSS_PRODUCT_DEFINED_ONLY_IN_THREE_DIMENSIONS:
                raise Exception("Change the vectors to three dimensions")
            else:
                raise e

    def area_triangle(self, v):
        return 0.5 * self.area_parallelogram(v)
        
    
            
                


#v = Vector([8.218, -9.341])
#w = Vector([-1.129, 2.111])
#print v+w
#print Vector([7.119, 8.215]) - Vector([-8.223, 0.878])
#print Vector([1.671, -1.012, -0.318]).scale(7.41)

#print Vector([-0.221, 7.437]).magnitude()
#print Vector([8.813, -1.331, -6.247]).magnitude()
#print Vector([5.581, -2.136]).normalize()
#print Vector([1.996, 3.108, -4.554]).normalize()


#print Vector([7.887, 4.138]).dotProduct(Vector([-8.802, 6.776]))
#print Vector([-5.955, -4.904, -1.874]).dotProduct(Vector([-4.496, -8.755, 7.103]))
#print Vector([3.183, -7.627]).angle(Vector([-2.668, 5.319]))
#print Vector([7.35, 0.221, 5.188]).angle(Vector([2.751, 8.259, 3.985]), degrees = True)

#print Vector([-7.579, -7.88]).isParallel(Vector([22.737, 23.64]))
#print Vector([-7.579, -7.88]).isOrthogonal(Vector([22.737, 23.64]))
#print 
#print Vector([-2.029, 9.97, 4.172]).isParallel(Vector([-9.231, -6.639, -7.245]))
#print Vector([-2.029, 9.97, 4.172]).isOrthogonal(Vector([-9.231, -6.639, -7.245]))
#print
#print Vector([-2.328, -7.284, -1.214]).isParallel(Vector([-1.821, 1.072, -2.94]))
#print Vector([-2.328, -7.284, -1.214]).isOrthogonal(Vector([-1.821, 1.072, -2.94]))
#print
#print Vector([2.118, 4.827]).isParallel(Vector([0, 0]))
#print Vector([2.118, 4.827]).isOrthogonal(Vector([0, 0]))

print Vector([3.039, 1.879]).projection(Vector([0.825, 2.036]))
print Vector([-9.88, -3.264, -8.159]).projection_perp(Vector([-2.155, -9.353, -9.473]))
print Vector([3.009, -6.172, 3.692, -2.51]).projection(Vector([6.404, -9.144, 2.759, 8.718]))
print Vector([3.009, -6.172, 3.692, -2.51]).projection_perp(Vector([6.404, -9.144, 2.759, 8.718]))



