import pygame
import math
import random
from src.settings import W, GROUND_Y


class Enemy:
    def __init__(self, speed):
        self.x = float(W + 20)
        self.y = float(GROUND_Y - 52)
        self.speed = speed + random.uniform(0.5, 1.5)
        self.hp = 1
        self.alive = True
        self.t = 0
        self.die_timer = 0
        self.width = 32
        self.height = 50

    @property
    def rect(self):
        return pygame.Rect(self.x + 4, self.y + 4, self.width - 8, self.height - 4)

    def update(self):
        self.t += 1
        if not self.alive:
            self.die_timer += 1
            self.y -= 1
            return
        self.x -= self.speed

    def hit(self):
        self.alive = False
        self.die_timer = 0

    def draw(self, surface):
        x, y = int(self.x), int(self.y)
        alpha = max(0, 255 - self.die_timer * 12) if not self.alive else 255

        s = pygame.Surface((self.width + 10, self.height + 10), pygame.SRCALPHA)
        sx, sy = 5, 5

        run_bob = math.sin(self.t * 0.4) * 3 if self.alive else 0
        sy = int(sy + run_bob)

        lswing = math.sin(self.t * 0.4) * 12
        leg_color = (20, 20, 20)
        pygame.draw.polygon(s, leg_color, [
            (sx + 8,  sy + 38), (sx + 6,  sy + 52 + lswing),
            (sx + 14, sy + 52 + lswing), (sx + 16, sy + 38),
        ])
        pygame.draw.polygon(s, leg_color, [
            (sx + 18, sy + 38), (sx + 16, sy + 52 - lswing),
            (sx + 24, sy + 52 - lswing), (sx + 26, sy + 38),
        ])

        pygame.draw.rect(s, (15, 15, 20), (sx + 4, sy + 16, 26, 24))

        pygame.draw.circle(s, (15, 15, 20), (sx + 17, sy + 10), 12)
        pygame.draw.rect(s, (15, 15, 20), (sx + 5, sy + 10, 24, 10))
        pygame.draw.circle(s, (200, 20, 20),  (sx + 12, sy + 9), 2)
        pygame.draw.circle(s, (200, 20, 20),  (sx + 22, sy + 9), 2)
        pygame.draw.circle(s, (255, 100, 100), (sx + 12, sy + 9), 1)
        pygame.draw.circle(s, (255, 100, 100), (sx + 22, sy + 9), 1)

        arm_x = sx + 4
        arm_y = sy + 20
        pygame.draw.line(s, (15, 15, 20), (arm_x, arm_y), (arm_x - 10, arm_y + 8), 5)
        kunai_pts = [
            (arm_x - 18, arm_y + 14),
            (arm_x - 12, arm_y + 10),
            (arm_x - 8,  arm_y + 16),
        ]
        pygame.draw.polygon(s, (150, 160, 170), kunai_pts)

        fade = pygame.Surface(s.get_size(), pygame.SRCALPHA)
        fade.fill((255, 255, 255, alpha))
        s.blit(fade, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        surface.blit(s, (x - 5, y - 5))


class Obstacle:
    TYPES = ["bamboo", "torch", "stone"]

    def __init__(self, speed):
        self.x = float(W + 10)
        self.speed = speed
        self.kind = random.choice(self.TYPES)
        self.t = 0
        self.alive = True

        if self.kind == "bamboo":
            self.width, self.height = 18, 70
            self.y = float(GROUND_Y - self.height)
        elif self.kind == "torch":
            self.width, self.height = 14, 40
            self.y = float(GROUND_Y - self.height)
        else:
            self.width, self.height = 34, 28
            self.y = float(GROUND_Y - self.height)

    @property
    def rect(self):
        return pygame.Rect(self.x + 2, self.y + 2, self.width - 4, self.height - 2)

    def update(self):
        self.t += 1
        self.x -= self.speed

    def draw(self, surface):
        x, y = int(self.x), int(self.y)
        if self.kind == "bamboo":
            self._draw_bamboo(surface, x, y)
        elif self.kind == "torch":
            self._draw_torch(surface, x, y)
        else:
            self._draw_stone(surface, x, y)

    def _draw_bamboo(self, surface, x, y):
        for i in range(2):
            bx = x + i * 10
            pygame.draw.rect(surface, (60, 100, 30), (bx, y, 8, self.height))
            for ny in range(y + 10, y + self.height, 20):
                pygame.draw.rect(surface, (80, 130, 40), (bx - 1, ny, 10, 4))
        for i in range(3):
            lx = x - 10 + i * 14
            ly = y - 8 + (i % 2) * 6
            pygame.draw.ellipse(surface, (50, 130, 40), (lx, ly, 22, 9))

    def _draw_torch(self, surface, x, y):
        pygame.draw.rect(surface, (80, 55, 25), (x + 3, y + 8, 8, self.height - 8))
        pygame.draw.rect(surface, (100, 70, 30), (x, y + 4, 14, 8))

        flame_h = 14 + int(math.sin(self.t * 0.25) * 4)
        flame_w = 10 + int(math.sin(self.t * 0.3) * 3)
        pygame.draw.ellipse(
            surface, (255, 240, 200),
            (x + 4 - flame_w // 4, y - flame_h + 4, flame_w // 2, flame_h // 2),
        )
        pygame.draw.ellipse(
            surface, (255, 140, 30),
            (x + 2 - flame_w // 4, y - flame_h, flame_w, flame_h),
        )

        flame_pts = [
            (x + 7, y - flame_h - 4),
            (x + 1, y + 4),
            (x + 14, y + 4),
        ]
        blit_pos = (x - 3, y - flame_h - 4)
        s = pygame.Surface((20, flame_h + 12), pygame.SRCALPHA)
        rel_pts = [(px - blit_pos[0], py - blit_pos[1]) for px, py in flame_pts]
        pygame.draw.polygon(s, (200, 60, 10, 160), rel_pts)
        surface.blit(s, blit_pos)

    def _draw_stone(self, surface, x, y):
        pts = [
            (x + 4,             y + self.height),
            (x,                 y + self.height - 10),
            (x + 6,             y),
            (x + 20,            y - 4),
            (x + self.width,    y + 6),
            (x + self.width + 2, y + self.height),
        ]
        pygame.draw.polygon(surface, (80, 75, 70), pts)
        pygame.draw.polygon(surface, (100, 95, 90), [
            (x + 8, y + 4), (x + 18, y + 2),
            (x + self.width - 2, y + 10), (x + 10, y + 14),
        ])
        pygame.draw.circle(surface, (60, 55, 50), (x + 17, y + 14), 4)


class Coin:
    def __init__(self, x, speed):
        self.x = float(x)
        self.y = float(GROUND_Y - random.randint(30, 120))
        self.speed = speed
        self.t = 0
        self.alive = True
        self.radius = 8

    @property
    def rect(self):
        return pygame.Rect(
            self.x - self.radius, self.y - self.radius,
            self.radius * 2, self.radius * 2,
        )

    def update(self):
        self.t += 1
        self.x -= self.speed
        self.y += math.sin(self.t * 0.08) * 0.5

    def draw(self, surface):
        x, y = int(self.x), int(self.y)
        pulse = abs(math.sin(self.t * 0.1))
        glow = pygame.Surface((28, 28), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 200, 50, int(60 * pulse)), (14, 14), 13)
        surface.blit(glow, (x - 14, y - 14))
        pygame.draw.circle(surface, (200, 160, 30), (x, y), self.radius)
        pygame.draw.circle(surface, (240, 200, 60), (x, y), self.radius - 2)
        pygame.draw.circle(surface, (255, 230, 100), (x - 2, y - 2), 3)
        pygame.draw.circle(surface, (150, 100, 10), (x, y), 2)


class Heart:
    def __init__(self, x, speed):
        self.x = float(x)
        self.y = float(GROUND_Y - random.randint(50, 140))
        self.speed = speed
        self.t = 0
        self.alive = True
        self.radius = 10

    @property
    def rect(self):
        return pygame.Rect(
            self.x - self.radius, self.y - self.radius,
            self.radius * 2, self.radius * 2,
        )

    def update(self):
        self.t += 1
        self.x -= self.speed
        self.y += math.sin(self.t * 0.07) * 0.5

    def draw(self, surface):
        x, y = int(self.x), int(self.y)
        pulse = abs(math.sin(self.t * 0.1))
        color = (220, 40, 60)
        glow = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 80, 80, int(60 * pulse)), (16, 16), 14)
        surface.blit(glow, (x - 16, y - 16))
        pygame.draw.circle(surface, color, (x - 4, y - 2), 6)
        pygame.draw.circle(surface, color, (x + 4, y - 2), 6)
        pygame.draw.polygon(surface, color, [
            (x - 9, y + 2), (x, y + 12), (x + 9, y + 2),
        ])
        pygame.draw.circle(surface, (255, 100, 120), (x - 5, y - 4), 2)
