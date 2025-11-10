# Easy figure making

Scripts for PyMOL or ChimeraX

## Installation (PyMOL)
For PyMOL, installation does NOT require downloading this repository. Instead, click on Plugins -> Plugin Manager -> Install New Plugin and you will see a URL option. 
Simply paste the URL of the script you want to use in and it's ready. 

I also recommend downloading this script https://raw.githubusercontent.com/cbalbin-bio/pymol-color-alphafold/master/coloraf.py while you're at it.

## Usage

The PyMOL commands are straightforward:
```
complexfig object_name, antigen_chain_id (this will remain in a surface view. use quotation marks if there are multiple antigen chains e.g "A,B") 
outline object_name
```

ChimeraX is a little more complicated. You will have to download the script and place it in a desired working directory for ChimeraX. Then:
```
runscript /path/to/cxfig.cxc <model_name> <antigen_chain> <idnumber>
```

I recommend setting a new id number for each model.
