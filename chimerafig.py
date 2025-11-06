# chimerafig.cxc
# Usage in ChimeraX:
#   source https://raw.githubusercontent.com/youruser/repo/main/nice_surface.cxc
#   chimerafig <object> <chain>
# Examples:
#   chimerafig 2vwd A
#   chimerafig mystructure.cif B
#   chimerafig #1 C

from chimerax.core.commands import run
import os

def chimerafig(session, object_arg, chain_id):
    """
    Display a specified chain as surface (gray) and other chains as cartoon,
    with publication-quality aesthetics.
    Accepts:
      - object filename (e.g., mystructure.cif)
      - base name (e.g., mystructure)
      - internal ID (e.g., #1)
      - PDB ID (e.g., 2vwd)
    Automatically fetches PDBs if needed.
    """
    # --- Resolve model ---
    model = None

    # Internal ID like #1, #2
    if object_arg.startswith("#"):
        try:
            index = int(object_arg[1:]) - 1
            model = session.models.list()[index]
        except Exception:
            raise ValueError(f"Invalid model ID {object_arg}")

    # Try exact name match
    if model is None:
        models = session.models.list(name=object_arg)
        if models:
            model = models[0]

    # Try base name (without extension)
    if model is None:
        base = os.path.splitext(object_arg)[0]
        models = session.models.list(name=base)
        if models:
            model = models[0]

    # If still not found, assume PDB ID to fetch
    if model is None:
        run(session, f"open {object_arg}")
        model = session.models.list()[-1]  # newest model

    # Get the model ID string (#1, #2, etc.)
    model_id = model.id_string

    # --- Scene aesthetics ---
    run(session, "lighting soft")
    run(session, "hide atoms")
    run(session, "set bgColor #ffffff00")
    run(session, "graphics silhouettes true width 5")
    run(session, "camera ortho")

    # --- Cartoon styling ---
    run(session, "cartoon style protein modeHelix default arrows false xsection oval width 2 thickness 2")
    run(session, "cartoon suppressBackboneDisplay false")

    # --- Show all chains as cartoon first ---
    run(session, f"cartoon style protein")
    run(session, f"color lightblue protein")

    # --- Highlight selected chain as surface ---
    run(session, f"surface {model_id}:{chain_id}")
    run(session, f"color gray80 {model_id}:{chain_id}")
    run(session, f"transparency 30 {model_id}:{chain_id} surfaces")

    # --- Orient and zoom ---
    run(session, "view orient")
    run(session, "view zoom")

    # Feedback
    session.logger.info(f"Displaying figure. Example export command: save figure.png supersample 8 transparentBackground true height 2500")

# --- Register the command ---
from chimerax.core.commands import CmdDesc, register
from chimerax.core.commands import StringArg

desc = CmdDesc(required=[('object_arg', StringArg), ('chain_id', StringArg)])
register('chimerafig', desc, chimerafig)
