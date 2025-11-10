# pymol_fig.py
# Usage in PyMOL:
#   run pymol_fig.py
#   make_figure("2vwd")  # object name in PyMOL

from pymol import cmd

def outline(obj_name):
    """
    Display a PyMOL object with surface + cartoon and set publication-quality aesthetics.
    
    Args:
        obj_name (str): Name of the object already loaded in PyMOL.
    """
    
    # Make sure object exists
    if obj_name not in cmd.get_object_list():
        print(f"Object '{obj_name}' does not exist in PyMOL.")
        return
    
    # Show cartoon for the object
    cmd.show("cartoon", obj_name)
    
    # Show surface for the object
    cmd.show("surface", obj_name)
    
    # Set transparency for surface
    cmd.set("transparency", 0.6, obj_name)
    cmd.color("gray80", obj_name)
    # Set rendering / aesthetics
    cmd.set("specular", 0)
    cmd.set("ambient", 0.4)
    cmd.set("cartoon_highlight_color", "grey")
    cmd.set("ray_trace_depth_factor", 1)
    cmd.set("ray_trace_disco_factor", 1)
    cmd.set("ray_trace_mode", 1)
    cmd.set("antialias", 2)
    cmd.set("ray_shadow", "off")
    
    # Set background color to white
    cmd.bg_color("white")
    
    # Optional: zoom onto the object
    cmd.zoom(obj_name)
    
    print(f"Figure ready")

# Register the command for interactive use
cmd.extend("outline", outline)
