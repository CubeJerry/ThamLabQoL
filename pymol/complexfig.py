from pymol import cmd
import os

def complexfig(obj, chain_ids):
    """
    Display specified chain(s) as surface (gray80)
    and others as cartoon (lightblue), with aesthetic settings.
    
    chain_ids: str, comma-separated chain letters, e.g., "A,B"
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

    # Parse target chains
    target_chains = [c.strip() for c in chain_ids.split(",")]
    target_selection = " or ".join([f"{obj}_{c}" for c in target_chains])

    # Hide all
    cmd.hide("everything")

    # Show target chains as surface
    cmd.show("surface", target_selection)
    cmd.color("gray80", target_selection)

    # Show other chains as cartoon
    other_selection = f"{obj}_* and not ({target_selection})"
    cmd.show("cartoon", other_selection)
    cmd.color("lightblue", other_selection)

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

    print(f"Displaying figure for chains: {', '.join(target_chains)}")

# Register command in PyMOL
cmd.extend("complexfig", complexfig)
