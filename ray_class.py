'''
Ray class
'''
class ray():
    '''
    Ray from origin in direction.
    Origin and direction are vec3.
    '''
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def __repr__(self):
        return 'origin: ' + str(self.origin) + ', direction: ' + str(self.direction) + '\n'

    def point_at_parameter(self, t):
        '''
        Position along the ray.
        '''
        return self.origin + self.direction * t
