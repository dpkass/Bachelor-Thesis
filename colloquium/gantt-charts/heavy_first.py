import matplotlib.pyplot as plt
from bisect import bisect_left as bs

# ------------------------------------------------------------------
# Existing schedule (heaviest jobs J1…J7 already placed)
# Current job J4 has weight 1 (lightest)
# Note: valid insertion positions must keep job‐IDs in ascending order.
# ------------------------------------------------------------------
machines = [
    ("Machine A", [(1, 10), (5, 6)]),  # J1 (10), J5 (6)
    ("Machine B", [(2, 9), (3, 8), (6, 4)]),  # J2 (9), J3 (8), J6 (4)
    ("Machine C", [(7, 7)])  # J7 (7)
]

new_job_w = 1  # weight of J4
new_job_id = 4  # ID of the new job


# ---------------- helper to compute Δ‐cost and new sequence ------------------
def delta_and_state(jobs, new_job):
    """
    jobs: list of (job_id, weight), sorted by job_id
    new_job: tuple (job_id, weight)
    Returns: (delta, new_sequence)
    """
    pos = bs(jobs, new_job)
    cost_before = sum(w * (i + 1) for i, (_, w) in enumerate(jobs))
    new_seq = jobs[:pos] + [new_job] + jobs[pos:]
    cost_after = sum(w * (i + 1) for i, (_, w) in enumerate(new_seq))
    return cost_after - cost_before, new_seq, pos


# --------- find best insertion slot (minimum Δ) for each machine ----------
best_slots = [delta_and_state(jobs, (new_job_id, new_job_w)) for name, jobs in machines]

# Which machine has the smallest Δ?
global_best = min(range(len(best_slots)), key=lambda i: best_slots[i][0])

# ------------------------ plotting ----------------------------------------
bar_h, gap, gap_m = 0.35, 0.1, 0.2
fig, ax = plt.subplots(figsize=(7, 4))

for idx, (m_name, jobs) in enumerate(machines):
    y_top = -idx * (2 * bar_h + gap + gap_m)  # “before” row
    y_bot = y_top - (bar_h + gap)  # “after” row

    Δ, new_seq, ins_pos = best_slots[idx]

    # ----- BEFORE bars (current sequence) -----
    for i, (job_id, w) in enumerate(jobs):
        ax.broken_barh([(i, 1)], (y_top, bar_h), facecolors="orange")
        ax.text(i + 0.5, y_top + bar_h / 2,
                rf"$w_{{{job_id}}}$={w}",
                ha='center', va='center', fontsize=8)

    # ----- AFTER bars (best insertion for J4) -----
    for i, (job_id, w) in enumerate(new_seq):
        if (i == ins_pos) and (job_id == new_job_id):
            ax.broken_barh(
                [(i, 1)], (y_bot, bar_h),
                facecolors="none", edgecolors="orange",
                hatch="////", lw=1.5
            )
            ax.text(i + 0.5, y_bot + bar_h / 2,
                    rf"$w_{{{job_id}}}$={w}",
                    ha='center', va='center', fontsize=8)
        else:
            ax.broken_barh([(i, 1)], (y_bot, bar_h), facecolors="orange")
            ax.text(i + 0.5, y_bot + bar_h / 2,
                    rf"$w_{{{job_id}}}$={w}",
                    ha='center', va='center', fontsize=8)

    # annotate Δ‐cost on the right
    ax.text(len(new_seq) + 0.2, y_bot + bar_h / 2,
            f"Δ = {Δ}", va='center', fontsize=9)

    # draw arrow to the globally chosen slot
    if idx == global_best:
        ax.annotate("chosen slot",
                    xy=(ins_pos + 0.5, y_bot - 0.1),
                    xytext=(ins_pos + 0.5, y_bot - 0.5),
                    arrowprops=dict(arrowstyle="->", lw=1.8),
                    ha='center')

# ----- Axes & cosmetics -----
ax.set_xlim(0, max(len(seq) for _, seq, _ in best_slots) + 1)
ax.set_xlabel("Position in machine timeline (unit time)")
ax.set_title(f"Inserting Job {new_job_id} ($w_{new_job_id}={new_job_w}$)", loc='right', fontsize=10)
ax.set_yticks(
    [-(i * (2 * bar_h + gap + gap_m) + gap / 2)
     for i in range(len(machines))]
)
ax.set_yticklabels([name for name, _ in machines])
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_xticks(range(
    0, max(len(seq) for _, seq, _ in best_slots) + 1
))
plt.tight_layout()
plt.savefig("heavy_first.png", dpi=150)
