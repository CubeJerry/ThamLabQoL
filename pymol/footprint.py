from pymol import cmd

def contact_figure(antigen, receptor):
    """
    Calculates the contact footprint and sets up the figure styling
    on the existing objects, ready for you to orient and ray trace manually.
    USAGE: footprint receptor, antigen
    """
    # ── 1. Calculate contact surface ──────────────────────────────────────
    cmd.flag('ignore', 'none')
    cmd.set('dot_solvent', 1)
    cmd.set('dot_density', 3)

    cmd.create('complextemp', "{} {}".format(antigen, receptor))
    antigen_area = cmd.get_area(antigen)
    receptor_area = cmd.get_area(receptor)
    complex_area = cmd.get_area('complextemp')
    contact_area = ((antigen_area + receptor_area) - complex_area) / 2
    cmd.delete('complextemp')

    cmd.select('contact', "({} and ({} around 6))".format(receptor, antigen))

    with open('contactareas.txt', 'a') as f:
        f.write("{}\t{}\t{}\n".format(receptor, antigen, contact_area))
    print("Global contact area between {} and {}: {:.2f} Å²".format(receptor, antigen, contact_area))

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
    cmd.set('hash_max', 2000)
    cmd.set('ambient_occlusion_mode', 1)
    cmd.set('ambient', 0.3)



    cmd.orient(antigen)
    cmd.zoom('all', buffer=5)

cmd.extend("footprint", contact_figure)
