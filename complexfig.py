# nice_surface.py
# Usage inside PyMOL:
#   run /path/to/complexfig.py
#   complexfig 2vwd, A 

from pymol import cmd
import os

def complexfig(obj, chain_id):
    """
    Display a specified chain as surface (gray80)
    and others as cartoon (lightblue), with aesthetic settings.
    """
    # If object isn't loaded yet, fetch or load
    if not cmd.get_object_list(obj):
        if os.path.exists(obj):
            cmd.load(obj, obj)
        else:
            cmd.fetch(obj, async_=0)
            obj = obj.lower()

    # Split chains
    cmd.split_chains(obj)
    chain_obj = f"{obj}_{chain_id}"

    # Hide all
    cmd.hide("everything")

    # Show target chain as surface
    cmd.show("surface", chain_obj)
    cmd.color("gray80", chain_obj)

    # Show other chains as cartoon
    cmd.show("cartoon", f"{obj}_* and not {chain_obj}")

    # Apply nice render settings
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

    print(f"✅ Displayed {obj} with chain {chain_id} as surface.")

# Register command in PyMOL
cmd.extend("complexfig", complexfig)
