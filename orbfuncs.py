"""----------------------------------------------------------------------------------------------------------------------------------------------------"""
### MODULES ###

from math import sin, cos

"""----------------------------------------------------------------------------------------------------------------------------------------------------"""
### CARRE ###

def carre(obj):
    
    x, y = obj.or_x, obj.or_y
    t = obj.t_orbite
    o_x, o_y = 0, 0
    s = obj.speed
    rs = obj.rotation_sens
    if rs == 'left':
        s = - s

    if y == o_y and ((x != o_x + t and rs == 'right') or (x != o_x and rs == 'left')):
        return (s, 0)
    elif y == o_y + t and ((x != o_x and rs == 'right') or (x != o_x + t and rs == 'left')):
        return (- s, 0)
    elif x == o_x:
        return (0, - s)
    elif x == o_x + t:
        return (0, s)
    else:
        print('Erreur')
        return (0, 0)

"""----------------------------------------------------------------------------------------------------------------------------------------------------"""
### CERCLE ###

def cercle(obj):

    change = obj.speed / 100
    
    if obj.rotation_sens == 'left':
        change = - change

    # obj.angle *= 10
    obj.angle += change

    if obj.angle >= obj.max_angle or obj.angle <= obj.min_angle:
        if obj.inv_rotation:
            obj.rotation_sens = {'right': 'left', 'left': 'right'}[obj.rotation_sens]
        else:
            obj.angle %= obj.max_angle

    x, y = cos(obj.angle) * obj.t_orbite + obj.parent.x, sin(obj.angle) * obj.t_orbite + obj.parent.y

    # obj.angle /= 10

    return (x - obj.x, y - obj.y)
