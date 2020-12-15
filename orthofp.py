#!/usr/bin/env python3
import sys
import os
import argparse
import warnings
Ortho4XP_dir='..' if getattr(sys,'frozen',False) else '.'
sys.path.append(os.path.join(Ortho4XP_dir,'src'))


warnings.filterwarnings("ignore", category=FutureWarning)

import O4_File_Names as FNAMES
sys.path.append(FNAMES.Provider_dir)
import O4_Imagery_Utils as IMG
import O4_Vector_Map as VMAP
import O4_Mesh_Utils as MESH
import O4_Mask_Utils as MASK
import O4_Tile_Utils as TILE
import O4_DSF_Utils as DSF
import O4_Overlay_Utils as OVL
import O4_Config_Utils as CFG  # CFG imported last because it can modify other modules variables
import OFP_FP_Utils as FP

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Reads a X-Plane flight plan file and uses Ortho4XP to build the tiles needed for the flight.", epilog="Each action is only performed if the tile doesn't exist or the --force option is used.")
    parser.add_argument("--xplane", help="X-Plane installation directory")
    parser.add_argument("--flightplan", help="Flight plan fms file. Checks current directory then x-plane \"Output/FMS plans\" directory if no path is included")
    parser.add_argument("--source", help="Source for photos e.g. BI, GO2, EUR etc")
    parser.add_argument("--zl", help="Zoom level for tiles", type=int, choices=[12, 13, 14, 15, 16, 17, 18])
    parser.add_argument("--padding", help="Padding to use for tiles either side of flight plan. Integer greater than or equal to 0. Default: 0", type=int, default=0)
    parser.add_argument("--basedir", help="Base directory for tiles. Must end with '/'. Default: ortho4xp/Tiles/", default='')
    parser.add_argument("--osm", help="Assemble vector data", action="store_true")
    parser.add_argument("--mesh", help="Triangulate 3D mesh", action="store_true")
    parser.add_argument("--mask", help="Draw water masks", action="store_true")
    parser.add_argument("--dsf", help="Build imagery/DSF", action="store_true")
    parser.add_argument("--deldsf", help="Delete imagery/DSF for other sources and/or zoom levels", action="store_true")
    parser.add_argument("--ovl", help="Extract overlays", action="store_true")
    parser.add_argument("--all", help="Perform all actions except deldsf", action="store_true")
    parser.add_argument("--force", help="Perform the selected actions even if the tile exists", action="store_true")

    args = parser.parse_args()

    if not os.path.isdir(FNAMES.Utils_dir):
        print("Missing ",FNAMES.Utils_dir,"directory, check your install. Exiting.")
        sys.exit()   
    for directory in (FNAMES.Preview_dir, FNAMES.Provider_dir, FNAMES.Extent_dir, FNAMES.Filter_dir, FNAMES.OSM_dir,
                      FNAMES.Mask_dir,FNAMES.Imagery_dir,FNAMES.Elevation_dir,FNAMES.Geotiff_dir,FNAMES.Patch_dir,
                      FNAMES.Tile_dir,FNAMES.Tmp_dir):
        if not os.path.isdir(directory):
            try: 
                os.makedirs(directory)
                print("Creating missing directory",directory)
            except: 
                print("Could not create required directory",directory,". Exit.")
                sys.exit()
    IMG.initialize_extents_dict()
    IMG.initialize_color_filters_dict()
    IMG.initialize_providers_dict()
    IMG.initialize_combined_providers_dict()

    if args.source not in IMG.providers_dict.keys():
        print("Error: %s not a valid source" % args.source)
        parser.print_help()
        exit(1)
    
    if args.padding < 0:
        print("Error: %d is less than 0" % args.padding)
        parser.print_help()
        exit(1)

    if not args.flightplan:
       print("Error: Flight plan file is required")
       parser.print_help()
       exit(1)

    if not args.zl:
       print("Error: Zoom level is required")
       parser.print_help()
       exit(1)

    if os.path.isfile(args.flightplan):
        fpfile = args.flightplan
        print(fpfile)
    elif args.xplane is not None and os.path.isfile(os.path.join(args.xplane, "Output", "FMS plans", args.flightplan)): 
        fpfile = os.path.join(args.xplane, "Output", "FMS plans", args.flightplan)
        print(fpfile)
    else:
        print("Error: Cannot find flight plan ", args.flightplan)
        exit(1)

    fp = FP.FlightPlan(fpfile)
    coords = fp.getCoords(args.padding)
    for idx, coord in enumerate(coords, start=1):
        print("Building tile " + str(idx) + " of " + str(len(coords)))
        lat=coord[0]
        lon=coord[1]
        tile=CFG.Tile(lat,lon,args.basedir)
        tile.default_website=args.source
        tile.default_zl=args.zl
        if not os.path.isfile(os.path.join(tile.build_dir,'Earth nav data',FNAMES.long_latlon(tile.lat,tile.lon)+'.dsf')) or args.force:
            if (args.osm or args.mesh or args.mask or args.dsf or args.ovl or args.all): tile.make_dirs()
            if args.osm or args.all:
                VMAP.build_poly_file(tile)
            if args.mesh or args.all:
                MESH.build_mesh(tile)
            if args.mask or args.all:
                MASK.build_masks(tile)
            if args.dsf or args.all:
                TILE.build_tile(tile)
            if args.deldsf:
                TILE.remove_unwanted_textures(tile)
        if (args.ovl or args.all) and (not os.path.isfile(os.path.join(FNAMES.Overlay_dir,"Earth nav data",FNAMES.round_latlon(tile.lat,tile.lon),FNAMES.short_latlon(tile.lat,tile.lon)+'.dsf')) or args.force):
            OVL.build_overlay(coord[0],coord[1])
