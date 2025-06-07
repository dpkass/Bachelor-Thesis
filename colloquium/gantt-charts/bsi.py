import matplotlib.pyplot as plt

# ------------------------- BSI Data -------------------------
iter1 = [
    ("Heavy lane",  [(3, 20), (5, 18)]),
    ("Medium lane", [(4, 16), (7, 12), (10, 17)]),
    ("Light lane",  [(1, 11), (2, 8), (8, 9), (9, 10)]),
]
iter1_left = [(6, 5), (11, 7), (12, 2)]

iter2 = [
    ("Heavy lane",  [(3, 20), (5, 18), (10, 17)]),
    ("Medium lane", [(1, 11), (4, 16), (7, 12), (9, 10)]),
    ("Light lane",  [(2, 8), (6, 5), (8, 9), (11, 7), (12, 2)])
]

def lane_cost(jobs):
    """Σ weight × completion-position."""
    return sum(w * (i + 1) for i, (_, w) in enumerate(jobs))

def job_str(job):
    id, w = job
    return f"[{id}, $w={w}$]"

costs1 = [lane_cost(jobs) for _, jobs in iter1]
costs2 = [lane_cost(jobs) for _, jobs in iter2]

# ------------------------- Helper -------------------------
def plot_iteration(iter_data, costs, filename, left=None):
    fig, ax = plt.subplots(figsize=(8, 5))
    bar_h, gap = 0.8, 0.4
    y_ticks, y_labels = [], []

    for idx, (lane, jobs) in enumerate(iter_data):
        y = idx * (bar_h + gap)
        y_ticks.append(y + bar_h / 2)
        y_labels.append(lane)

        for pos, (job, w) in enumerate(jobs, start=1):
            x = pos - 1
            ax.broken_barh([(x, 1)], (y, bar_h), facecolors="orange")
            ax.text(x + 0.5, y + bar_h / 2,
                    rf"$w_{{{job}}}={w}$",
                    ha="center", va="center", fontsize=9)
        ax.text(len(jobs) + 0.2, y + bar_h / 2,
                f"Cost = {costs[idx]}",
                va="center", fontsize=9)

    ax.set_ylim(-0.2, len(iter_data) * (bar_h + gap))
    ax.set_xlim(0, max(len(j) for _, j in iter_data) + 2)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    if left:
        fig.text(0.8, 0.05, f"Jobs left: {', '.join(map(job_str, left))}", ha="center", va="top", fontsize=10)
    
    plt.subplots_adjust(bottom=.15)
    plt.savefig(filename)

# ------------------------- Draw Figures -------------------------
plot_iteration(iter1, costs1, "./bsi_iter1", iter1_left)
plot_iteration(iter2, costs2, "./bsi_iter2")
