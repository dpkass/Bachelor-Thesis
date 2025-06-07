import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ─────────────────────────────────────────────────────────────────────────────
# Data for 10 jobs
jobs = list(range(1, 11))
weights = [5, 1, 9, 3, 10, 2, 8, 4, 7, 6]  # J1=5, J2=1, J3=9, etc.

# Step 1: original array
orig_order = jobs.copy()

# Step 2: sort by weight descending
sorted_indices = sorted(range(len(jobs)), key=lambda i: weights[i], reverse=True)
sorted_order = [jobs[i] for i in sorted_indices]

# Step 3: split into 2 machines (5 jobs each)
machines_step3 = {
    "A": sorted_order[0:5],
    "B": sorted_order[5:10]
}

# Step 4: within each machine, sort by job ID ascending
machines_step4 = {m: sorted(machines_step3[m]) for m in machines_step3}
# ─────────────────────────────────────────────────────────────────────────────

fig = plt.figure(figsize=(14, 7))
gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1], wspace=0.4)

# ──────────────── Step 1: Original Array (Column 1) ─────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
ax1.yaxis_inverted()
ax1.set_aspect('equal')
for i, j in enumerate(orig_order):
    rect = Rectangle((0, i), 1, 1, facecolor='orange')
    ax1.add_patch(rect)
    ax1.text(0.5, i + 0.5, f"$w_{{{j}}}={weights[j - 1]}$",
             ha='center', va='center', fontsize=8)
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 10)
ax1.set_xticks([])
ax1.set_yticks(range(11))
ax1.set_title("Step 1: Original Array\n(10 jobs)", pad=10)

# ──────────────── Step 2: Sorted by Weight Descending (Column 2) ───────────
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_aspect('equal')
for i, j in enumerate(sorted_order):
    rect = Rectangle((0, i), 1, 1, facecolor='orange')
    ax2.add_patch(rect)
    ax2.text(0.5, i + 0.5, f"$w_{{{j}}}={weights[j - 1]}$",
             ha='center', va='center', fontsize=8)
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 10)
ax2.set_xticks([])
ax2.set_yticks(range(11))
ax2.set_title("Step 2: Sort by Weight\nDescending", pad=10)

# ──────────────── Steps 3 & 4 (Column 3: stacked) ─────────────────────────
inner = gs[0, 2].subgridspec(2, 1, height_ratios=[1, 1], hspace=0.4)
ax3 = fig.add_subplot(inner[0, 0])  # Step 3
ax4 = fig.add_subplot(inner[1, 0])  # Step 4

# Step 3: Reshape into 2 machines (top of column 3)
ax3.set_aspect('equal')
for idx, m in enumerate(["A", "B"]):
    jobs_m = machines_step3[m]
    x = idx  # M1 at x=0; M2 at x=1
    for i, j in enumerate(jobs_m):
        rect = Rectangle((x, i), 1, 1, facecolor='orange')
        ax3.add_patch(rect)
        ax3.text(x + 0.5, i + 0.5, f"$w_{{{j}}}={weights[j - 1]}$",
                 ha='center', va='center', fontsize=8)

# Reserve extra vertical space up to y=5.5 for the title
ax3.set_xlim(0, 2)
ax3.set_ylim(0, 5)
ax3.set_xticks([0.5, 1.5])
ax3.set_xticklabels(["A", "B"])
ax3.set_yticks(range(6))
ax3.set_title("Step 3: Reshape into 2 Machines", pad=12)

# Step 4: Sort each machine by Job ID (bottom of column 3)
ax4.set_aspect('equal')
for idx, m in enumerate(["A", "B"]):
    jobs_m = machines_step4[m]
    x = idx
    for i, j in enumerate(jobs_m):
        rect = Rectangle((x, i), 1, 1, facecolor='orange')
        ax4.add_patch(rect)
        ax4.text(x + 0.5, i + 0.5, f"$w_{{{j}}}={weights[j - 1]}$",
                 ha='center', va='center', fontsize=8)

ax4.set_xlim(0, 2)
ax4.set_ylim(0, 5)
ax4.set_xticks([0.5, 1.5])
ax4.set_xticklabels(["A", "B"])
ax4.set_yticks(range(6))
ax4.set_title("Step 4: Sort Each Machine\nby Job ID", pad=12)

for ax in [ax1, ax2, ax3, ax4]:
    ax.grid(axis='y', color='w')
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)

plt.tight_layout()
plt.savefig("sort_and_split.png")
