import matplotlib.pyplot as plt

# Example schedules (unit durations, weights w1=2, w2=3, w3=1)
jobs = [
    {"name": "Job 1", "weight": 2, "color": "#003399"},
    {"name": "Job 2", "weight": 3, "color": "#4f9d5d"},
    {"name": "Job 3", "weight": 1, "color": "#666666"},
]

schedule1 = [
    {"job": jobs[0], "machine": "A", "start": 0},
    {"job": jobs[2], "machine": "A", "start": 1},
    {"job": jobs[1], "machine": "B", "start": 0},
]

schedule2 = [
    {"job": jobs[0], "machine": "A", "start": 0},
    {"job": jobs[1], "machine": "A", "start": 1},
    {"job": jobs[2], "machine": "B", "start": 0},
]


def plot_schedule_with_cost(schedule, label, ax):
    # Map machines to y‐positions (A on top, B below)
    machines = ["A", "B"]
    y_positions = {m: idx for idx, m in enumerate(machines)}

    total_cost = 0
    for entry in schedule:
        job = entry["job"]
        job_name = job["name"]
        m = entry["machine"]
        start = entry["start"]
        w = job["weight"]
        y = y_positions[m]
        Cj = start + 1
        cost = w * Cj
        total_cost += cost
        color = job["color"]

        # Draw the horizontal bar
        ax.barh(y, 1, left=start, height=0.6, color=color)
        # Label the bar with the job name
        ax.text(start + 1 / 2, y, job_name, va="center", ha="center", color="white", fontsize=10)
        # Annotate the weighted cost above each bar
        ax.text(
            start + 1 / 2,
            y + 0.4,
            rf"${w} \cdot {Cj} = {cost}$",
            va="center", ha="center", color="black", fontsize=9
        )

    # Remove x-axis ticks and grid
    ax.set_xticks([])
    ax.grid(False)

    # Y-axis: “Machine A” then “Machine B”
    ax.set_yticks(list(y_positions.values()))
    ax.set_yticklabels([f"{m}" for m in machines])
    ax.invert_yaxis()  # so Machine A is on top
    ax.set_xlim(0, 2.2)

    ax.set_ylim(1.5, -.5)

    # Annotate total cost centered below the plot
    ax.set_title(rf"$\mathbf{{Example\ {label}.}}$ Total cost = ${total_cost}$")


# Create a figure with two stacked subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5, 8), sharex=True)

plot_schedule_with_cost(schedule1, "a", ax1)
plot_schedule_with_cost(schedule2, "b", ax2)

job_text = ",  ".join([f"{job['name']}: $w={job['weight']}$" for job in jobs])
fig.text(0.5, 0.93, job_text, ha="center", va="top", fontsize=12)

fig.suptitle("Schedule Comparison", fontsize=18)
plt.subplots_adjust(bottom=0.05, top=0.83)

# Save to PNG (for PowerPoint insertion)
fig.savefig("toy_example_gantt.png", dpi=150)
