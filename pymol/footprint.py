from pymol import cmd

def contact_figure(antigen, receptor):
    """
    Calculates the contact footprint and sets up the figure styling
    on the existing objects, ready for you to orient and ray trace manually.
    USAGE: contact_figure antigen, receptor
    """
    # ── 1. Calculate contact surface ──────────────────────────────────────
    cmd.flag('ignore', 'none')
    cmd.set('dot_solvent', 1)
    cmd.set('dot_density', 3)

    cmd.create('complextemp', f"{antigen} {receptor}")
    antigen_area = cmd.get_area(antigen)
    receptor_area = cmd.get_area(receptor)
    complex_area = cmd.get_area('complextemp')
    contact_area = ((antigen_area + receptor_area) - complex_area) / 2
    cmd.delete('complextemp')

    cmd.select('contact', f"({receptor} and ({antigen} around 6))")

    with open('contactareas.txt', 'a') as f:
        f.write(f"{receptor}\t{antigen}\t{contact_area}\n")
    print(f"Global contact area between {receptor} and {antigen}: {contact_area:.2f} Å²")

    # ── 2. Set up visuals ─────────────────────────────────────────────────
    cmd.hide('everything')

    cmd.show('cartoon', receptor)
    cmd.show('surface', receptor)
    cmd.color('white', receptor)
    cmd.set('transparency', 0.25, receptor)

    cmd.show('cartoon', antigen)
    cmd.color('skyblue', antigen)

    cmd.show('surface', 'contact')
    cmd.color('red', 'contact')
    cmd.set('transparency', 0.0, 'contact')

    # ── 3. Render settings ────────────────────────────────────────────────
    cmd.bg_color('white')
    cmd.set('ray_shadows', 1)
    cmd.set('ray_opaque_background', 1)
    cmd.set('antialias', 2)
    cmd.set('ray_trace_mode', 1)
    cmd.set('ray_trace_gain', 0.1)
    cmd.set('surface_quality', 1)
    cmd.set('cartoon_fancy_helices', 1)
    cmd.set('hash_max', 1000)

    cmd.orient(receptor)
    cmd.zoom('all', buffer=5)
