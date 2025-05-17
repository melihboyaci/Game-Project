import pygame
from ..utils.planet import Planet

class PlanetManager:
    def __init__(self):
        self.planets = []

    def add_planet(self, planet):
        self.planets.append(planet)
    
    def update(self):
        for planet in self.planets:
            planet.update()

    def draw(self, screen, camera_pos):
        for planet in self.planets:
            planet.draw(screen, camera_pos)

