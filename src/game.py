import math
import random
import pygame
from src.settings import PHASES, W
from src.background import Background
from src.player import Player
from src.entities import Enemy, Obstacle, Coin, Heart
from src.hud import HUD


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.bg = Background()
        self.hud = HUD()
        self.running = True
        self._reset()
        self.state = "menu"

    def _reset(self):
        self.player = Player()
        self.enemies: list[Enemy] = []
        self.obstacles: list[Obstacle] = []
        self.coins: list[Coin] = []
        self.hearts: list[Heart] = []
        self.particles: list[dict] = []
        self.score = 0
        self.coin_count = 0
        self.phase_idx = 0
        self.phase_timer = 0
        self.banner_timer = 0
        self.bg = Background()
        self.enemy_timer = 0
        self.obstacle_timer = 0
        self.coin_timer = 0
        self.heart_timer = 0
        self.t = 0
        self.state = "phase_banner"

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if self.state == "menu":
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self._reset()
                elif self.state == "playing":
                    if event.key in (pygame.K_UP, pygame.K_SPACE, pygame.K_w):
                        self.player.jump()
                    if event.key in (pygame.K_z, pygame.K_x, pygame.K_j):
                        self.player.attack()
                elif self.state in ("game_over", "victory"):
                    if event.key == pygame.K_r:
                        self.state = "menu"

    def _update(self):
        self.t += 1

        if self.state == "menu":
            return

        if self.state == "phase_banner":
            self.banner_timer += 1
            self.bg.update(PHASES[self.phase_idx]["speed"] * 0.3)
            if self.banner_timer >= 150:
                self.banner_timer = 0
                self.state = "playing"
            return

        if self.state in ("game_over", "victory"):
            return

        phase = PHASES[self.phase_idx]
        speed = phase["speed"]
        self.phase_timer += 1
        self.score += 1

        self.bg.update(speed)
        self.player.update()

        self.enemy_timer += 1
        self.obstacle_timer += 1
        self.coin_timer += 1
        self.heart_timer += 1

        if self.enemy_timer >= phase["enemy_rate"]:
            self.enemy_timer = 0
            self.enemies.append(Enemy(speed))

        if self.obstacle_timer >= phase["obstacle_rate"]:
            self.obstacle_timer = 0
            if random.random() < 0.7:
                self.obstacles.append(Obstacle(speed))

        if self.coin_timer >= 60:
            self.coin_timer = 0
            if random.random() < 0.6:
                self.coins.append(Coin(W + 20, speed))

        if self.heart_timer >= 400:
            self.heart_timer = 0
            if random.random() < 0.15:
                self.hearts.append(Heart(W + 20, speed))

        for e in self.enemies:   e.update()
        for o in self.obstacles: o.update()
        for c in self.coins:     c.update()
        for h in self.hearts:    h.update()

        self.enemies   = [e for e in self.enemies   if e.x > -80 or not e.alive and e.die_timer < 25]
        self.obstacles = [o for o in self.obstacles if o.x > -80]
        self.coins     = [c for c in self.coins     if c.x > -30 and c.alive]
        self.hearts    = [h for h in self.hearts    if h.x > -30 and h.alive]

        self._check_collisions()
        self._update_particles()

        if self.phase_timer >= phase["duration"]:
            self.phase_timer = 0
            self.enemy_timer = 0
            self.obstacle_timer = 0
            self.enemies.clear()
            self.obstacles.clear()
            self.hearts.clear()
            self.phase_idx += 1
            if self.phase_idx >= len(PHASES):
                self.state = "victory"
            else:
                self.state = "phase_banner"

        if self.player.hp <= 0:
            self.state = "game_over"

    def _check_collisions(self):
        p = self.player
        p_rect = p.rect
        atk_rect = p.get_attack_rect()

        invincible_frames = 120 if self.phase_idx == 2 else 90
        for e in self.enemies:
            if not e.alive:
                continue
            if atk_rect and atk_rect.colliderect(e.rect):
                e.hit()
                self.score += 150
                self._spawn_particles(e.x + 16, e.y + 16, (200, 40, 40))
            elif p_rect.colliderect(e.rect):
                if p.take_damage(invincible_frames):
                    self._spawn_particles(p.x + 18, p.y + 20, (255, 100, 50))

        for o in self.obstacles:
            if p_rect.colliderect(o.rect) and p.obstacle_cooldown == 0:
                self.score = max(0, self.score - 100)
                p.obstacle_cooldown = 45
                p.vy = -4
                self._spawn_particles(p.x + 18, p.y + 20, (255, 200, 50))

        for c in self.coins:
            if c.alive and p_rect.colliderect(c.rect):
                c.alive = False
                self.coin_count += 1
                self.score += 50
                self._spawn_particles(c.x, c.y, (255, 220, 60), count=8, size=3)

        for h in self.hearts:
            if h.alive and p_rect.colliderect(h.rect):
                h.alive = False
                p.hp = min(3, p.hp + 1)
                self._spawn_particles(h.x, h.y, (255, 80, 80), count=12, size=4)

    def _spawn_particles(self, x, y, color, count=12, size=4):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1.5, 5.0)
            self.particles.append({
                "x": x, "y": y,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed - 2,
                "life": random.randint(18, 35),
                "max_life": 35,
                "color": color,
                "size": size,
            })

    def _update_particles(self):
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.2
            p["life"] -= 1
        self.particles = [p for p in self.particles if p["life"] > 0]

    def _draw_particles(self):
        for p in self.particles:
            alpha = int(255 * p["life"] / p["max_life"])
            s = pygame.Surface((p["size"] * 2, p["size"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*p["color"], alpha), (p["size"], p["size"]), p["size"])
            self.screen.blit(s, (int(p["x"]) - p["size"], int(p["y"]) - p["size"]))

    def _draw(self):
        phase_idx = min(self.phase_idx, len(PHASES) - 1)
        self.bg.draw(self.screen, phase_idx)

        if self.state == "menu":
            self.bg.update(PHASES[0]["speed"] * 0.4)
            self.hud.draw_menu(self.screen, self.t)
            pygame.display.flip()
            return

        if self.state == "phase_banner":
            alpha = min(255, self.banner_timer * 6)
            self.hud.draw_phase_banner(
                self.screen,
                PHASES[phase_idx]["name"],
                phase_idx,
                alpha,
            )
            pygame.display.flip()
            return

        for h in self.hearts:    h.draw(self.screen)
        for c in self.coins:     c.draw(self.screen)
        for o in self.obstacles: o.draw(self.screen)
        for e in self.enemies:   e.draw(self.screen)
        self.player.draw(self.screen)
        self._draw_particles()

        phase = PHASES[phase_idx]
        progress = self.phase_timer / phase["duration"]
        self.hud.draw(
            self.screen,
            self.player,
            self.score,
            self.phase_idx,
            progress,
            phase["name"],
            self.coin_count,
        )

        if self.state == "game_over":
            self.hud.draw_game_over(self.screen, self.score, self.coin_count)
        elif self.state == "victory":
            self.hud.draw_victory(self.screen, self.score, self.coin_count)

        pygame.display.flip()
