#!/usr/bin/env python3

from .log import debug, report, error

def true_ground_velocity(x, z, a, b, c, d):
    """Here we define the true ground velocity"""
    return (  (x-c)**2 / a**2  +  (z-d)**2 / b**2)

