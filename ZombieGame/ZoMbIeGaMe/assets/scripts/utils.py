"""A bunch of helpful stuff in one place. YAyyyyyyyyyyyyyyyyyyyyy. Please someone help me"""

import math

import pygame

sprite_info = {
    0: {'size': (18, 22), 'pos0': (0, 10), 'top_pos': (0, 0)},
    1: {'size': (16, 22), 'pos0': (0, 10), 'pos1': (0, 8), 'top_pos': (0, 0)},
    2: {'size': (16, 24), 'pos0': (0, 12), 'pos1': (0, 10), 'top_pos': (0, 0)},
    3: {'size': (16, 22), 'pos0': (0, 10), 'pos1': (0, 8), 'top_pos': (0, 0)},
    4: {'size': (20, 28), 'pos0': (2, 16), 'pos1': (0, 0), 'top_pos': (0, 0)},
    5: {'size': (18, 26), 'pos0': (0, 14), 'pos1': (0, 8), 'top_pos': (0, 0)},
    6: {'size': (18, 24), 'pos0': (2, 12), 'pos1': (0, 8), 'top_pos': (0, 0)},
    7: {'size': (16, 22), 'pos0': (0, 10), 'pos1': (0, 8), 'top_pos': (0, 0)},
    8: {'size': (16, 22), 'pos0': (0, 10), 'pos1': (0, 8), 'top_pos': (0, 0)},
    9: {'size': (16, 24), 'pos0': (0, 12), 'pos1': (0, 8), 'top_pos': (0, 0)},
    10: {'size': (16, 22), 'pos0': (0, 10), 'pos1': (0, 8), 'top_pos': (0, 0)},
    11: {'size': (16, 24), 'pos0': (0, 12), 'pos1': (0, 8), 'top_pos': (0, 0)},
    12: {'size': (18, 22), 'pos0': (0, 10), 'pos1': (0, 8), 'top_pos': (0, 0)},
    13: {'size': (16, 22), 'pos0': (0, 10), 'pos1': (0, 8), 'top_pos': (0, 0)},
    14: {'size': (16, 26), 'pos0': (0, 14), 'pos1': (0, 8), 'top_pos': (0, 0)},
    15: {'size': (18, 22), 'pos0': (0, 10), 'pos1': (0, 8), 'top_pos': (0, 0)},
    16: {'size': (18, 24), 'pos0': (0, 12), 'pos1': (0, 8), 'top_pos': (0, 0)},
    17: {'size': (18, 26), 'pos0': (0, 14), 'pos1 ': (0, 8), 'top_pos': (0, 0)},
}

keys = {
    'A': pygame.K_a,
    'B': pygame.K_b,
    'C': pygame.K_c,
    'D': pygame.K_d,
    'E': pygame.K_e,
    'F': pygame.K_f,
    'G': pygame.K_g,
    'H': pygame.K_h,
    'I': pygame.K_i,
    'J': pygame.K_j,
    'K': pygame.K_k,
    'L': pygame.K_l,
    'M': pygame.K_m,
    'N': pygame.K_n,
    'O': pygame.K_o,
    'P': pygame.K_p,
    'Q': pygame.K_q,
    'R': pygame.K_r,
    'S': pygame.K_s,
    'T': pygame.K_t,
    'U': pygame.K_u,
    'V': pygame.K_v,
    'W': pygame.K_w,
    'X': pygame.K_x,
    'Y': pygame.K_y,
    'Z': pygame.K_z 
}


def change_hue(surf, hue, exclusion=(0, 0, 0)):
    """Changes the hue of a surface for all colors not in the exclusion list and isn't black (bc dats not a coloure)."""
    for x in range(surf.get_width()):
        for y in range(surf.get_height()):
            color = surf.get_at((x, y))
            if color[:] not in exclusion and (color[:] != (0, 0, 0, 0) or color == (0, 0, 0)):
                new_hue = (color.hsla[0] + hue)
                new_color = pygame.Color(0)
                new_color.hsla = (new_hue, color.hsla[1], color.hsla[2], color.hsla[3])
                surf.set_at((x, y), new_color)
    surf = surf.copy()
    return surf

def darken(surf, percent):
    """Lilttarly just makes the surface dark by the percent passed (and returns the new surf)."""
    surf = surf.copy()
    percent = percent / 100
    dark_surf = pygame.Surface(surf.get_size()).convert_alpha()
    dark_surf.fill((0, 0, 0, int(percent * 255)))
    dark_surf.blit(surf, (0, 0))
    return surf

def rotate_on_pivot(surf, angle, pivot, origin):
    """Rotates things on te pivot i think idk"""
    surf = pygame.transform.rotate(surf, int(angle))
    offset = pivot + (origin - pivot).rotate(-angle)
    rect = surf.get_rect(center=offset)
    return surf, rect

def get_angle(d_pos):
    """Uhm if you didn't know it gets the angle."""
    return -math.degrees(math.atan2(d_pos.y, d_pos.x))

def get_angle_to_mouse(pos):
    """Uhm if you didn't know, it gets the angle to te mousE :). Havaday"""
    mouse_pos = pygame.math.Vector2(*pygame.mouse.get_pos())
    mouse_offset = mouse_pos - pos
    mouse_angle = get_angle(mouse_offset)
    return mouse_angle
