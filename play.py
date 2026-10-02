"""Watch an evolved champion fly.  python play.py [condition] [--fps=60]

Replays the exact simulator (engine.trace) on unseen test levels.
SPACE / click: next level   UP / DOWN: speed   ESC: quit
"""
import os, sys, pickle
import pygame
from game import engine as E, worlds
from ga import evolve as G

args = [a for a in sys.argv[1:] if not a.startswith("--")]
cond = args[0] if args else "base"
fps = next((int(a.split("=")[1]) for a in sys.argv[1:] if a.startswith("--fps=")), 60)
path = next(p for p in (f"logs/{cond}.pkl", f"logs_shipped/{cond}.pkl") if os.path.exists(p))
pk = pickle.load(open(path, "rb"))
run = max(pk["runs"], key=lambda r: r["test"]["test_pipes"])   # best champion of the condition
champ, mode = run["champ"], pk["cfg"]["mode"]
table = worlds.table(pk["world"])
W, H = 480, int(E.H)
DEATH = {E.TRUNC: "survived all frames", E.GROUND: "hit ground", E.CEIL: "hit ceiling", E.PIPE: "hit pipe"}

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption(f"Flappy GA - {cond} (seed {run['seed']})")
font = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()
level_i = 0


def load(i):
    seed = int(G.TEST_SEEDS[i % len(G.TEST_SEEDS)])
    ty, res = E.trace(champ, seed, table, pk["cfg"]["max_frames"], mode)
    return seed, ty, res


seed, ty, res = load(level_i)
t = 0
while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
            pygame.quit(); sys.exit()
        if (ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE) or ev.type == pygame.MOUSEBUTTONDOWN:
            level_i += 1; seed, ty, res = load(level_i); t = 0
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_UP:
            fps = min(fps * 2, 1920)
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_DOWN:
            fps = max(fps // 2, 15)

    f = min(t, len(ty) - 1)
    y = ty[f]
    screen.fill((112, 197, 206))
    gaps = table[seed]
    i0 = max(0, int((E.SPEED * f - E.FIRST_X) // E.SPACING))
    for i in range(i0, min(i0 + 4, E.N_PIPES)):
        px = E.FIRST_X + E.SPACING * i - E.SPEED * f
        c, hg = gaps[i], E.GAP / 2
        pygame.draw.rect(screen, (83, 160, 44), (px, 0, E.PIPE_W, c - hg))
        pygame.draw.rect(screen, (83, 160, 44), (px, c + hg, E.PIPE_W, H - c - hg))
    pygame.draw.circle(screen, (250, 200, 40), (int(E.BIRD_X), int(y)), int(E.HALF))
    pipes = sum(E.FIRST_X + E.SPACING * i + E.PIPE_W < E.BIRD_X - E.HALF + E.SPEED * f for i in range(E.N_PIPES))
    lines = [f"level {seed}   pipes {pipes}   {fps} fps"]
    if t >= len(ty) - 1:
        lines += [f"{DEATH[int(res[2])]} - {int(res[1])} pipes", "SPACE for next level"]
    for k, s in enumerate(lines):
        screen.blit(font.render(s, True, (0, 0, 0)), (10, 10 + 26 * k))
    pygame.display.flip()
    t += 1
    clock.tick(fps)
