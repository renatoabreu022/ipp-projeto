import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
 
# ── MUDA AQUI O NOME DO FICHEIRO ───────────────────────────────────────────────
FICHEIRO = "grafo_braga.json"
# ──────────────────────────────────────────────────────────────────────────────
 
PALETTE = [
    "#1a78c2", "#e63946", "#f4a261", "#6a4c93",
    "#2a9d8f", "#8d99ae", "#57cc99", "#e9c46a",
]
 
with open(FICHEIRO, encoding="utf-8") as f:
    dados = json.load(f)
 
G = nx.DiGraph()
for origem, vizinhos in dados["adjacencias"].items():
    for v in vizinhos:
        G.add_edge(origem, v["destino"], weight=v["distancia"])
 
# Posições: coordenadas reais se existirem, senão layout automático
coords = dados.get("coordenadas", {})
if all(n in coords for n in G.nodes()):
    lats = [coords[n][0] for n in G.nodes()]
    lons = [coords[n][1] for n in G.nodes()]
    pos = {
        n: (
            (coords[n][1] - min(lons)) / (max(lons) - min(lons) or 1),
            (coords[n][0] - min(lats)) / (max(lats) - min(lats) or 1),
        )
        for n in G.nodes()
    }
else:
    pos = nx.spring_layout(G, seed=42)
 
nodes = list(G.nodes())
node_colors = [PALETTE[i % len(PALETTE)] for i, n in enumerate(nodes)]
 
edge_weights = [G[u][v]["weight"] for u, v in G.edges()] or [1]
max_w, min_w = max(edge_weights), min(edge_weights)
rng = max_w - min_w or 1
 
fig, ax = plt.subplots(figsize=(12, 8))
fig.patch.set_facecolor("#0d1117")
ax.set_facecolor("#0d1117")
 
for u, v in G.edges():
    w = G[u][v]["weight"]
    ax.annotate("", xy=pos[v], xytext=pos[u],
                arrowprops=dict(
                    arrowstyle="-|>",
                    color="#4fc3f7",
                    alpha=0.3 + 0.5 * ((w - min_w) / rng),
                    lw=0.8 + 3.0 * ((w - min_w) / rng),
                    connectionstyle="arc3,rad=0.12"
                ))
 
nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors,
                       node_size=700, alpha=0.95,
                       linewidths=1.8, edgecolors="white")
 
short = {n: (n[:12] + "…" if len(n) > 14 else n) for n in nodes}
nx.draw_networkx_labels(G, pos, labels=short, ax=ax,
                        font_size=8, font_color="white", font_weight="bold")
 
edge_labels = {(u, v): f"{G[u][v]['weight']*1000:.0f}m" for u, v in G.edges()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax,
                             font_size=6, font_color="#adb5bd",
                             bbox=dict(boxstyle="round,pad=0.1",
                                       fc="#0d1117", ec="none", alpha=0.7),
                             label_pos=0.35)
 
color_map = {n: PALETTE[i % len(PALETTE)] for i, n in enumerate(nodes)}
patches = [mpatches.Patch(color=color_map[n], label=n) for n in nodes]
ax.legend(handles=patches, loc="upper right", framealpha=0.15,
          facecolor="#1e2533", edgecolor="#4fc3f7",
          labelcolor="white", fontsize=8)
 
ax.set_title(FICHEIRO, color="white", fontsize=13, fontweight="bold")
ax.axis("off")
plt.tight_layout()
plt.show()