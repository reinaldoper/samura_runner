import pygame
import math
from src.settings import (
    W, H, PHASES, GROUND_Y, MOON_COLOR, SAKURA_COLOR,
    MOUNTAIN_FAR, MOUNTAIN_MID, PAGODA_COLOR,
    TREE_DARK, TREE_MID, GROUND_TOP, GROUND_BOT, GRASS_COLOR,
)


class Background:
    def __init__(self):
        self.offsets = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.factors = [0.03, 0.12, 0.25, 0.5, 1.0]
        self.t = 0

    def update(self, speed):
        self.t += 1
        for i in range(len(self.offsets)):
            self.offsets[i] += speed * self.factors[i]

    def draw(self, surface, phase_idx):
        phase = PHASES[phase_idx]
        sky_top = phase["bg_sky"]
        sky_bot = tuple(min(255, c + 40) for c in sky_top)
        self._draw_sky(surface, sky_top, sky_bot)
        self._draw_moon(surface)
        self._draw_sakura_particles(surface)
        self._draw_mountains_far(surface)
        self._draw_pagoda(surface)
        self._draw_mountains_mid(surface)
        self._draw_trees_back(surface)
        self._draw_ground(surface)

    def _draw_sky(self, surface, top, bot):
        for y in range(H):
            r = top[0] + (bot[0] - top[0]) * y // H
            g = top[1] + (bot[1] - top[1]) * y // H
            b = top[2] + (bot[2] - top[2]) * y // H
            pygame.draw.line(surface, (r, g, b), (0, y), (W, y))

    def _draw_moon(self, surface):
        mx = 720
        my = 70
        for r in range(45, 25, -5):
            alpha = max(0, 30 - (45 - r) * 8)
            s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*MOON_COLOR, alpha), (r, r), r)
            surface.blit(s, (mx - r, my - r))
        pygame.draw.circle(surface, MOON_COLOR, (mx, my), 28)
        pygame.draw.circle(surface, (200, 190, 140), (mx - 6, my - 4), 8)

    def _draw_sakura_particles(self, surface):
        positions = [
            (100, 60), (200, 90), (350, 50), (500, 80),
            (650, 55), (800, 75), (150, 120), (450, 100), (700, 110),
        ]
        for i, (bx, by) in enumerate(positions):
            ox = self.offsets[0]
            x = int((bx - ox * 0.5) % (W + 50)) - 25
            y = by + int(math.sin(self.t * 0.02 + i) * 8)
            s = pygame.Surface((8, 8), pygame.SRCALPHA)
            pygame.draw.circle(s, (*SAKURA_COLOR, 180), (4, 4), 4)
            surface.blit(s, (x, y))

    def _draw_mountains_far(self, surface):
        peaks = [
            (0, 180), (120, 120), (250, 160), (380, 100),
            (500, 150), (630, 110), (760, 170), (900, 130), (1020, 140),
        ]
        ox = int(self.offsets[1]) % 1050
        for bx, peak_h in peaks:
            x = (bx - ox) % 1050
            pts = [
                (x - 80, GROUND_Y - 10),
                (x,      GROUND_Y - 10 - peak_h),
                (x + 80, GROUND_Y - 10),
            ]
            pygame.draw.polygon(surface, MOUNTAIN_FAR, pts)
            snow = [
                (x,      GROUND_Y - 10 - peak_h),
                (x - 22, GROUND_Y - 10 - peak_h + 45),
                (x + 22, GROUND_Y - 10 - peak_h + 45),
            ]
            pygame.draw.polygon(surface, (200, 200, 220, 180), snow)

    def _draw_pagoda(self, surface):
        ox = int(self.offsets[1] * 0.15) % (W + 200)
        bx = (500 - ox) % (W + 200) - 100
        by = GROUND_Y - 10
        c = PAGODA_COLOR
        pygame.draw.rect(surface, c, (bx - 20, by - 60, 40, 60))
        for i, (w, h) in enumerate([(55, 18), (45, 16), (35, 14)]):
            ty = by - 60 - i * 30
            pygame.draw.rect(surface, c, (bx - w // 2, ty - h, w, h))
            roof = [
                (bx - w // 2 - 8, ty - h),
                (bx + w // 2 + 8, ty - h),
                (bx + w // 2,     ty - h - 10),
                (bx - w // 2,     ty - h - 10),
            ]
            pygame.draw.polygon(surface, (c[0] + 10, c[1] + 10, c[2] + 10), roof)
        pygame.draw.polygon(surface, c, [
            (bx,     by - 60 - 95),
            (bx - 6, by - 60 - 78),
            (bx + 6, by - 60 - 78),
        ])

    def _draw_mountains_mid(self, surface):
        peaks = [
            (50, 100), (180, 80), (320, 110), (460, 75),
            (600, 95), (740, 85), (880, 105), (1020, 90),
        ]
        ox = int(self.offsets[2]) % 1050
        for bx, peak_h in peaks:
            x = (bx - ox) % 1050
            pts = [
                (x - 70, GROUND_Y),
                (x,      GROUND_Y - peak_h),
                (x + 70, GROUND_Y),
            ]
            pygame.draw.polygon(surface, MOUNTAIN_MID, pts)

    def _draw_trees_back(self, surface):
        tree_xs = list(range(0, 1100, 65))
        ox = int(self.offsets[3]) % 1100
        for bx in tree_xs:
            x = (bx - ox) % 1100
            h = 90 + (bx % 35)
            pygame.draw.rect(surface, (40, 25, 10), (x + 10, GROUND_Y - 30, 8, 35))
            for layer, (lw, _) in enumerate([(30, 0), (38, 18), (44, 34)]):
                color = TREE_DARK if layer % 2 == 0 else TREE_MID
                pygame.draw.polygon(surface, color, [
                    (x + 14,      GROUND_Y - 30 - h + layer * 20),
                    (x + 14 - lw, GROUND_Y - 30 - h + layer * 20 + 28),
                    (x + 14 + lw, GROUND_Y - 30 - h + layer * 20 + 28),
                ])

    def _draw_ground(self, surface):
        pygame.draw.rect(surface, GROUND_TOP, (0, GROUND_Y, W, 20))
        pygame.draw.rect(surface, GROUND_BOT, (0, GROUND_Y + 20, W, H - GROUND_Y - 20))
        ox = int(self.offsets[4]) % 80
        for gx in range(-ox, W + 80, 80):
            pygame.draw.polygon(surface, GRASS_COLOR, [
                (gx,      GROUND_Y),
                (gx + 6,  GROUND_Y - 12),
                (gx + 12, GROUND_Y),
            ])
            pygame.draw.polygon(surface, GRASS_COLOR, [
                (gx + 18, GROUND_Y),
                (gx + 24, GROUND_Y - 9),
                (gx + 30, GROUND_Y),
            ])
        for gx in range(-int(ox * 0.5), W + 80, 55):
            pygame.draw.ellipse(surface, (65, 50, 30), (gx, GROUND_Y + 5, 30, 10))
