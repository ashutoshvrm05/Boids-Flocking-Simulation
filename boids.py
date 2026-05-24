import pygame
import random
import math


class Boid():
    
    def __init__(self):

        self.SEPARATION = 1
        self.ALIGNMENT = 1
        self.COHESION = 1

        self.p = Vector(random.uniform(100, 800), random.uniform(100, 800))
        self.vu = Vector(random.uniform(-1,1), random.uniform(-1,1))
        self.vu = self.vu.normalise()
        self.vm = 2

        arrow_font = pygame.font.SysFont('couriernew, consolas, monospace', 45, bold=True)
        self.original_arrow_surface = arrow_font.render("→", True, (255,255,255))
        self.original_rect = self.original_arrow_surface.get_rect(center=(self.p.xcomp, self.p.ycomp))

        self.rotated_arrow_surface = pygame.transform.rotate(self.original_arrow_surface, self.vu.angleX())
        self.rotated_rect = self.rotated_arrow_surface.get_rect(center=self.original_rect.center)

        # print(self.x, " ", self.y, " ", self.vx, " ", self.vy)
    
    def update_boid(self, neighbors, s, a, c):
        separation_vector = self.calc_sep(neighbors)
        alignment_vector = self.calc_align(neighbors)
        cohesion_vector = self.calc_cohe(neighbors)

        wall_vector = self.avoid_wall()
        
        current_velocity = self.vu * self.vm

        new_velocity = current_velocity + (separation_vector)*(s/100) + (alignment_vector)*(a/100) + (cohesion_vector)*(c/100) + (wall_vector)*0.2

        speed = abs(new_velocity)
        if speed > 4:       
            new_velocity = new_velocity.normalise() * 4
        elif speed < 1.5:   
            new_velocity = new_velocity.normalise() * 1.5

        self.vm = abs(new_velocity)
        if self.vm > 0:
            self.vu = new_velocity.normalise()

        self.p = self.p + new_velocity

        self.original_rect = self.original_arrow_surface.get_rect(center=(int(self.p.xcomp), int(self.p.ycomp)))
        self.rotated_arrow_surface = pygame.transform.rotate(self.original_arrow_surface, -self.vu.angleX())
        self.rotated_rect = self.rotated_arrow_surface.get_rect(center=self.original_rect.center)

    def calc_sep(self, neighbors):
        # si = summation of (pi - pj)/(pi - pj)^2
        s = Vector(0, 0)
        for boid in neighbors:
            diff = self.p - boid.p
            dist_sq = (diff.xcomp * diff.xcomp) + (diff.ycomp * diff.ycomp) 
            
            if dist_sq > 0: 
                s = s + diff * (1 / dist_sq)

        return s
    
    def calc_align(self, neighbors):
        n = len(neighbors)
        if n > 0:
            sum_vel = Vector(0,0)
            for boid in neighbors:
                sum_vel = sum_vel + (boid.vu * boid.vm) 
            
            avg_vel = sum_vel * (1/n)
            
            current_vel = self.vu * self.vm
            steering = avg_vel - current_vel
            return steering
        else:
            return Vector(0,0)
        
    def calc_cohe(self, neighbors):
        n = len(neighbors)

        if n > 0:
            c = Vector(0,0)
            sum = Vector(0,0)
            for boid in neighbors:
                sum = sum + boid.p
            c = sum*(1/n) -self.p
            return c
        else:
            return Vector(0,0)
        
    def avoid_wall(self):
        margin = 100
        turn_factor = 0.4

        steer = Vector(0,0)

        if self.p.xcomp < margin:
            steer.xcomp = steer.xcomp + turn_factor
        elif self.p.xcomp > 900-margin:
            steer.xcomp = steer.xcomp - turn_factor 
        
        if self.p.ycomp < margin:
            steer.ycomp = steer.ycomp + turn_factor
        elif self.p.ycomp > 900-margin:
            steer.ycomp = steer.ycomp - turn_factor 

        return steer

class SpatialGrid:
    def __init__(self, width, height, radius):
        self.cell_size = radius
        self.cols = math.ceil(width / self.cell_size)
        self.rows = math.ceil(height / self.cell_size)
        
        self.cells = [[] for _ in range(self.cols * self.rows)]

    def clear(self):
        for cell in self.cells:
            cell.clear()

    def _constrain(self, val, min_val, max_val):
        return max(min_val, min(val, max_val))

    def get_cell_index(self, x, y):
        grid_x = self._constrain(int(x // self.cell_size), 0, self.cols - 1)
        grid_y = self._constrain(int(y // self.cell_size), 0, self.rows - 1)
        return grid_x + (grid_y * self.cols)

    def insert(self, boid):
        index = self.get_cell_index(boid.p.xcomp, boid.p.ycomp)
        self.cells[index].append(boid)

    def get_neighbors(self, boid):
        neighbors = []
        
        grid_x = int(boid.p.xcomp // self.cell_size)
        grid_y = int(boid.p.ycomp // self.cell_size)
        
        for offset_y in [-1, 0, 1]:
            for offset_x in [-1, 0, 1]:
                check_x = grid_x + offset_x
                check_y = grid_y + offset_y
                
                if 0 <= check_x < self.cols and 0 <= check_y < self.rows:
                    index = check_x + (check_y * self.cols)
                    
                    for other_boid in self.cells[index]:
                        if other_boid is not boid:
                            neighbors.append(other_boid)
                            
        return neighbors


class Vector():

    def __init__(self, x, y):
        self.xcomp = x
        self.ycomp = y

    def normalise(self):
        mag = abs(self)
        return Vector(self.xcomp/mag, self.ycomp/mag)
    
    def angleX(self):
        return math.degrees(math.atan2(self.ycomp, self.xcomp))
        
    def __add__(self, other):
        return Vector(self.xcomp + other.xcomp, self.ycomp + other.ycomp)
    
    def __sub__(self, other):
        return Vector(self.xcomp - other.xcomp, self.ycomp - other.ycomp)

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector(self.xcomp * scalar, self.ycomp * scalar)

    def __abs__(self):
        return math.sqrt(self.xcomp*self.xcomp + self.ycomp*self.ycomp)


def main():

    NUM_OF_BOIDS = 500
    SEPARATION_WEIGHT = 10
    ALIGNMENT_WEIGHT = 12
    COHESION_WEIGHT = 0.1
    VISIBILITY_RADIUS = 20

    pygame.init()

    screen = pygame.display.set_mode((900, 900))
    pygame.display.set_caption("Boids Simulation")
    clock = pygame.time.Clock()
    boid_font = pygame.font.SysFont('couriernew, consolas, monospace', 14, bold=True)

    grid = SpatialGrid(900, 900, VISIBILITY_RADIUS)

    boids = []
    for i in range(0, NUM_OF_BOIDS):
        boids.append(Boid())

    running = True
    myboid = Boid()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill((0,0,0))

        grid.clear()
        for boid in boids:
            grid.insert(boid)

        for boid in boids:
            neighbor = grid.get_neighbors(boid)
            boid.update_boid(neighbor, SEPARATION_WEIGHT, ALIGNMENT_WEIGHT, COHESION_WEIGHT)
            screen.blit(boid.rotated_arrow_surface, boid.rotated_rect)
        
        # myboid.update_boid()
        # screen.blit(myboid.rotated_arrow_surface, myboid.rotated_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()


if __name__ == "__main__":
    main()