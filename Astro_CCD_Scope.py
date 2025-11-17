from datetime import datetime
from zoneinfo import ZoneInfo

from starplot import OpticPlot, DSO, Observer, _
from starplot.callables import color_by_bv
from starplot.models import Refractor, Camera
from starplot.styles import PlotStyle, extensions

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

#################### LENSE Definitions ###################
#
# Some Entry Wide Field lenses you may be considering
# Please add as many as you like
SV555 = 243
REDCAT51 = 250
ASKAR71 = 490

#
# Set the Lense (See Above) to the OPTIC_LENSE
#
OPTIC_LENSE = SV555
OPTIC_LENSE_STR = "SV555"
#################### CAMERA Definitions ###################

#
# Camera to simulate. Again - adjust to your preference. But I suggest creating a new Name per Camera
# It will help to minimize simple and difficult to spot mistakes.
# Please NOTE. You tell the Camera which OPTIC_LENSE you are using also.
#

imx585 = Camera(
    sensor_height=6.26, sensor_width=11.14, lens_focal_length=OPTIC_LENSE, rotation=0
)

# Used in ASI 533 Pro. Square Sensor
imx533 = Camera(
    sensor_height=11.31, sensor_width=11.31, lens_focal_length=OPTIC_LENSE, rotation=0
)
asi12600 = Camera(
sensor_height=23.5, sensor_width=15.7, lens_focal_length=OPTIC_LENSE, rotation=0
)
#
# Set the Camera (See Above) to the OPTIC_CAMERA
#
OPTIC_CAMERA = imx585
OPTIC_CAMERA_STR = "imx585"

#################### TARGET Definitions ###################
#
# A Genieric "top 20" of DSO's - again edit/Adjust but we need to make sure there is a SPACE HYPHEN SPACE Description
# NGC Needs 4 numbers including leading 0's
#
TARGET_LIST = deep_sky_objects = [
    "M31 - Andromeda Galaxy",
    "M42 - Orion Nebula",
    "M45 - Pleiades",
    "M13 - Hercules Globular Cluster",
    "M51 - Whirlpool Galaxy",
    "M81 - Bode's Galaxy",
    "M82 - Cigar Galaxy",
    "M33 - Triangulum Galaxy",
    "M101 - Pinwheel Galaxy",
    "M57 - Ring Nebula",
    "M27 - Dumbbell Nebula",
    "NGC 7000 - North America Nebula",
    "NGC 0253 - Sculptor Galaxy",
    "NGC 0869 - Double Cluster",
    "M104 - Sombrero Galaxy",
    "M20 - Trifid Nebula",
    "M8 - Lagoon Nebula",
    "M17 - Swan (Omega) Nebula",
    "M4 - Globular Cluster in Scorpius",
    "M87 - Virgo A Galaxy",
]

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
print(f"Scope  {OPTIC_LENSE_STR}")
print(f"Camera {OPTIC_CAMERA_STR}")
print("")
for t in TARGET_LIST:
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
    else:
        print(f"✖ Found {common_name}")
