'''
Material class
'''
from abc import ABC, abstractmethod
import random
import numpy as np
import vector_class as v
import ray_class as r

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

def reflect(vec_v, vec_n):
    '''
    Reflection of vector off surface.
    Parameters: vec3, vec3
    Returns: vec3
    '''
    return vec_v - 2 * vec_v.dot_product(vec_n) * vec_n

def refract(vec_v, vec_n, ni_over_nt, refracted):
    '''
    Refraction of vector with surface.
    Parameters: vec3, vec3, float, vec3
    Returns: Boolean, vec3
    '''
    uv = vec_v.unit_vector()
    dt = uv.dot_product(vec_n)
    discriminant = 1.0 - ni_over_nt * ni_over_nt * (1 - dt * dt)
    if discriminant > 0:
        refracted = ni_over_nt * (uv - vec_n * dt) - vec_n * np.sqrt(discriminant)
        return True, refracted
    else:
        return False, refracted

def schlick(cosine, refractive_index):
    '''
    Vary amount of reflectivity according to viewing angle.
    Parameters: float, float
    Returns: float
    '''
    r0 = (1 - refractive_index) / (1 + refractive_index)
    r0 = r0 * r0
    return r0 + (1 - r0) * np.power((1 - cosine), 5)

class Material(ABC):
    '''
    Abstract method for scattering rays off a material surface.
    '''
    @abstractmethod
    def scatter(self, this_ray, rec, attenuation, scattered):
        pass

class Lambert(Material):
    '''
    Lambertian, or diffuse, material.
    '''
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, this_ray, rec, attenuation, scattered):
        target = rec.p + rec.normal + random_in_unit_sphere()
        scattered = r.ray(rec.p, target-rec.p)
        return True, scattered, self.albedo

class Metal(Material):
    '''
    Metallic, or shiny, material.
    Fuzz = 0 for perfect reflections.
    Fuzz = 1 for blurry reflections.
    '''
    def __init__(self, albedo, fuzz):
        self.albedo = albedo
        if fuzz < 1:
            self.fuzz = fuzz
        else:
            self.fuzz = 1

    def scatter(self, this_ray, rec, attenuation, scattered):
        reflected = reflect(this_ray.direction.unit_vector(), rec.normal)
        offset = reflected * 0.01
        scattered = r.ray(rec.p, reflected + offset + self.fuzz * random_in_unit_sphere())
        dot = scattered.direction.dot_product(rec.normal)
        return dot > 0, scattered, self.albedo

class Dielectric(Material):
    '''
    Dielectric, or glass, material.
    '''
    def __init__(self, ri):
        self.ri = ri    # refractive index

    def scatter(self, this_ray, rec, attenuation, scattered):
        outward_normal = v.vec3(0.0, 0.0, 0.0)
        refracted = v.vec3(0.0, 0.0, 0.0)
        reflected = reflect(this_ray.direction.unit_vector(), rec.normal)
        ni_over_nt = 0.0
        reflect_prob = 0.0
        cosine = 0.0
        attenuation = v.vec3(1.0, 1.0, 1.0)

        if this_ray.direction.dot_product(rec.normal) > 0:
            outward_normal = -rec.normal
            ni_over_nt = self.ri
            cosine = self.ri * this_ray.direction.dot_product(rec.normal) / abs(this_ray.direction)
        else:
            outward_normal = rec.normal
            ni_over_nt = 1.0 / self.ri
            cosine = -this_ray.direction.dot_product(rec.normal) / abs(this_ray.direction)

        refract_result = refract(this_ray.direction, outward_normal, ni_over_nt, refracted)
        if refract_result[0]:
            reflect_prob = schlick(cosine, self.ri)
        else:
            scattered = r.ray(rec.p, reflected)
            reflect_prob = 1.0

        if random.random() < reflect_prob:
            scattered = r.ray(rec.p, reflected)
        else:
            scattered = r.ray(rec.p, refract_result[1])

        return True, scattered, attenuation
