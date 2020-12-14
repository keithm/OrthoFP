# OrthoFP

Reads a X-Plane flight plan file and uses Ortho4XP to build the tiles needed for the flight.


## INSTALLATION

Mac and Linux users already have the prerequisites installed if they have a working install of Ortho4XP.

If you use the Windows binary Ortho4XP package:
Install python making sure you tick "pip" on the first window and "Add Python to environment variables" on the last window.

Install the required libraries using the Ortho4XP instructions for Windows at the following url
https://github.com/oscarpilote/Ortho4XP/blob/master/Install_Instructions.txt

Clone the repository or download the zip file and copy the contents to the top level Ortho4XP directory.
orthofp.py will be in the top level Ortho4XP directory.
OFP_FP_Utils.py will be in the src directory.


## Usage

Open a terminal or command prompt and cd to the Otho4XP directory.
Run the script using the following options:

usage: orthofp.py [-h] [--xplane XPLANE] [--flightplan FLIGHTPLAN] [--source SOURCE] [--zl {12,13,14,15,16,17,18}] [--padding PADDING] [--basedir BASEDIR] [--osm] [--mesh] [--mask] [--dsf] [--deldsf] [--ovl] [--all]

optional arguments:
  -h, --help            show this help message and exit
  --xplane XPLANE       X-Plane installation directory
  --flightplan FLIGHTPLAN
                        Flight plan fms file. Checks current directory then x-plane "Output/FMS plans" directory if no path is included
  --source SOURCE       Source for photos e.g. BI, GO2, EUR etc
  --zl {12,13,14,15,16,17,18}
                        Zoom level for tiles
  --padding PADDING     Padding to use for tiles either side of flight plan. Integer greater than or equal to 0. Default: 0
  --basedir BASEDIR     Base directory for tiles. Must end with '/'. Default: ortho4xp/Tiles/
  --osm                 Assemble vector data
  --mesh                Triangulate 3D mesh
  --mask                Draw water masks
  --dsf                 Build imagery/DSF
  --deldsf              Delete imagery/DSF for other sources and/or zoom levels
  --ovl                 Extract overlays
  --all                 Perform all actions except deldsf