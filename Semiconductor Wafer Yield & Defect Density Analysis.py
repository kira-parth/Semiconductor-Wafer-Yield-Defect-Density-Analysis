import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. PARAMETERS
# ============================================================

wafer_diameter_mm = 150       # Wafer diameter
die_width_mm = 5              # Die width
die_height_mm = 5             # Die height

defect_density_cm2 = 0.10     # Defects / cm^2

num_trials = 5000             # Monte Carlo trials
random_seed = 42

np.random.seed(random_seed)


# ============================================================
# 2. WAFER / DIE GEOMETRY
# ============================================================

wafer_radius_mm = wafer_diameter_mm / 2

# Convert wafer area from mm^2 to cm^2
wafer_area_cm2 = np.pi * wafer_radius_mm**2 / 100

# Expected number of defects
expected_defects = defect_density_cm2 * wafer_area_cm2

print("Wafer diameter:", wafer_diameter_mm, "mm")
print("Wafer area:", round(wafer_area_cm2, 2), "cm²")
print("Defect density:", defect_density_cm2, "defects/cm²")
print("Expected defects:", round(expected_defects, 2))


# ============================================================
# 3. CREATE DIE CENTERS
# ============================================================

def create_dies(wafer_diameter, die_width, die_height):

    radius = wafer_diameter / 2

    x_centers = np.arange(
        -radius + die_width/2,
        radius,
        die_width
    )

    y_centers = np.arange(
        -radius + die_height/2,
        radius,
        die_height
    )

    dies = []

    for x in x_centers:
        for y in y_centers:

            # Four corners of the die
            corners = [
                (x - die_width/2, y - die_height/2),
                (x + die_width/2, y - die_height/2),
                (x - die_width/2, y + die_height/2),
                (x + die_width/2, y + die_height/2)
            ]

            # Keep only dies whose complete area
            # lies inside the circular wafer
            inside = all(
                (cx**2 + cy**2) <= radius**2
                for cx, cy in corners
            )

            if inside:
                dies.append((x, y))

    return np.array(dies)


dies = create_dies(
    wafer_diameter_mm,
    die_width_mm,
    die_height_mm
)

total_dies = len(dies)

print("Total usable dies:", total_dies)


# ============================================================
# 4. GENERATE RANDOM DEFECT LOCATIONS
# ============================================================

def generate_defects(num_defects, wafer_diameter):

    radius = wafer_diameter / 2

    # Uniform random points inside a circle
    r = radius * np.sqrt(np.random.random(num_defects))
    theta = 2 * np.pi * np.random.random(num_defects)

    x = r * np.cos(theta)
    y = r * np.sin(theta)

    return x, y


# ============================================================
# 5. MAP DEFECTS TO DIES
# ============================================================

def calculate_yield(defect_density):

    # Poisson distribution gives the actual number
    # of defects for this Monte Carlo wafer
    num_defects = np.random.poisson(
        defect_density * wafer_area_cm2
    )

    defect_x, defect_y = generate_defects(
        num_defects,
        wafer_diameter_mm
    )

    defective_die = np.zeros(total_dies, dtype=bool)

    for dx, dy in zip(defect_x, defect_y):

        # Find die containing this defect
        distance = np.sqrt(
            (dies[:, 0] - dx)**2 +
            (dies[:, 1] - dy)**2
        )

        nearest_die = np.argmin(distance)

        die_x = dies[nearest_die, 0]
        die_y = dies[nearest_die, 1]

        # Check whether defect is actually inside
        # the rectangular die
        if (
            abs(dx - die_x) <= die_width_mm / 2
            and
            abs(dy - die_y) <= die_height_mm / 2
        ):
            defective_die[nearest_die] = True

    good_dies = np.sum(~defective_die)
    bad_dies = np.sum(defective_die)

    yield_percent = (
        good_dies / total_dies
    ) * 100

    return (
        yield_percent,
        good_dies,
        bad_dies,
        num_defects,
        defect_x,
        defect_y,
        defective_die
    )


# ============================================================
# 6. RUN ONE WAFER
# ============================================================

result = calculate_yield(defect_density_cm2)

