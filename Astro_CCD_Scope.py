from datetime import datetime
from zoneinfo import ZoneInfo

from starplot import OpticPlot, DSO, Observer, _
from starplot.callables import color_by_bv
from starplot.models import Refractor, Camera
from starplot.styles import PlotStyle, extensions
from Ccd import AstroCamera
from Scope import AstroScope
from Target import AstroTarget

import argparse
import sys

def to_lower(value: str) -> str:
    return value.lower()

def to_upper(value: str) -> str:
    return value.upper()

def no_space(value:str) -> str:
    return value.strip()

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Camera + Scope command-line interface"
    )

    # Required arguments
    parser.add_argument(
        "-c", "--camera",
        type=to_lower,
        required=False,
        help="Camera name (converted to lowercase)"
    )

    parser.add_argument(
        "-s", "--scope",
        type=to_upper,
        required=False,
        help="Scope name (converted to UPPERCASE)"
    )
    
    parser.add_argument(
        "-t", "--target",
        type=no_space,
        required=False,
        help="Target grouo name (converted to UPPERCASE)"
    )

    # Listing options
    parser.add_argument(
        "--list-cameras",
        action="store_true",
        help="List all supported cameras"
    )

    parser.add_argument(
        "--list-scopes",
        action="store_true",
        help="List all supported scopes"
    )
    
    parser.add_argument(
        "--list-targets",
        action="store_true",
        help="List all supported target groups"
    )

    return parser


def check_main()->Optinal(_ccd,_scope,_target):
    parser = build_parser()
    args = parser.parse_args()
    _AC=AstroCamera()
    _AS=AstroScope()
    _AT=AstroTarget()

    # Handle listing mode first (no required args)
    if args.list_cameras:
        print("Available Cameras:")
        _AC.dump()
        sys.exit(0)

    if args.list_scopes:
        print("Available Scopes:")
        _AS.dump()
        sys.exit(0)
    
    if args.list_targets:
        print("Available Targets:")
        _AT.dump()
        sys.exit(0)

    # Now enforce required parameters if not listing
    if not args.camera or not args.scope or not args.target :
        parser.error("Both --camera, --scope and --target are required unless listing.")

    # Normal operation

    # Need To get the Camera first
    print(f"Looking up Camera = {args.camera}")
    camera = _AC.find(args.camera)
    if camera:
        print(f"✔ Camera {args.camera} found")
    else:
        print(f"✖ Camera {args.camera} not found please --list-cameras and try check spelling.")
        exit(0)

    print(f"Scope  = {args.scope}")
    scope = _AS.find(args.scope)
    if scope:
        print(f"✔ Scope {args.scope} found")
    else:
        print(f"✖ Scope {args.scope} not found please --list-scopes and try check spelling.")
        exit(0)
    
    print(f"Target  = {args.target}")
    target= _AT.find(args.target)
    if target:
        print(f"✔ Target {args.target} found")
    else:
        print(f"✖ Target {args.target} not found please --list-targets try check spelling.")
        exit(0)
    return camera,scope, target



if __name__ == "__main__":
    camera,scope,target=check_main()


#################### Your Observing Definitions ###################
#
# Define the Main criteria for your observing place, and target list
#

dt = datetime(2025, 11, 16, 21, 0, 0, tzinfo=ZoneInfo("Asia/Manila"))

observer = Observer(
    dt=dt,
    lat=15.2,
    lon=118.2,
)

#################### SKY Clarity/Limit Definitions ###################
#
# These are the limits that you will see in the simulation. Alter as you need
# My sky is aprox Bortle 4 - So Stars with naked eye are 6.1-7.0 - as a guide/guess add +5 with a scope
# Adjust/alter as you see fit
#
STAR_LIMIT = 6.1 + 5.0
DSO_LIMIT = 4.1 + 5.0

OPTIC_LENSE_STR = scope.name

OPTIC_CAMERA = Camera(
    sensor_height=camera.height, sensor_width=camera.width,
    lens_focal_length=scope.focal_length, rotation=0
) 
OPTIC_CAMERA_STR = camera.name

#################### Map Style Definitions ###################

#
# Map Style - again you can alter as you see fit
#

style = PlotStyle().extend(
    extensions.BLUE_LIGHT,
    extensions.MAP,
    {
        "legend": {
            "location": "lower right",  # show legend inside map
            "num_columns": 3,
            "background_alpha": 1,
        },
    },
)

print("\n\nStarting simulation using")
print(f"Scope  {scope.name}")
print(f"Camera {camera.name}")
print(f"Target {target.name}")
print("")
for t in target.dso:
    common_name, desc = t.split("-")
    desc = desc.strip()
    common_name = common_name.replace(" ", "")
    if common_name.startswith("M"):
        messier = common_name.replace("M", "")
        try:
            obj = DSO.get(m=messier)
        except ValueError:
            print(f"✖ Object {common_name} has multiple definitions")
    else:
        obj = DSO.get(name=common_name)
    if obj:
        print(f"✔ Found {common_name}")
        try:
            p = OpticPlot(
                ra=obj.ra,
                dec=obj.dec,
                observer=observer,
                optic=OPTIC_CAMERA,
                style=style,
                resolution=2600,
                # scale=0.5,
                autoscale=True,
                raise_on_below_horizon=False,
            )
            p.stars(
                where=[_.magnitude < STAR_LIMIT], color_fn=color_by_bv, bayer_labels=True
            )
            p.dsos(where=[_.magnitude < DSO_LIMIT], where_labels=[False])
            p.info()
            p.export(
                f"{OPTIC_LENSE_STR}_{OPTIC_CAMERA_STR}_{common_name}_{desc}.png",
                padding=0.1,
                transparent=True,
            )
        except ValueError:
            print(f"✖ Sorry. Field of View too large to compute")

    else:
        print(f"✖ Found {common_name}")
