from pymol import cmd, util

def electropot(obj_name):
    """
    Generate electrostatic potential surface for a given object
    with aesthetic settings applied.
    
    Usage:
        electropot <object_name>
    """
    if not cmd.object_exists(obj_name):
        print(f"[ERROR] Object '{obj_name}' not found in session.")
        return

    # Run electrostatic potential
    util.protein_vacuum_esp(obj_name, mode=2, quiet=0, _self=cmd)

    # Apply aesthetic settings
    cmd.space("cmyk")
    cmd.set("ray_trace_mode", 1)
    cmd.set("specular", 0)
    cmd.set("ambient", 0.4)
    cmd.bg_color("white")

    print(f"[DONE] Electrostatic potential applied to '{obj_name}'.")

# Register as a PyMOL command
cmd.extend("electropot", electropot)
