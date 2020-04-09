'''
Raytracable sphere
'''
import numpy as np
import vector_class as v
from hitable_class import Hitable

class sphere(Hitable):
    '''
    sphere
    '''
    def __init__(self, centre, radius, material):
        self.centre = centre
        self.radius = radius
        self.material = material

    def __repr__(self):
        return str(self.centre) + ', ' + str(self.radius) + ', ' + str(self.material) + '\n'

    def hit(self, this_ray, t_min, t_max, rec):
        '''
        Register a hit of a ray on the sphere geometry.
        '''
        oc = this_ray.origin - self.centre
        a = v.vec3.dot_product(this_ray.direction, this_ray.direction)
        b = v.vec3.dot_product(oc, this_ray.direction)
        c = v.vec3.dot_product(oc, oc) - self.radius * self.radius
        discriminant = b * b - a * c
        if discriminant > 0:
            temp = (-b - np.sqrt(discriminant)) / a
            if temp < t_max and temp > t_min:
                rec.t = temp
                rec.p = this_ray.point_at_parameter(rec.t)
                rec.normal = (rec.p - self.centre) / self.radius
                rec.material = self.material
                return True
            temp = (-b + np.sqrt(discriminant)) / a
            if temp < t_max and temp > t_min:
                rec.t = temp
                rec.p = this_ray.point_at_parameter(rec.t)
                rec.normal = (rec.p - self.centre) / self.radius
                rec.material = self.material
                return True
        return False
