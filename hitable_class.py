'''
Hitable class
'''
from abc import ABC
import vector_class as v

class Hitable(ABC):
    '''
    Abstract base class for a hit on a surface.
    '''
    def hit(self, this_ray, t_min, t_max, rec):
        pass

class hit_record:
    '''
    Record of a ray hitting scene geometry.
    '''
    def __init__(self, t=0.0, p=v.vec3(0.0, 0.0, 0.0), normal=v.vec3(0.0, 0.0, 0.0)):
        self.t = t              # float
        self.p = p              # vec3
        self.normal = normal    # vec3
        self.material = None    # material class instance

    def __repr__(self):
        return str(self.t) + ', ' + str(self.p) + ', ' + str(self.normal) + '\n'
