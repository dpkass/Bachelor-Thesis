import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# Example schedule just before placing the next job
#
#  • Each tuple: (machine_name, [(job_id, weight), …])
#  • All jobs have unit processing time, so bar width = 1.
#  • ‘Load’ on a machine = Σ  weight × completion-position.
# ------------------------------------------------------------------
machines = [
    ("Machine A", [(1, 2), (3, 4)]),
    ("Machine B", [(2, 3)]),
    ("Machine C", [(4, 5), (5, 2), (6, 1)])
]

bar_h   = 0.8
gap     = 0.4
fig, ax = plt.subplots(figsize=(6, 3.5))

loads, y_ticks, y_labels = [], [], []

# ------------------------------------------------------------------
# Draw one Gantt row per machine
# ------------------------------------------------------------------
for idx, (m_name, jobs) in enumerate(machines):
    y = idx * (bar_h + gap)
    y_ticks.append(y + bar_h/2)
    y_labels.append(m_name)

    # draw bars (unit length) + annotate weights
    for pos, (job, w) in enumerate(jobs, start=1):
        x = pos - 1
        ax.broken_barh([(x, 1)], (y, bar_h), facecolors="orange")
        ax.text(x + 0.5, y + bar_h/2, rf"$w_{{{job}}}={w}$",
                ha="center", va="center", fontsize=9)

    # calculate & label cumulative load
    load = sum(w * p for p, (_, w) in enumerate(jobs, start=1))
    loads.append(load)
    ax.text(len(jobs) + 0.2, y + bar_h/2, f"Load (total cost) = {load}",
            va="center", fontsize=9)

# ------------------------------------------------------------------
# Arrow to least-loaded machine
# ------------------------------------------------------------------
least = loads.index(min(loads))
arrow_y = least * (bar_h + gap) + bar_h/2
arrow_x = len(machines[least][1]) + 1.7
ax.annotate("least loaded",
            xy=(arrow_x, arrow_y),
            xytext=(arrow_x + .7, arrow_y),
            arrowprops=dict(arrowstyle="->", lw=1.8),
            va="center")

# ------------------------------------------------------------------
# Cosmetic axes tweaks
# ------------------------------------------------------------------
ax.set_ylim(-0.2, len(machines)*(bar_h + gap))
ax.set_xlim(0, max(len(j) for _, j in machines) + 2)
ax.set_yticks(y_ticks)
ax.set_yticklabels(y_labels)
ax.set_xlabel("Job position on machine (unit time)")
# ax.set_title("Greedy: Least-Loaded")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("./least_loaded.png", dpi=150)

