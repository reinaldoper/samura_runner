import pygame
import math
from src.settings import W, H


class HUD:
    def __init__(self):
        self.font_big   = pygame.font.Font(None, 32)
        self.font_med   = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)
        self.font_huge  = pygame.font.Font(None, 72)
        self.font_sub   = pygame.font.Font(None, 20)

    def draw(self, surface, player, score, phase_idx, phase_progress, phase_name, coins):
        self._draw_panel(surface)
        self._draw_hp(surface, player.hp)
        self._draw_score(surface, score, coins)
        self._draw_phase(surface, phase_idx, phase_name)
        self._draw_progress(surface, phase_progress)
        self._draw_controls(surface)

    def _draw_panel(self, surface):
        panel = pygame.Surface((W, 52), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 140))
        surface.blit(panel, (0, 0))
        pygame.draw.line(surface, (180, 140, 40), (0, 52), (W, 52), 1)

    def _draw_hp(self, surface, hp):
        label = self.font_small.render("VITALIDADE", True, (180, 140, 40))
        surface.blit(label, (12, 6))
        for i in range(3):
            x = 12 + i * 34
            y = 22
            color = (200, 40, 40) if i < hp else (50, 30, 30)
            pygame.draw.polygon(surface, color, [
                (x + 12, y + 4), (x + 4, y - 4), (x, y),
                (x + 12, y + 18), (x + 24, y), (x + 20, y - 4),
            ])
            pygame.draw.circle(surface, color, (x + 6,  y - 2), 6)
            pygame.draw.circle(surface, color, (x + 18, y - 2), 6)
            if i < hp:
                pygame.draw.polygon(surface, (230, 80, 80), [
                    (x + 12, y + 2), (x + 6, y - 2), (x + 4, y + 2),
                    (x + 12, y + 12), (x + 20, y + 2), (x + 18, y - 2),
                ])

    def _draw_score(self, surface, score, coins):
        label = self.font_small.render("PONTOS", True, (180, 140, 40))
        surface.blit(label, (W // 2 - 30, 6))
        score_txt = self.font_big.render(f"{score:06d}", True, (255, 230, 100))
        surface.blit(score_txt, (W // 2 - score_txt.get_width() // 2, 16))
        coin_txt = self.font_small.render(f"* {coins}", True, (220, 200, 60))
        surface.blit(coin_txt, (W // 2 + 60, 24))

    def _draw_phase(self, surface, phase_idx, phase_name):
        label = self.font_small.render("FASE", True, (180, 140, 40))
        surface.blit(label, (W - 160, 6))
        phase_txt = self.font_med.render(f"{phase_idx + 1}. {phase_name}", True, (220, 200, 160))
        surface.blit(phase_txt, (W - 165, 20))

    def _draw_progress(self, surface, progress):
        bar_x, bar_y, bar_w, bar_h = 12, 48, W - 24, 3
        pygame.draw.rect(surface, (40, 30, 20), (bar_x, bar_y, bar_w, bar_h))
        fill = int(bar_w * progress)
        if fill > 0:
            pygame.draw.rect(surface, (220, 180, 40), (bar_x, bar_y, fill, bar_h))
        for i in range(1, 3):
            mx = bar_x + bar_w * i // 3
            pygame.draw.rect(surface, (100, 80, 40), (mx - 1, bar_y - 2, 2, bar_h + 4))

    def _draw_controls(self, surface):
        ctrl = self.font_small.render("UP/Space: Pular  |  Z/X: Atacar", True, (100, 80, 60))
        surface.blit(ctrl, (12, H - 20))

    def draw_phase_banner(self, surface, phase_name, phase_idx, alpha):
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(alpha * 0.5)))
        surface.blit(overlay, (0, 0))
        title = self.font_huge.render(f"FASE {phase_idx + 1}", True, (220, 180, 40))
        sub = self.font_big.render(phase_name, True, (200, 160, 120))
        jp = self.font_sub.render("- O Caminho do Samurai -", True, (160, 120, 80))
        surface.blit(title, (W // 2 - title.get_width() // 2, H // 2 - 70))
        surface.blit(sub,   (W // 2 - sub.get_width() // 2,   H // 2))
        surface.blit(jp,    (W // 2 - jp.get_width() // 2,    H // 2 + 34))

    def draw_game_over(self, surface, score, coins):
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        title = self.font_huge.render("GAME OVER", True, (200, 40, 40))
        s1    = self.font_big.render(f"Pontos: {score:06d}", True, (220, 200, 100))
        s2    = self.font_big.render(f"Moedas: {coins}", True, (200, 180, 60))
        hint  = self.font_med.render("Pressione R para recomecar", True, (160, 140, 100))
        surface.blit(title, (W // 2 - title.get_width() // 2, H // 2 - 100))
        surface.blit(s1,    (W // 2 - s1.get_width() // 2,    H // 2))
        surface.blit(s2,    (W // 2 - s2.get_width() // 2,    H // 2 + 38))
        surface.blit(hint,  (W // 2 - hint.get_width() // 2,  H // 2 + 90))

    def draw_victory(self, surface, score, coins):
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))
        title = self.font_huge.render("VITORIA!", True, (255, 220, 50))
        sub   = self.font_big.render("O samurai conquistou todas as fases", True, (200, 180, 120))
        s1    = self.font_big.render(f"Pontos finais: {score:06d}", True, (220, 200, 100))
        s2    = self.font_big.render(f"Moedas: {coins}", True, (200, 180, 60))
        hint  = self.font_med.render("Pressione R para jogar novamente", True, (160, 140, 100))
        surface.blit(title, (W // 2 - title.get_width() // 2, H // 2 - 110))
        surface.blit(sub,   (W // 2 - sub.get_width() // 2,   H // 2 - 40))
        surface.blit(s1,    (W // 2 - s1.get_width() // 2,    H // 2 + 10))
        surface.blit(s2,    (W // 2 - s2.get_width() // 2,    H // 2 + 48))
        surface.blit(hint,  (W // 2 - hint.get_width() // 2,  H // 2 + 100))

    def draw_menu(self, surface, t):
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))
        pulse = abs(math.sin(t * 0.04))
        title_color = (
            int(200 + 55 * pulse),
            int(160 + 60 * pulse),
            int(40 + 10 * pulse),
        )
        title = self.font_huge.render("SAMURAI RUNNER", True, title_color)
        sub   = self.font_big.render("O Caminho do Samurai", True, (180, 160, 100))
        hint  = self.font_med.render("Pressione ENTER para comecar", True, (160, 140, 100))
        ctrl1 = self.font_small.render("UP / Space  --  Pular (duplo pulo)", True, (120, 100, 70))
        ctrl2 = self.font_small.render("Z ou X  --  Atacar com a katana", True, (120, 100, 70))
        ctrl3 = self.font_small.render("Desvie de inimigos, colete moedas e coracoes!", True, (120, 100, 70))
        surface.blit(title, (W // 2 - title.get_width() // 2, H // 2 - 120))
        surface.blit(sub,   (W // 2 - sub.get_width() // 2,   H // 2 - 38))
        surface.blit(hint,  (W // 2 - hint.get_width() // 2,  H // 2 + 20))
        surface.blit(ctrl1, (W // 2 - ctrl1.get_width() // 2, H // 2 + 60))
        surface.blit(ctrl2, (W // 2 - ctrl2.get_width() // 2, H // 2 + 80))
        surface.blit(ctrl3, (W // 2 - ctrl3.get_width() // 2, H // 2 + 100))
