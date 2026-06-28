# Samurai Runner

Jogo de plataforma 2D com parallax de cenário japonês feudal.

## Instalação local

```bash
pip install pygame
python main.py
```

## Deploy no Netlify (via pygbag)

```bash
pip install pygbag
python -m pygbag main.py
```

Isso gera a pasta `build/web/`. Suba essa pasta no Netlify como site estático.

## Controles

| Tecla         | Acao                        |
|---------------|-----------------------------|
| UP / Espaco   | Pular (duplo pulo)          |
| Z ou X        | Atacar com a katana         |
| R             | Recomecar (game over)       |
| Enter         | Iniciar (menu)              |

## Mecanicas

- **3 fases** com dificuldade crescente (velocidade e taxa de inimigos)
- **Duplo pulo** para desviar de obstaculos
- **Ataque com katana** elimina ninjas (+150 pts)
- **Moedas** flutuantes (+50 pts cada)
- **Coracao de cura** raro — restaura 1 HP ao coletar
- **Obstaculos** nao causam dano, apenas penalidade de -100 pts
- **Invencibilidade** apos levar dano (pisca); 2s na fase 3
- **Barra de progresso** da fase no topo da tela

## Fases

| # | Nome               | Velocidade | Inimigo     | Obstaculo   |
|---|--------------------|-----------|-------------|-------------|
| 1 | Floresta Sagrada   | 4.0       | 1 a cada 2s | 1 a cada 1.5s |
| 2 | Templo das Sombras | 5.5       | 1 a cada 1.3s | 1 a cada 1s |
| 3 | Montanha do Dragao | 7.0       | 1 a cada 0.9s | 1 a cada 0.75s |

## Estrutura

```
samurai_runner/
├── main.py           # Entry point (loop async para pygbag)
├── requirements.txt
└── src/
    ├── settings.py   # Constantes e configuracao de fases
    ├── background.py # Parallax com 5 camadas
    ├── player.py     # Samurai com animacoes
    ├── entities.py   # Ninja, obstaculos, moedas, coracoes
    ├── hud.py        # Interface (HP, score, fases)
    └── game.py       # Estado do jogo e colisoes
```

## Como estender

- Novas fases: adicione entradas em `settings.py > PHASES`
- Novos obstaculos: adicione tipos em `entities.py > Obstacle.TYPES`
- Novos power-ups: siga o padrao de `Heart` em `entities.py`
- Chefe de fase: crie classe `Boss` com HP multiplo