yield_percent = result[0]
good_dies = result[1]
bad_dies = result[2]
num_defects = result[3]

print("\n--- Single Wafer Simulation ---")
print("Generated defects:", num_defects)
print("Good dies:", good_dies)
print("Bad dies:", bad_dies)
print("Yield:", round(yield_percent, 2), "%")


# ============================================================
# 7. MONTE CARLO SIMULATION
# ============================================================

def monte_carlo_yield(
    defect_density,
    trials=5000
):

    yields = []

    for _ in range(trials):

        result = calculate_yield(
            defect_density
        )

        yields.append(result[0])

    yields = np.array(yields)

    mean_yield = np.mean(yields)
    std_yield = np.std(yields)

    return yields, mean_yield, std_yield


yields, mean_yield, std_yield = monte_carlo_yield(
    defect_density_cm2,
    num_trials
)

print("\n--- Monte Carlo Result ---")
print("Trials:", num_trials)
print("Mean yield:", round(mean_yield, 3), "%")
print("Yield standard deviation:", round(std_yield, 3), "%")


# ============================================================
# 8. CONFIDENCE INTERVAL
# ============================================================

confidence_low = np.percentile(yields, 2.5)
confidence_high = np.percentile(yields, 97.5)

print(
    "95% Monte Carlo yield interval:",
    round(confidence_low, 3),
    "% -",
    round(confidence_high, 3),
    "%"
)


# ============================================================
# 9. YIELD VS DEFECT DENSITY
# ============================================================

defect_densities = np.array([
    0.01,
    0.02,
    0.05,
    0.10,
    0.20,
    0.30,
    0.50,
    0.75,
    1.00
])

mean_yields = []
std_yields = []

for density in defect_densities:

    yields, mean_y, std_y = monte_carlo_yield(
        density,
        num_trials
    )

    mean_yields.append(mean_y)
    std_yields.append(std_y)


mean_yields = np.array(mean_yields)
std_yields = np.array(std_yields)


# ============================================================
# 10. PLOT YIELD VS DEFECT DENSITY
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    defect_densities,
    mean_yields,
    marker='o'
)

plt.xlabel("Defect Density (defects/cm²)")
plt.ylabel("Mean Die Yield (%)")
plt.title("Semiconductor Wafer Yield vs Defect Density")
plt.grid(True)

plt.show()


# ============================================================
# 11. PLOT MONTE CARLO DISTRIBUTION
# ============================================================

plt.figure(figsize=(8, 5))

plt.hist(
    yields,
    bins=30
)

plt.xlabel("Wafer Yield (%)")
plt.ylabel("Number of Simulated Wafers")
plt.title(
    f"Monte Carlo Yield Distribution\n"
    f"Defect Density = {defect_densities[-1]} defects/cm²"
)

plt.grid(True)

plt.show()


# ============================================================
# 12. VISUALIZE ONE WAFER
# ============================================================

result = calculate_yield(defect_density_cm2)

defect_x = result[4]
defect_y = result[5]
defective_die = result[6]

plt.figure(figsize=(8, 8))

# Wafer boundary
wafer = plt.Circle(
    (0, 0),
    wafer_radius_mm,
    fill=False,
    linewidth=2
)

plt.gca().add_patch(wafer)

# Plot dies
for i, (x, y) in enumerate(dies):

    if defective_die[i]:
        rectangle = plt.Rectangle(
            (
                x - die_width_mm/2,
                y - die_height_mm/2
            ),
            die_width_mm,
            die_height_mm
        )
    else:
        rectangle = plt.Rectangle(
            (
                x - die_width_mm/2,
                y - die_height_mm/2
            ),
            die_width_mm,
            die_height_mm,
            fill=False
        )

    plt.gca().add_patch(rectangle)


# Defect locations
plt.scatter(
    defect_x,
    defect_y,
    s=15,
    marker='x'
)

plt.xlabel("X position (mm)")
plt.ylabel("Y position (mm)")
plt.title(
    f"Wafer Defect Map\n"
    f"Yield = {result[0]:.2f}%"
)

plt.axis("equal")
plt.grid(True)

plt.show()