import pygame
import math
from src.settings import GRAVITY, GROUND_Y


class Player:
    def __init__(self):
        self.x = 130
        self.y = float(GROUND_Y - 60)
        self.vy = 0.0
        self.on_ground = False
        self.jumps_left = 2
        self.state = "run"
        self.t = 0
        self.invincible = 0
        self.obstacle_cooldown = 0
        self.hp = 3
        self.width = 36
        self.height = 56
        self.attacking = False
        self.attack_timer = 0
        self.attack_cooldown = 0

    @property
    def rect(self):
        return pygame.Rect(self.x + 6, self.y + 4, self.width - 12, self.height - 4)

    def jump(self):
        if self.jumps_left > 0:
            self.vy = -13.5 if self.jumps_left == 2 else -11.0
            self.jumps_left -= 1
            self.on_ground = False

    def attack(self):
        if self.attack_cooldown <= 0 and self.state not in ("hurt", "dead"):
            self.attacking = True
            self.attack_timer = 18
            self.attack_cooldown = 30
            self.state = "attack"

    def take_damage(self, invincible_frames=90):
        if self.invincible > 0 or self.state == "dead":
            return False
        self.hp -= 1
        self.invincible = invincible_frames
        self.vy = -6
        self.state = "hurt" if self.hp > 0 else "dead"
        return True

    def get_attack_rect(self):
        if self.attacking:
            return pygame.Rect(self.x + self.width - 4, self.y + 10, 40, 30)
        return None

    def update(self):
        self.t += 1
        self.invincible = max(0, self.invincible - 1)
        self.obstacle_cooldown = max(0, self.obstacle_cooldown - 1)
        self.attack_cooldown = max(0, self.attack_cooldown - 1)

        self.vy += GRAVITY
        self.y += self.vy

        if self.y >= GROUND_Y - self.height:
            self.y = float(GROUND_Y - self.height)
            self.vy = 0
            self.on_ground = True
            self.jumps_left = 2
        else:
            self.on_ground = False

        if self.state == "dead":
            return
        if self.attack_timer > 0:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.attacking = False
                self.state = "run" if self.on_ground else ("fall" if self.vy > 0 else "jump")
        elif self.state == "hurt":
            if self.invincible < 75:
                self.state = "run" if self.on_ground else "fall"
        else:
            if self.on_ground:
                self.state = "run"
            elif self.vy < 0:
                self.state = "jump"
            else:
                self.state = "fall"

    def draw(self, surface):
        if self.invincible > 0 and (self.t // 4) % 2 == 0 and self.state != "dead":
            return

        x, y = int(self.x), int(self.y)
        t = self.t
        run_bob = math.sin(t * 0.35) * 3 if self.state == "run" else 0
        y = int(y + run_bob)

        shadow = pygame.Surface((36, 10), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 80), (0, 0, 36, 10))
        surface.blit(shadow, (x + 2, GROUND_Y - 4))

        if self.state == "run":
            lswing = math.sin(t * 0.35) * 14
        elif self.state in ("jump", "fall"):
            lswing = -20 if self.vy < 0 else 10
        else:
            lswing = 0

        leg_color = (30, 15, 10)
        pts_leg_l = [
            (x + 10, y + 44),
            (x + 8,  y + 44 + lswing + 18),
            (x + 16, y + 44 + lswing + 18),
            (x + 18, y + 44),
        ]
        pygame.draw.polygon(surface, leg_color, pts_leg_l)
        pts_leg_r = [
            (x + 20, y + 44),
            (x + 18, y + 44 - lswing + 18),
            (x + 26, y + 44 - lswing + 18),
            (x + 28, y + 44),
        ]
        pygame.draw.polygon(surface, leg_color, pts_leg_r)

        pygame.draw.rect(surface, (60, 40, 20), (x + 5,  y + 44 + lswing + 17, 14, 5))
        pygame.draw.rect(surface, (60, 40, 20), (x + 15, y + 44 - lswing + 17, 14, 5))

        kimono_pts = [
            (x + 6,  y + 20),
            (x + 30, y + 20),
            (x + 34, y + 46),
            (x + 2,  y + 46),
        ]
        pygame.draw.polygon(surface, (180, 20, 20), kimono_pts)
        pygame.draw.line(surface, (130, 10, 10), (x + 18, y + 20), (x + 18, y + 46), 2)
        pygame.draw.line(surface, (220, 180, 40), (x + 6, y + 32), (x + 30, y + 32), 1)

        pygame.draw.rect(surface, (50, 50, 60), (x + 2,  y + 20, 10, 8))
        pygame.draw.rect(surface, (50, 50, 60), (x + 24, y + 20, 10, 8))

        arm_swing = math.sin(t * 0.35 + math.pi) * 10 if self.state == "run" else 0
        if self.state == "attack":
            prog = 1 - (self.attack_timer / 18)
            arm_angle = -30 + prog * 120
        else:
            arm_angle = arm_swing

        sword_arm_x = x + 28
        sword_arm_y = y + 24
        arm_rad = math.radians(arm_angle)
        ex = sword_arm_x + math.cos(arm_rad) * 28
        ey = sword_arm_y + math.sin(arm_rad) * 28
        pygame.draw.line(
            surface, (160, 15, 15),
            (sword_arm_x, sword_arm_y),
            (int(ex - math.cos(arm_rad) * 14), int(ey - math.sin(arm_rad) * 14)),
            6,
        )
        blade_start = (
            int(sword_arm_x + math.cos(arm_rad) * 6),
            int(sword_arm_y + math.sin(arm_rad) * 6),
        )
        blade_end = (
            int(ex + math.cos(arm_rad) * 16),
            int(ey + math.sin(arm_rad) * 16),
        )
        blade_mid = (
            int((blade_start[0] + blade_end[0]) // 2),
            int((blade_start[1] + blade_end[1]) // 2),
        )
        pygame.draw.line(surface, (210, 210, 230), blade_start, blade_end, 3)
        pygame.draw.line(surface, (255, 255, 255), blade_start, blade_mid, 1)
        pygame.draw.circle(surface, (180, 150, 30), blade_start, 4)

        left_arm_x = x + 8
        left_arm_y = y + 24
        left_rad = math.radians(-arm_swing)
        lax = left_arm_x + math.cos(left_rad) * 16
        lay = left_arm_y + math.sin(left_rad) * 16
        pygame.draw.line(
            surface, (160, 15, 15),
            (left_arm_x, left_arm_y),
            (int(lax), int(lay)),
            5,
        )

        head_y = y + 10
        pygame.draw.circle(surface, (45, 45, 55), (x + 18, head_y), 14)
        pygame.draw.rect(surface, (45, 45, 55), (x + 6, head_y, 24, 12))
        pygame.draw.rect(surface, (60, 60, 70), (x + 4, head_y + 8, 28, 5))
        pygame.draw.ellipse(surface, (200, 160, 120), (x + 9, head_y - 2, 18, 16))

        if self.state == "dead":
            pygame.draw.line(surface, (80, 40, 40), (x + 11, head_y + 4), (x + 14, head_y + 7), 2)
            pygame.draw.line(surface, (80, 40, 40), (x + 14, head_y + 4), (x + 11, head_y + 7), 2)
            pygame.draw.line(surface, (80, 40, 40), (x + 20, head_y + 4), (x + 23, head_y + 7), 2)
            pygame.draw.line(surface, (80, 40, 40), (x + 23, head_y + 4), (x + 20, head_y + 7), 2)
        else:
            pygame.draw.circle(surface, (20, 10, 10), (x + 13, head_y + 5), 2)
            pygame.draw.circle(surface, (20, 10, 10), (x + 22, head_y + 5), 2)

        pygame.draw.line(surface, (200, 30, 30), (x + 18, head_y - 14), (x + 18, head_y - 6), 3)
        pygame.draw.circle(surface, (220, 50, 50), (x + 18, head_y - 15), 4)

        if self.attacking and self.attack_timer > 10:
            s = pygame.Surface((70, 40), pygame.SRCALPHA)
            alpha = int(200 * (self.attack_timer / 18))
            pygame.draw.arc(
                s, (255, 255, 200, alpha),
                (0, 0, 70, 40),
                math.radians(-30), math.radians(60),
                3,
            )
            surface.blit(s, (x + 20, y + 10))
