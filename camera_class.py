'''
Camera class
'''
import math
import random
import vector_class as v
import ray_class as r

def random_in_unit_disk():
    '''
    Random rays.
    Returns: vec3
    '''
    pt = v.vec3(0.0, 0.0, 0.0)
    while True:
        pt = 2.0 * v.vec3(random.random(), random.random(), 0) - v.vec3(1, 1, 0)
        if pt.dot_product(pt) >= 1.0:
            break
    return pt

class camera():
    '''
    Simple axis aligned camera.
    '''
    def __init__(self, look_from, look_at, v_up, vertical_fov, aspect, aperture, focus_distance):
        self.lens_radius = aperture / 2
        self.cw = v.vec3.unit_vector(look_from - look_at)
        cu_cross = v_up.cross_product(self.cw)
        self.cu = cu_cross.unit_vector()
        self.cv = self.cw.cross_product(self.cu)

        self.origin = look_from
        self.theta = vertical_fov * math.pi / 180
        self.half_height = math.tan(self.theta/2)
        self.half_width = aspect * self.half_height

        self.lower_left_corner = self.origin - self.half_width* focus_distance * self.cu - self.half_height * focus_distance * self.cv- focus_distance * self.cw
        self.horizontal = 2 * self.half_width * focus_distance * self.cu
        self.vertical = 2 * self.half_height * focus_distance * self.cv

    def __repr__(self):
        return str(self.lower_left_corner) + ', ' + str(self.horizontal) + ', ' + str(self.vertical) + ', ' + str(self.origin)

    def get_ray(self, u_coord, v_coord):
        '''
        Return ray at position.
        '''
        rd = self.lens_radius * random_in_unit_disk()
        offset = self.cu * rd.x + self.cv * rd.y
        return r.ray(self.origin + offset, self.lower_left_corner + u_coord * self.horizontal + v_coord * self.vertical - self.origin - offset)
