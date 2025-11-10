from pymol import cmd
import os

def complexfig(obj, chain_ids):
    """
    Display specified chain(s) as surface (gray80),
    all other chains as cartoon (lightblue), with nice render settings.
    Accepts a single chain ('A') or multiple chains as a comma-separated string ('A,D').
    """

    # Clean up input string and split chains
    chain_ids = chain_ids.replace('"', '').replace("'", "")
    target_chains = [c.strip() for c in chain_ids.split(",")]

    # Load object if not already loaded
    if not cmd.get_object_list(obj):
        if os.path.exists(obj):
            cmd.load(obj, obj)
        else:
            cmd.fetch(obj, async_=0)
            obj = obj.lower()

    # Hide everything first
    cmd.hide("everything", obj)

    # Show target chains as surface
    for c in target_chains:
        cmd.show("surface", f"{obj} and chain {c}")
        cmd.color("gray80", f"{obj} and chain {c}")

    # Show all other chains as cartoon
    all_chains = cmd.get_chains(obj)
    other_chains = [c for c in all_chains if c not in target_chains]

    if other_chains:
        others_selection = " or ".join([f"{obj} and chain {c}" for c in other_chains])
        cmd.show("cartoon", others_selection)
        cmd.color("lightblue", others_selection)

    # Render settings
    cmd.set("ambient_occlusion_mode", 1)
    cmd.set("specular", 0)
    cmd.set("ambient", 0.4)
    cmd.set("cartoon_highlight_color", "grey")
    cmd.set("ray_trace_depth_factor", 1)
    cmd.set("ray_trace_disco_factor", 1)
    cmd.set("ray_trace_mode", 1)
    cmd.set("antialias", 2)
    cmd.set("ray_shadow", "off")
    cmd.bg_color("white")

    cmd.orient()
    cmd.zoom("all")
    cmd.split_chains(obj)

# Register command in PyMOL
cmd.extend("complexfig", complexfig)
