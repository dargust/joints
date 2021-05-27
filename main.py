import sys, pygame
import time
from pygame.math import Vector2
pygame.init()

clock = pygame.time.Clock()

size = width, height = 640, 480
screen = pygame.display.set_mode(size)

points = list(map(Vector2, [(100, 100), (200, 100), (300, 100), (400, 100), (500, 100)]))
target = Vector2(450, 300)
target_speed = Vector2(3, 3)

rel_points = []
angles = []

max_angle = 360 # Adjust for limited angles

for i in range(1, len(points)):
    rel_points.append(points[i] - points[i-1])
    angles.append(0)

def solve_ik(i, endpoint, target):
    if i < len(points) - 2:
        endpoint = solve_ik(i+1, endpoint, target)
    current_point = points[i]

    angle = (endpoint-current_point).angle_to(target-current_point)
    angles[i] += min(max(-3, angle), 3)
    angles[i] = min(max(180-max_angle, (angles[i]+180)%360), 180+max_angle)-180

    return current_point + (endpoint-current_point).rotate(angle)

def render():
    black = 0, 0, 0
    white = 255, 255, 255

    screen.fill(white)
    for i in range(1, len(points)):
        prev = points[i-1]
        cur = points[i]
        pygame.draw.aaline(screen, black, prev, cur)
    for point in points:
        pygame.draw.circle(screen, black, (int(point[0]), int(point[1])), 5)
    pygame.draw.circle(screen, black, (int(target[0]), int(target[1])), 10)
    pygame.display.flip()

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    solve_ik(0, points[-1], target)
    angle = 0
    for i in range(1, len(points)):
        angle += angles[i-1]
        points[i] = points[i-1] + rel_points[i-1].rotate(angle)

    x,y = pygame.mouse.get_pos()
    target.x = x
    target.y = y

    render()

    clock.tick(60)

pygame.quit()