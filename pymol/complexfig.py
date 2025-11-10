from pymol import cmd
import os

def complexfig(obj, chain_ids):
    """
    Display specified chain(s) as surface (gray80),
    others as cartoon (lightblue), with nice render settings.
    Accepts a single chain ('A') or multiple chains as a comma-separated string ('A,D').
    """

    # Remove quotes if user included them
    chain_ids = chain_ids.replace('"', '').replace("'", "")
    target_chains = [c.strip() for c in chain_ids.split(",")]

    # Load object if not already loaded
    if not cmd.get_object_list(obj):
        if os.path.exists(obj):
            cmd.load(obj, obj)
        else:
            cmd.fetch(obj, async_=0)
            obj = obj.lower()

    # Split chains internally
    cmd.split_chains(obj)

    # Hide all first
    cmd.hide("everything")

    # Show target chains as surface
    for c in target_chains:
        chain_obj = f"{obj}_{c}"
        cmd.show("surface", chain_obj)
        cmd.color("gray80", chain_obj)

    # Show all other chains as cartoon
    others = " or ".join([f"{obj}_{c}" for c in cmd.get_chains(obj) if c not in target_chains])
    if others:
        cmd.show("cartoon", others)
        cmd.color("lightblue", others)

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

    print(f"Displaying {obj} with chains {', '.join(target_chains)}")

# Register command in PyMOL
cmd.extend("complexfig", complexfig)
