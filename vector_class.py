'''
Vector class
'''
import numpy as np

class vec3():
    '''
    Three dimensional vector class.
    '''
    def __init__(self, x, y, z):
        (self.x, self.y, self.z) = (x, y, z)
        self.values = (self.x, self.y, self.z)

    def __repr__(self):
        return str(self.x) + ', ' + str(self.y) + ', ' + str(self.z)

    def __getitem__(self, key):
        return self.values[key]

    def __add__(self, other):
        if isinstance(other, self.__class__):
            # other is a vector
            return vec3(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            # other is a scalar
            return vec3(self.x + other, self.y + other, self.z + other)

    def __sub__(self, other):
        return vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            # other is a vector
            return vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            # other is a scalar
            return vec3(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        if isinstance(other, self.__class__):
            # other is a vector
            return vec3(other.x * self.x, other.y * self.y, other.z * self.z)
        else:
            # other is a scalar
            return vec3(other * self.x, other * self.y, other * self.z)

    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            # other is a vector
            return vec3(self.x / other.x, self.y / other.y, self.z / other.z)
        else:
            # other is a scalar
            return vec3(self.x / other, self.y / other, self.z / other)

    def __neg__(self):
        return vec3(-self.x, -self.y, -self.z)

    def __abs__(self):
        '''
        Absolute value or magnitude of vector
        '''
        x = self.x**2
        y = self.y**2
        z = self.z**2
        return np.sqrt(x + y + z)

    def unit_vector(self):
        '''
        Normalised vector or unit vector.
        '''
        magnitude = abs(self)
        x = self.x * (1.0 / np.where(magnitude == 0, 1, magnitude))
        y = self.y * (1.0 / np.where(magnitude == 0, 1, magnitude))
        z = self.z * (1.0 / np.where(magnitude == 0, 1, magnitude))
        return vec3(x, y, z)

    def dot_product(self, other):
        '''
        Sum of products of vectors.
        '''
        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)

    def cross_product(self, other):
        '''
        New vector at right angles to self and other.
        '''
        x = (self.y * other.z) - (self.z * other.y)
        y = (self.z * other.x) - (self.x * other.z)
        z = (self.x * other.y) - (self.y * other.x)
        return vec3(x, y, z)

    def squared_length(self):
        '''
        Squared length of self vector.
        Returns float.
        '''
        return self.x * self.x + self.y * self.y + self.z * self.z
