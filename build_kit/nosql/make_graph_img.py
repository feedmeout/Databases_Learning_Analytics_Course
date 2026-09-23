# Forum reply network for NoSQL Evening 1, Part 2 (invented example) -> ../img_n1p2/forum_graph.png
import os, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
H = os.path.dirname(os.path.abspath(__file__))
plt.rcParams['font.family'] = 'DejaVu Sans'
K = 4 / 3
pos = {n: (x * K, y) for n, (x, y) in {'Μαρία': (0.50, 0.52), 'Νίκος': (0.16, 0.80), 'Ελένη': (0.84, 0.80), 'Άννα': (0.84, 0.20),
       'Γιώργος': (0.16, 0.20), 'Κώστας': (0.50, 0.06)}.items()}
edges = [('Νίκος', 'Μαρία', 4), ('Ελένη', 'Μαρία', 3), ('Άννα', 'Μαρία', 2), ('Γιώργος', 'Νίκος', 2), ('Μαρία', 'Ελένη', 1)]
fig = plt.figure(figsize=(9.6, 7.2), dpi=150); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(-0.02 * K, 1.02 * K); ax.set_ylim(-0.06, 0.98); ax.set_aspect('equal'); ax.axis('off')
R = 0.105
DEEP, INK, MIST, AMB, MUTED = '#0D47A1', '#12233F', '#DCE6F5', '#F2A413', '#55657C'
for a, b, w in edges:
    (x1, y1), (x2, y2) = pos[a], pos[b]
    rad = 0.18 if {a, b} == {'Μαρία', 'Ελένη'} else 0.0
    ar = FancyArrowPatch((x1, y1), (x2, y2), connectionstyle=f'arc3,rad={rad}', arrowstyle='-|>,head_length=14,head_width=8',
                         lw=1.6 + 1.3 * w, color=MUTED, shrinkA=58, shrinkB=62, zorder=1)
    ax.add_patch(ar)
    mx, my = (x1 + x2) / 2 + 0.5 * rad * (y2 - y1), (y1 + y2) / 2 - 0.5 * rad * (x2 - x1)
    ax.text(mx, my, str(w), ha='center', va='center', fontsize=22, fontweight='bold', color=INK,
            bbox=dict(boxstyle='round,pad=0.28', fc='white', ec=MUTED, lw=1.2), zorder=3)
for n, (x, y) in pos.items():
    central = n == 'Μαρία'; iso = n == 'Κώστας'
    ax.add_patch(Circle((x, y), R * (1.25 if central else 1), fc=DEEP if central else ('white' if iso else MIST),
                        ec=AMB if iso else DEEP, lw=3.5 if iso else 2, ls='--' if iso else '-', zorder=2))
    ax.text(x, y, n, ha='center', va='center', fontsize=21, fontweight='bold', color='white' if central else INK, zorder=4)
fig.savefig(os.path.join(H, '..', 'img_n1p2', 'forum_graph.png'), facecolor='white')
print('ok')
