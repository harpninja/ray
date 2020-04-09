import numpy as np
import sys
import random
import math
import vector_class as v
import ray_class as r
import sphere_class as s
import camera_class as c
import material_class as m
from hitable_class import hit_record
from hitable_list_class import Hitable_List

MAXFLOAT = sys.float_info.max
sys.setrecursionlimit(1500)  # increase python's default recursion limit of 1000

def random_in_unit_sphere():
    '''
    Random rays.
    Returns: vec3
    '''
    pt = v.vec3(0.0, 0.0, 0.0)
    while True:
        pt = 2.0 * v.vec3(random.random(), random.random(), random.random()) - v.vec3(1, 1, 1)
        if pt.squared_length() >= 1.0:
            break
    return pt

def build_scene():
    scene = []
    scene.append(s.sphere(v.vec3(0, -1000, 0), 1000, m.Lambert(v.vec3(0.5, 0.5, 0.5))))

    # ranges were -11 to 11
    for a in range(-4, 4, 1):     # start, stop, step
        for b in range(-4, 4, 1):     # start, stop, step
            choose_mat = random.random()
            centre = v.vec3(a + 0.9 * random.random(), 0.2, b + 0.9 * random.random())
            if abs(centre - v.vec3(4, 0.2, 0)) > 0.9:
                if choose_mat < 0.8:    # diffuse
                    scene.append(s.sphere(centre, 0.2, m.Lambert(v.vec3(random.random(), random.random(), random.random()))))
                elif choose_mat < 0.95:     # metal
                    scene.append(s.sphere(centre, 0.2, m.Metal(v.vec3(0.5 * (1 +random.random()), 0.5 * (1 +random.random()), 0.5 * (1 +random.random())), 0.5*random.random())))
                else:
                    scene.append(s.sphere(centre, 0.2, m.Dielectric(1.5)))

    scene.append(s.sphere(v.vec3(0, 1, 0), 1.0, m.Dielectric(1.5)))
    scene.append(s.sphere(v.vec3(-4, 1, 0), 1.0, m.Lambert(v.vec3(0.4, 0.2, 0.1))))
    scene.append(s.sphere(v.vec3(4, 1, -1), 1.0, m.Metal(v.vec3(0.7, 0.6, 0.5), 0.0)))

    return Hitable_List(scene)

def colour(this_ray, world, depth):
    '''
    Colour pixel based on ray hit.
    '''
    rec = hit_record()

    if world.hit(this_ray, 0.001, MAXFLOAT, rec):
        scattered = r.ray(v.vec3(0.0, 0.0, 0.0), v.vec3(0.0, 0.0, 0.0))
        attenuation = v.vec3(0.0, 0.0, 0.0)
        hit = rec.material.scatter(this_ray, rec, attenuation, scattered)
        if depth < 50 and hit[0]:
            # hit 1 = scattered, hit 2 = albedo
            return colour(hit[1], world, depth + 1) * hit[2]     # return coloured ray
        else:
            return v.vec3(0.0, 0.0, 0.0)

    # blue background
    unit_direction = v.vec3.unit_vector(this_ray.direction)
    t = 0.5 * (unit_direction.y + 1.0)
    return (1.0 - t) * v.vec3(1.0, 1.0, 1.0) + t * v.vec3(0.5, 0.7, 1.0)

def main():
    '''
    Write a ppm file.
    '''
    world = build_scene()

    nx = 200
    ny = 100
    ns = 100
    look_from = v.vec3(13, 2, 3)
    look_at = v.vec3(0, 0, 0)
    dist_to_focus = 10  # was abs(look_from - look_at)
    aperture = 0.1
    cam1 = c.camera(look_from, look_at, v.vec3(0,1,0), 20, nx/ny, aperture, dist_to_focus)

    output_file = 'out.ppm'
    f = open(output_file, 'w')
    f.write('P3\n' + str(nx) + ' ' + str(ny) + '\n255\n')

    for j in range(ny - 1, -1, -1):
        for i in range(0, nx):
            col = v.vec3(0, 0, 0)
            for k in range(0, ns):
                u_coord = (i + random.random()) / nx  # 0.0 <= random.random() < 1.0
                v_coord = (j + random.random()) / ny
                this_ray = cam1.get_ray(u_coord, v_coord)
                col = col + colour(this_ray, world, 0)

            col = col / ns
            col = v.vec3(np.sqrt(col[0]), np.sqrt(col[1]), np.sqrt(col[2])) # gamma correction
            ir = int(255.99 * col[0])
            ig = int(255.99 * col[1])
            ib = int(255.99 * col[2])
            f.write(str(ir) + ' ' +   str(ig) + ' ' + str(ib) + '\n')
    f.close()

main()
