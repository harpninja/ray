'''
Hitable list class
'''
from hitable_class import Hitable, hit_record

class Hitable_List(Hitable):
    '''
    List of hitable objects.
    '''
    def __init__(self, hitable_objects):
        self.hitable_objects = hitable_objects

    def hit(self, ray, t_min, t_max, rec):
        '''
        Implementation of abstract base class for a hit on a surface.
        '''
        tmp_hit_rec = hit_record()
        hit_anything = False
        closest_so_far = t_max
        for obj in self.hitable_objects:
            if obj.hit(ray, t_min, closest_so_far, tmp_hit_rec):
                hit_anything = True
                closest_so_far = tmp_hit_rec.t
                rec.t = tmp_hit_rec.t
                rec.p = tmp_hit_rec.p
                rec.normal = tmp_hit_rec.normal
                rec.material = tmp_hit_rec.material
        return hit_anything
