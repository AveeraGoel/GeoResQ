import os
import json
import ee
import folium
import pandas as pd
import streamlit as st

from streamlit_folium import st_folium


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="GeoResQ | Disaster Risk Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# GEORESQ UI / CSS
# ============================================================

st.html("""
<style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 5%,
                rgba(0, 170, 255, 0.08),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 75%,
                rgba(0, 255, 170, 0.045),
                transparent 30%
            ),
            #070b12;

        color: #e8f0f7;
    }

    .block-container {
        max-width: 1700px;
        padding-top: 1rem;
        padding-left: 1.8rem;
        padding-right: 1.8rem;
        padding-bottom: 3rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }


    /* ========================================================
       HEADER
       ======================================================== */

    .georesq-header {
        display: flex;
        justify-content: space-between;
        align-items: center;

        padding: 18px 22px;
        margin-bottom: 16px;

        background:
            linear-gradient(
                135deg,
                rgba(12, 24, 38, 0.97),
                rgba(7, 15, 25, 0.97)
            );

        border: 1px solid rgba(80, 180, 255, 0.18);
        border-radius: 15px;

        box-shadow:
            0 0 30px rgba(0, 160, 255, 0.06);
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .brand-icon {
        width: 48px;
        height: 48px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 12px;

        background:
            linear-gradient(
                135deg,
                #0878e8,
                #00cfff
            );

        font-size: 25px;

        box-shadow:
            0 0 22px rgba(0, 180, 255, 0.30);
    }

    .brand-title {
        font-size: 25px;
        font-weight: 850;
        letter-spacing: 1.2px;
        color: #ffffff;
    }

    .brand-subtitle {
        font-size: 11px;
        color: #71879a;
        margin-top: 3px;
        letter-spacing: 0.8px;
    }

    .live-status {
        display: flex;
        align-items: center;
        gap: 8px;

        padding: 8px 14px;

        border-radius: 20px;

        background: rgba(0, 220, 150, 0.07);
        border: 1px solid rgba(0, 220, 150, 0.22);

        color: #54e6ad;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.7px;
    }

    .live-dot {
        width: 8px;
        height: 8px;

        border-radius: 50%;

        background: #42e6a4;

        box-shadow:
            0 0 10px #42e6a4;
    }


    /* ========================================================
       MAP HEADER
       ======================================================== */

    .map-header {
        display: flex;
        justify-content: space-between;
        align-items: center;

        padding: 15px 18px;

        background:
            linear-gradient(
                90deg,
                rgba(10, 22, 35, 0.98),
                rgba(8, 16, 27, 0.96)
            );

        border:
            1px solid rgba(70, 170, 255, 0.22);

        border-bottom: none;

        border-radius: 14px 14px 0 0;
    }

    .map-title {
        font-size: 16px;
        font-weight: 750;
        color: #ffffff;
        letter-spacing: 0.5px;
    }

    .map-subtitle {
        font-size: 10px;
        color: #6f8598;
        margin-top: 4px;
        letter-spacing: 0.4px;
    }

    .map-badge {
        padding: 6px 12px;

        border-radius: 6px;

        background: rgba(0, 150, 255, 0.09);

        border:
            1px solid rgba(0, 150, 255, 0.25);

        color: #50b9ff;

        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.8px;
    }


    /* ========================================================
       SECTION HEADERS
       ======================================================== */

    .section-title {
        font-size: 18px;
        font-weight: 750;
        color: #f5f8fb;

        margin-top: 24px;
        margin-bottom: 8px;
    }

    .section-line {
        height: 1px;

        background:
            linear-gradient(
                90deg,
                rgba(0, 180, 255, 0.35),
                transparent
            );

        margin-bottom: 15px;
    }


    /* ========================================================
       METRIC CARDS
       ======================================================== */

    .metric-card {
        background:
            linear-gradient(
                145deg,
                rgba(16, 29, 43, 0.96),
                rgba(8, 17, 27, 0.96)
            );

        border:
            1px solid rgba(100, 170, 220, 0.14);

        border-radius: 12px;

        padding: 15px 16px;

        min-height: 103px;

        box-shadow:
            inset 0 1px rgba(255,255,255,0.025);
    }

    .metric-label {
        color: #71879b;

        font-size: 9px;

        text-transform: uppercase;

        letter-spacing: 1.2px;
    }

    .metric-value {
        color: #ffffff;

        font-size: 24px;

        font-weight: 850;

        margin-top: 8px;
    }

    .metric-description {
        color: #53697b;

        font-size: 10px;

        margin-top: 3px;
    }


    /* ========================================================
       RISK CARD
       ======================================================== */

    .risk-card {
        padding: 19px 21px;

        border-radius: 14px;

        background:
            linear-gradient(
                135deg,
                rgba(255, 120, 30, 0.08),
                rgba(15, 25, 38, 0.97)
            );

        margin-top: 15px;
        margin-bottom: 18px;
    }

    .risk-label {
        font-size: 9px;

        letter-spacing: 1.7px;

        color: #8094a5;

        text-transform: uppercase;
    }

    .risk-value {
        font-size: 30px;

        font-weight: 900;

        margin-top: 4px;
    }

    .risk-score {
        font-size: 11px;

        color: #8ba0b1;

        margin-top: 2px;
    }


    /* ========================================================
       INTERACTIVE RISK KEY
       ======================================================== */

    .risk-key-intro {
        color: #71879a;
        font-size: 11px;
        line-height: 1.5;
        margin-bottom: 12px;
    }

    div[role="radiogroup"] {
        display: flex !important;
        gap: 8px !important;
        flex-wrap: wrap !important;

        padding: 10px !important;

        background:
            rgba(8, 17, 27, 0.92) !important;

        border:
            1px solid rgba(80, 160, 220, 0.14) !important;

        border-radius: 12px !important;
    }

    div[role="radiogroup"] label {
        background:
            rgba(18, 31, 45, 0.90) !important;

        border:
            1px solid rgba(100, 170, 220, 0.12) !important;

        border-radius: 8px !important;

        padding: 7px 12px !important;

        transition:
            all 0.15s ease !important;
    }

    div[role="radiogroup"] label:hover {
        border-color:
            rgba(77, 185, 255, 0.45) !important;

        background:
            rgba(30, 50, 70, 0.95) !important;
    }


    /* ========================================================
       ASSESSMENT PANEL
       ======================================================== */

    .assessment-panel {
        margin-top: 16px;

        padding: 22px;

        border-radius: 15px;

        background:
            linear-gradient(
                135deg,
                rgba(14, 28, 42, 0.98),
                rgba(7, 15, 25, 0.98)
            );
    }

    .assessment-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;

        gap: 20px;

        flex-wrap: wrap;
    }

    .assessment-kicker {
        color: #6f8598;

        font-size: 9px;

        letter-spacing: 1.7px;

        text-transform: uppercase;

        margin-bottom: 7px;
    }

    .assessment-title {
        color: #ffffff;

        font-size: 21px;

        font-weight: 800;
    }

    .assessment-status {
        padding: 8px 14px;

        border-radius: 20px;

        font-size: 10px;

        font-weight: 800;

        letter-spacing: 1px;
    }

    .assessment-value-row {
        display: flex;

        align-items: flex-end;

        gap: 15px;

        margin-top: 20px;

        flex-wrap: wrap;
    }

    .assessment-value {
        font-size: 34px;

        font-weight: 900;

        line-height: 1;
    }

    .assessment-current {
        color: #64798b;

        font-size: 10px;

        padding-bottom: 3px;
    }

    .assessment-description {
        margin-top: 18px;

        padding-top: 15px;

        border-top:
            1px solid rgba(100,160,200,0.10);

        color: #8296a7;

        font-size: 12px;

        line-height: 1.6;
    }

    .assessment-method {
        margin-top: 13px;

        color: #53697b;

        font-size: 10px;

        line-height: 1.5;
    }


    /* ========================================================
       INFO STRIP
       ======================================================== */

    .info-strip {
        padding: 11px 15px;

        margin-top: 10px;

        background: rgba(8, 18, 29, 0.88);

        border:
            1px solid rgba(80, 160, 220, 0.13);

        border-radius: 9px;

        color: #7d91a3;

        font-size: 10px;
    }


    /* ========================================================
       DECISION CARDS
       ======================================================== */

    .decision-card {
        padding: 17px;

        min-height: 145px;

        border-radius: 12px;

        background:
            linear-gradient(
                145deg,
                rgba(14, 28, 42, 0.96),
                rgba(8, 17, 27, 0.96)
            );

        border:
            1px solid rgba(90, 160, 215, 0.14);
    }

    .decision-title {
        color: #ffffff;

        font-size: 14px;

        font-weight: 750;

        margin-bottom: 9px;
    }

    .decision-value {
        color: #4db9ff;

        font-size: 21px;

        font-weight: 800;

        margin-bottom: 6px;
    }

    .decision-text {
        color: #71879a;

        font-size: 10px;

        line-height: 1.5;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #080e16,
                #0b111a
            );

        border-right:
            1px solid rgba(80, 160, 220, 0.10);
    }

    .sidebar-brand {
        padding: 7px 0 18px 0;
    }

    .sidebar-kicker {
        font-size: 9px;

        letter-spacing: 2px;

        color: #4db9ff;

        font-weight: 800;
    }

    .sidebar-title {
        font-size: 21px;

        font-weight: 850;

        color: #ffffff;

        margin-top: 4px;
    }

    .sidebar-description {
        font-size: 10px;

        color: #65798b;

        margin-top: 4px;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer-box {
        text-align: center;

        padding: 15px;

        color: #4f6476;

        font-size: 10px;

        letter-spacing: 0.5px;

        line-height: 1.7;
    }

</style>
""")


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ID = os.getenv(
    "GEE_PROJECT",
    "georesq"
)

CENTER_LAT = 12.975
CENTER_LON = 80.20

RISK_THRESHOLD = 0.40


# ============================================================
# EARTH ENGINE INITIALIZATION
# ============================================================

def initialize_earth_engine():

    try:

        ee.Initialize(
            project=PROJECT_ID
        )

        return True, "Earth Engine connected locally."

    except Exception as local_error:

        try:

            raw = st.secrets.get(
                "GEE_SERVICE_ACCOUNT_JSON",
                None
            )

            if raw:

                if isinstance(raw, dict):
                    info = dict(raw)
                else:
                    info = json.loads(str(raw))

                credentials = ee.ServiceAccountCredentials(
                    info["client_email"],
                    key_data=info["private_key"]
                )

                ee.Initialize(
                    credentials=credentials,
                    project=PROJECT_ID
                )

                return (
                    True,
                    "Earth Engine connected using service account."
                )

        except Exception as cloud_error:

            return (
                False,
                "Local Earth Engine initialization failed:\n"
                + str(local_error)
                + "\n\nCloud authentication also failed:\n"
                + str(cloud_error)
            )

        return False, str(local_error)


EE_OK, EE_ERROR = initialize_earth_engine()


if not EE_OK:

    st.error(
        "❌ Earth Engine is not initialized."
    )

    st.markdown(
        """
        ### If you are running locally

        Run:

        ```bash
        earthengine authenticate
        ```

        Then restart Streamlit.
        """
    )

    st.code(EE_ERROR)

    st.stop()


# ============================================================
# AREA OF INTEREST
# ============================================================

AOI = ee.Geometry.Rectangle(
    [
        80.05,
        12.80,
        80.35,
        13.15
    ]
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize(
    image,
    min_value,
    max_value
):

    return (
        image
        .subtract(min_value)
        .divide(
            max_value - min_value
        )
        .clamp(0, 1)
    )


def add_ee_layer(
    map_obj,
    ee_image,
    vis_params,
    name,
    shown=True,
    opacity=0.7
):

    map_id = (
        ee.Image(ee_image)
        .getMapId(vis_params)
    )

    folium.TileLayer(
        tiles=(
            "https://earthengine.googleapis.com/v1alpha/"
            f"{map_id['mapid']}/tiles/{{z}}/{{x}}/{{y}}"
        ),

        attr="Google Earth Engine",

        name=name,

        overlay=True,

        control=True,

        show=shown,

        opacity=opacity

    ).add_to(
        map_obj
    )


def region_value(
    image,
    reducer=ee.Reducer.mean(),
    scale=1000
):

    try:

        result = (
            image
            .reduceRegion(
                reducer=reducer,
                geometry=AOI,
                scale=scale,
                maxPixels=1e9
            )
            .getInfo()
        )

        if not result:
            return 0.0

        values = list(
            result.values()
        )

        if not values:
            return 0.0

        value = values[0]

        if value is None:
            return 0.0

        return float(value)

    except Exception:

        return 0.0


def calculate_area(
    image,
    scale=100
):

    try:

        area = (
            ee.Image(image)
            .selfMask()
            .multiply(
                ee.Image.pixelArea()
            )
            .reduceRegion(
                reducer=ee.Reducer.sum(),
                geometry=AOI,
                scale=scale,
                maxPixels=1e10
            )
            .getInfo()
        )

        if not area:
            return 0.0

        values = list(
            area.values()
        )

        if (
            not values
            or values[0] is None
        ):
            return 0.0

        return (
            float(values[0])
            / 1e6
        )

    except Exception:

        return 0.0


def classify_score(score):

    if score < 0.25:

        return (
            "LOW",
            "🟢",
            "#32d583"
        )

    elif score < 0.40:

        return (
            "MODERATE",
            "🟡",
            "#f5c451"
        )

    elif score < 0.60:

        return (
            "HIGH",
            "🟠",
            "#ff9f43"
        )

    else:

        return (
            "VERY HIGH",
            "🔴",
            "#ff5c5c"
        )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.html("""
<div class="sidebar-brand">

    <div class="sidebar-kicker">
        GEORESQ CONTROL
    </div>

    <div class="sidebar-title">
        Mission Console
    </div>

    <div class="sidebar-description">
        Disaster analysis parameters
    </div>

</div>
""")

st.sidebar.markdown("---")

st.sidebar.markdown(
    "### 📍 ANALYSIS ORIGIN"
)

start_lat = st.sidebar.number_input(
    "Start Latitude",
    value=12.960000,
    format="%.6f"
)

start_lon = st.sidebar.number_input(
    "Start Longitude",
    value=80.200000,
    format="%.6f"
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    "### ⚠️ RISK MODEL"
)

st.sidebar.metric(
    "Risk Threshold",
    f"{RISK_THRESHOLD:.2f}"
)

st.sidebar.caption(
    "Pixels with a risk score at or above this value are classified as elevated risk."
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    "### 🛰️ DATA PIPELINE"
)

st.sidebar.markdown(
    """
    **ACTIVE SOURCES**

    🛰️ Sentinel-1 SAR  
    🌱 Sentinel-2  
    ⛰️ SRTM DEM  
    🌧️ CHIRPS  
    💧 MERIT Hydro  
    🏙️ Dynamic World  
    👥 GHSL Population
    """
)

st.sidebar.markdown("---")

st.sidebar.info(
    """
    **GeoResQ**

    Satellite-based disaster risk intelligence
    for rapid hazard mapping, exposure analysis
    and decision support.
    """
)


# ============================================================
# MAIN HEADER
# ============================================================

st.html("""
<div class="georesq-header">

    <div class="brand">

        <div class="brand-icon">
            🌍
        </div>

        <div>

            <div class="brand-title">
                GEORESQ
            </div>

            <div class="brand-subtitle">
                DISASTER RISK INTELLIGENCE • GEOSPATIAL COMMAND CENTER
            </div>

        </div>

    </div>

    <div class="live-status">
        <span class="live-dot"></span>
        LIVE RISK ANALYSIS
    </div>

</div>
""")


# ============================================================
# TERRAIN
# ============================================================

with st.spinner(
    "Loading terrain intelligence..."
):

    dem = (
        ee.Image(
            "USGS/SRTMGL1_003"
        )
        .select("elevation")
        .clip(AOI)
    )

    slope = (
        ee.Terrain
        .slope(dem)
        .clip(AOI)
    )


# ============================================================
# SENTINEL-1 FLOOD DETECTION
# ============================================================

with st.spinner(
    "Processing Sentinel-1 SAR..."
):

    s1 = (
        ee.ImageCollection(
            "COPERNICUS/S1_GRD"
        )
        .filterBounds(AOI)
        .filter(
            ee.Filter.eq(
                "instrumentMode",
                "IW"
            )
        )
        .filter(
            ee.Filter.listContains(
                "transmitterReceiverPolarisation",
                "VV"
            )
        )
        .select("VV")
    )

    before_collection = (
        s1
        .filterDate(
            "2025-09-01",
            "2026-08-31"
        )
    )

    after_collection = (
        s1
        .filterDate(
            "2026-09-01",
            "2026-09-20"
        )
    )

    before_count = (
        before_collection
        .size()
        .getInfo()
    )

    after_count = (
        after_collection
        .size()
        .getInfo()
    )

    if before_count > 0:

        sar_before = (
            before_collection
            .median()
            .clip(AOI)
        )

    else:

        sar_before = (
            ee.Image
            .constant(-15)
            .rename("VV")
            .clip(AOI)
        )

    if after_count > 0:

        sar_after = (
            after_collection
            .median()
            .clip(AOI)
        )

    else:

        sar_after = (
            ee.Image
            .constant(-15)
            .rename("VV")
            .clip(AOI)
        )

    sar_change = (
        sar_before
        .subtract(
            sar_after
        )
        .rename(
            "SAR_change"
        )
    )


# ============================================================
# PERMANENT WATER MASK
# ============================================================

jrc_water = (
    ee.Image(
        "JRC/GSW1_4/GlobalSurfaceWater"
    )
    .select("occurrence")
)

permanent_water = (
    jrc_water
    .gt(50)
    .clip(AOI)
)


# ============================================================
# OBSERVED FLOOD
# ============================================================

observed_flood = (
    sar_after
    .lt(-16)
    .And(
        sar_change.gt(3)
    )
    .And(
        permanent_water.Not()
    )
    .rename(
        "Observed_Flood"
    )
    .clip(AOI)
)


# ============================================================
# CHIRPS RAINFALL
# ============================================================

with st.spinner(
    "Processing rainfall intelligence..."
):

    chirps = (
        ee.ImageCollection(
            "UCSB-CHG/CHIRPS/DAILY"
        )
        .filterBounds(AOI)
        .filterDate(
            "2026-08-25",
            "2026-09-20"
        )
        .select(
            "precipitation"
        )
    )

    chirps_count = (
        chirps
        .size()
        .getInfo()
    )

    if chirps_count > 0:

        rainfall_recent = (
            chirps
            .sort(
                "system:time_start",
                False
            )
            .limit(3)
            .sum()
            .clip(AOI)
        )

    else:

        rainfall_recent = (
            ee.Image
            .constant(0)
            .rename(
                "precipitation"
            )
            .clip(AOI)
        )


rainfall_score = normalize(
    rainfall_recent,
    0,
    150
)


# ============================================================
# MERIT HYDRO
# ============================================================

with st.spinner(
    "Processing hydrological terrain..."
):

    merit_hydro = (
        ee.Image(
            "MERIT/Hydro/v1_0_1"
        )
        .select("hnd")
        .clip(AOI)
    )

    low_hand = (
        ee.Image
        .constant(1)
        .subtract(
            normalize(
                merit_hydro,
                0,
                50
            )
        )
        .clamp(0, 1)
    )


# ============================================================
# FLOOD SUSCEPTIBILITY
# ============================================================

flood_susceptibility = (
    low_hand
    .multiply(0.50)
    .add(
        rainfall_score
        .multiply(0.50)
    )
    .rename(
        "Flood_Susceptibility"
    )
)


# ============================================================
# FLOOD HAZARD
# ============================================================

flood_hazard = (
    flood_susceptibility
    .multiply(0.70)
    .add(
        observed_flood
        .multiply(0.30)
    )
    .rename(
        "Flood_Hazard"
    )
    .clip(AOI)
)


# ============================================================
# SENTINEL-2 NDVI
# ============================================================

with st.spinner(
    "Processing Sentinel-2 vegetation..."
):

    s2 = (
        ee.ImageCollection(
            "COPERNICUS/S2_SR_HARMONIZED"
        )
        .filterBounds(AOI)
        .filterDate(
            "2026-09-01",
            "2026-09-20"
        )
        .filter(
            ee.Filter.lt(
                "CLOUDY_PIXEL_PERCENTAGE",
                30
            )
        )
    )

    s2_count = (
        s2
        .size()
        .getInfo()
    )

    if s2_count > 0:

        s2_image = (
            s2
            .median()
            .clip(AOI)
        )

        ndvi = (
            s2_image
            .normalizedDifference(
                [
                    "B8",
                    "B4"
                ]
            )
            .rename(
                "NDVI"
            )
        )

    else:

        ndvi = (
            ee.Image
            .constant(0.45)
            .rename(
                "NDVI"
            )
            .clip(AOI)
        )


# ============================================================
# DYNAMIC WORLD
# ============================================================

with st.spinner(
    "Processing land-use intelligence..."
):

    dynamic_world = (
        ee.ImageCollection(
            "GOOGLE/DYNAMICWORLD/V1"
        )
        .filterBounds(AOI)
        .filterDate(
            "2026-09-01",
            "2026-09-20"
        )
    )

    dw_count = (
        dynamic_world
        .size()
        .getInfo()
    )

    if dw_count > 0:

        built_up = (
            dynamic_world
            .select("built")
            .mean()
            .clip(AOI)
        )

    else:

        built_up = (
            ee.Image
            .constant(0.20)
            .rename(
                "built"
            )
            .clip(AOI)
        )


# ============================================================
# GHSL POPULATION
# ============================================================

with st.spinner(
    "Processing population exposure..."
):

    population = (
        ee.Image(
            "JRC/GHSL/P2023A/GHS_POP/2020"
        )
        .select(
            "population_count"
        )
        .clip(AOI)
    )

    population_score = normalize(
        population,
        0,
        1000
    )


# ============================================================
# EXPOSURE
# ============================================================

exposure = (
    built_up
    .multiply(0.50)
    .add(
        population_score
        .multiply(0.50)
    )
    .rename(
        "Exposure"
    )
    .clip(AOI)
)


# ============================================================
# LANDSLIDE HAZARD
# ============================================================

slope_score = normalize(
    slope,
    0,
    45
)

elevation_score = normalize(
    dem,
    0,
    500
)

inverse_ndvi = (
    ee.Image
    .constant(1)
    .subtract(
        normalize(
            ndvi,
            -1,
            1
        )
    )
    .clamp(0, 1)
)

landslide_hazard = (
    slope_score
    .multiply(0.50)

    .add(
        rainfall_score
        .multiply(0.25)
    )

    .add(
        inverse_ndvi
        .multiply(0.15)
    )

    .add(
        elevation_score
        .multiply(0.10)
    )

    .rename(
        "Landslide_Hazard"
    )
    .clip(AOI)
)


# ============================================================
# MULTI-HAZARD RISK
# ============================================================

multi_hazard_risk = (
    flood_hazard
    .multiply(0.40)

    .add(
        landslide_hazard
        .multiply(0.30)
    )

    .add(
        exposure
        .multiply(0.30)
    )

    .rename(
        "Multi_Hazard_Risk"
    )

    .clip(AOI)
)


# ============================================================
# ELEVATED RISK
# ============================================================

elevated_risk = (
    multi_hazard_risk
    .gte(
        RISK_THRESHOLD
    )
    .rename(
        "Elevated_Risk"
    )
)


# ============================================================
# SETTLEMENTS
# ============================================================

settlements = (
    built_up
    .gte(0.50)
    .rename(
        "Settlements"
    )
)

affected_settlements = (
    settlements
    .And(
        elevated_risk
    )
    .rename(
        "Affected_Settlements"
    )
)


# ============================================================
# METRICS
# ============================================================

with st.spinner(
    "Calculating risk telemetry..."
):

    mean_risk = region_value(
        multi_hazard_risk,
        scale=500
    )

    max_risk = region_value(
        multi_hazard_risk,
        reducer=ee.Reducer.max(),
        scale=500
    )

    mean_flood = region_value(
        flood_hazard,
        scale=500
    )

    mean_landslide = region_value(
        landslide_hazard,
        scale=500
    )

    mean_exposure = region_value(
        exposure,
        scale=500
    )

    observed_flood_area = calculate_area(
        observed_flood,
        scale=100
    )

    elevated_risk_area = calculate_area(
        elevated_risk,
        scale=100
    )

    affected_built_area = calculate_area(
        built_up.updateMask(
            elevated_risk
        ),
        scale=100
    )

    affected_settlement_area = calculate_area(
        affected_settlements,
        scale=100
    )


# ============================================================
# OVERALL RISK
# ============================================================

overall_level, overall_icon, overall_color = classify_score(
    mean_risk
)


# ============================================================
# MAP HEADER
# ============================================================

st.html("""
<div class="map-header">

    <div>

        <div class="map-title">
            🛰️ GEOSPATIAL RISK SURFACE
        </div>

        <div class="map-subtitle">
            MULTI-HAZARD ANALYSIS • SATELLITE • TERRAIN • RAINFALL • EXPOSURE
        </div>

    </div>

    <div class="map-badge">
        ● SATELLITE ANALYSIS
    </div>

</div>
""")


# ============================================================
# MAIN MAP
# ============================================================

m = folium.Map(
    location=[
        CENTER_LAT,
        CENTER_LON
    ],

    zoom_start=11,

    tiles="OpenStreetMap",

    control_scale=True
)


# ============================================================
# ELEVATION
# ============================================================

add_ee_layer(
    m,
    dem,
    {
        "min": 0,
        "max": 300,
        "palette": [
            "blue",
            "green",
            "yellow",
            "brown"
        ]
    },
    "Elevation",
    shown=False,
    opacity=0.60
)


# ============================================================
# SLOPE
# ============================================================

add_ee_layer(
    m,
    slope,
    {
        "min": 0,
        "max": 45,
        "palette": [
            "green",
            "yellow",
            "orange",
            "red"
        ]
    },
    "Slope",
    shown=False,
    opacity=0.60
)


# ============================================================
# OBSERVED FLOOD
# ============================================================

add_ee_layer(
    m,
    observed_flood,
    {
        "min": 0,
        "max": 1,
        "palette": [
            "005eff"
        ]
    },
    "Observed Flood",
    shown=True,
    opacity=0.78
)


# ============================================================
# FLOOD HAZARD
# ============================================================

add_ee_layer(
    m,
    flood_hazard,
    {
        "min": 0,
        "max": 1,
        "palette": [
            "ffffff",
            "ffff00",
            "ff9900",
            "ff0000"
        ]
    },
    "Flood Hazard",
    shown=False,
    opacity=0.55
)


# ============================================================
# LANDSLIDE HAZARD
# ============================================================

add_ee_layer(
    m,
    landslide_hazard,
    {
        "min": 0,
        "max": 1,
        "palette": [
            "00ff66",
            "ffff00",
            "ff9900",
            "ff0000"
        ]
    },
    "Landslide Hazard",
    shown=False,
    opacity=0.55
)


# ============================================================
# EXPOSURE
# ============================================================

add_ee_layer(
    m,
    exposure,
    {
        "min": 0,
        "max": 1,
        "palette": [
            "ffffff",
            "ffff00",
            "ff9900",
            "ff0000"
        ]
    },
    "Exposure",
    shown=False,
    opacity=0.50
)


# ============================================================
# MULTI-HAZARD RISK
# ============================================================

add_ee_layer(
    m,
    multi_hazard_risk,
    {
        "min": 0,
        "max": 1,
        "palette": [
            "00d084",
            "ffff00",
            "ff9900",
            "ff0000"
        ]
    },
    "Multi-Hazard Risk",
    shown=True,
    opacity=0.58
)


# ============================================================
# ELEVATED RISK
# ============================================================

add_ee_layer(
    m,
    elevated_risk,
    {
        "min": 0,
        "max": 1,
        "palette": [
            "ff1744"
        ]
    },
    "Elevated Risk Zones",
    shown=False,
    opacity=0.65
)


# ============================================================
# AFFECTED SETTLEMENTS
# ============================================================

add_ee_layer(
    m,
    affected_settlements,
    {
        "min": 0,
        "max": 1,
        "palette": [
            "7a0019"
        ]
    },
    "Affected Settlements",
    shown=False,
    opacity=0.80
)


# ============================================================
# ANALYSIS ORIGIN
# ============================================================

folium.Marker(
    [
        start_lat,
        start_lon
    ],

    tooltip="GeoResQ Analysis Origin",

    popup=(
        "<b>GeoResQ Analysis Origin</b><br>"
        f"Latitude: {start_lat:.6f}<br>"
        f"Longitude: {start_lon:.6f}"
    ),

    icon=folium.Icon(
        color="blue",
        icon="info-sign"
    )

).add_to(m)


# ============================================================
# MAP LAYER CONTROL
# ============================================================

folium.LayerControl(
    collapsed=False
).add_to(m)


# ============================================================
# DISPLAY MAP
# ============================================================

st_folium(
    m,
    width=None,
    height=760,
    returned_objects=[]
)


# ============================================================
# MAP LEGEND
# ============================================================

st.html("""
<div class="info-strip">

    <b style="color:#eaf4fb;">
        RISK SCALE
    </b>

    &nbsp;&nbsp;&nbsp;

    <span style="color:#32d583;">●</span>
    LOW

    &nbsp;&nbsp;

    <span style="color:#f5c451;">●</span>
    MODERATE

    &nbsp;&nbsp;

    <span style="color:#ff9f43;">●</span>
    HIGH

    &nbsp;&nbsp;

    <span style="color:#ff5c5c;">●</span>
    VERY HIGH

    &nbsp;&nbsp;&nbsp;&nbsp;

    <span style="color:#4db9ff;">
        ◆
    </span>

    SATELLITE-DERIVED

</div>
""")


# ============================================================
# INTERACTIVE RISK ASSESSMENT KEY
# ============================================================

st.html("""
<div class="section-title">
    🎛️ INTERACTIVE RISK ASSESSMENT
</div>

<div class="section-line"></div>

<div class="risk-key-intro">
    Select a layer to inspect its current GeoResQ assessment.
    The assessment updates automatically based on the selected
    hazard indicator.
</div>
""")


risk_layers = [
    "Observed Flood",
    "Flood Hazard",
    "Landslide Hazard",
    "Exposure",
    "Multi-Hazard Risk",
    "Elevated Risk Zones",
    "Affected Settlements"
]


selected_layer = st.radio(
    "Select risk layer",
    risk_layers,
    horizontal=True,
    label_visibility="collapsed",
    key="risk_assessment_layer"
)


# ============================================================
# SELECTED LAYER ASSESSMENT
# ============================================================

if selected_layer == "Observed Flood":

    assessment_icon = "🌊"
    assessment_title = "Observed Flood Assessment"

    assessment_value = (
        f"{observed_flood_area:.2f} km²"
    )

    if observed_flood_area > 0:
        assessment_status = "FLOOD SIGNAL DETECTED"
        assessment_color = "#2997ff"
    else:
        assessment_status = "NO SIGNIFICANT SIGNAL"
        assessment_color = "#32d583"

    assessment_description = (
        "Sentinel-1 SAR detected areas showing significant "
        "temporal backscatter change. Permanent water bodies "
        "are excluded from the observed flood candidate layer."
    )

    assessment_method = (
        "Method: Sentinel-1 VV backscatter change + "
        "permanent-water masking."
    )


elif selected_layer == "Flood Hazard":

    assessment_icon = "💧"
    assessment_title = "Flood Hazard Assessment"

    assessment_value = (
        f"{mean_flood:.3f}"
    )

    (
        assessment_status,
        _,
        assessment_color
    ) = classify_score(
        mean_flood
    )

    assessment_description = (
        "Flood hazard combines hydrological terrain "
        "conditions, recent rainfall and observed flood "
        "signals to produce a normalized 0–1 hazard score."
    )

    assessment_method = (
        "Model: 50% low HAND + 50% rainfall for "
        "susceptibility, combined with observed flood."
    )


elif selected_layer == "Landslide Hazard":

    assessment_icon = "⛰️"
    assessment_title = "Landslide Hazard Assessment"

    assessment_value = (
        f"{mean_landslide:.3f}"
    )

    (
        assessment_status,
        _,
        assessment_color
    ) = classify_score(
        mean_landslide
    )

    assessment_description = (
        "Landslide susceptibility is modeled from terrain "
        "slope, rainfall, vegetation condition and elevation."
    )

    assessment_method = (
        "Model: 50% slope + 25% rainfall + "
        "15% inverse NDVI + 10% elevation."
    )


elif selected_layer == "Exposure":

    assessment_icon = "🏙️"
    assessment_title = "Disaster Exposure Assessment"

    assessment_value = (
        f"{mean_exposure:.3f}"
    )

    (
        assessment_status,
        _,
        assessment_color
    ) = classify_score(
        mean_exposure
    )

    assessment_description = (
        "Exposure represents the potential concentration "
        "of people and built-up areas within the analyzed "
        "region."
    )

    assessment_method = (
        "Model: 50% Dynamic World built-up probability "
        "+ 50% normalized GHSL population."
    )


elif selected_layer == "Multi-Hazard Risk":

    assessment_icon = "⚠️"
    assessment_title = "Multi-Hazard Risk Assessment"

    assessment_value = (
        f"{mean_risk:.3f}"
    )

    assessment_status = overall_level
    assessment_color = overall_color

    assessment_description = (
        "This is the primary GeoResQ risk indicator. "
        "It combines flood hazard, landslide hazard and "
        "disaster exposure into a single normalized risk score."
    )

    assessment_method = (
        "Model: 40% flood hazard + 30% landslide hazard "
        "+ 30% exposure."
    )


elif selected_layer == "Elevated Risk Zones":

    assessment_icon = "🚨"
    assessment_title = "Elevated Risk Zone Assessment"

    assessment_value = (
        f"{elevated_risk_area:.2f} km²"
    )

    if elevated_risk_area > 0:

        assessment_status = "ACTION REQUIRED"
        assessment_color = "#ff5c5c"

    else:

        assessment_status = "NO ELEVATED ZONES"
        assessment_color = "#32d583"

    assessment_description = (
        "These are areas where the modeled multi-hazard "
        f"risk score is greater than or equal to "
        f"{RISK_THRESHOLD:.2f}."
    )

    assessment_method = (
        f"Threshold: Multi-Hazard Risk ≥ {RISK_THRESHOLD:.2f}."
    )


else:

    assessment_icon = "🏠"
    assessment_title = "Affected Settlement Assessment"

    assessment_value = (
        f"{affected_settlement_area:.2f} km²"
    )

    if affected_settlement_area > 0:

        assessment_status = "SETTLEMENTS EXPOSED"
        assessment_color = "#ff5c5c"

    else:

        assessment_status = "LOW EXPOSURE"
        assessment_color = "#32d583"

    assessment_description = (
        "This layer identifies built-up settlement areas "
        "that overlap with elevated multi-hazard risk zones."
    )

    assessment_method = (
        "Method: Dynamic World built-up areas "
        "intersected with elevated risk zones."
    )


# ============================================================
# ASSESSMENT PANEL
# ============================================================

st.html(
    f"""
    <div
        class="assessment-panel"
        style="
            border:
                1px solid {assessment_color}55;

            box-shadow:
                0 0 30px {assessment_color}0d;
        "
    >

        <div class="assessment-top">

            <div>

                <div class="assessment-kicker">
                    SELECTED ANALYSIS
                </div>

                <div class="assessment-title">
                    {assessment_icon}
                    {assessment_title}
                </div>

            </div>


            <div
                class="assessment-status"
                style="
                    background:
                        {assessment_color}15;

                    border:
                        1px solid {assessment_color}55;

                    color:
                        {assessment_color};
                "
            >
                {assessment_status}
            </div>

        </div>


        <div class="assessment-value-row">

            <div
                class="assessment-value"
                style="
                    color:{assessment_color};
                "
            >
                {assessment_value}
            </div>

            <div class="assessment-current">
                CURRENT GEORESQ ASSESSMENT
            </div>

        </div>


        <div class="assessment-description">
            {assessment_description}
        </div>


        <div class="assessment-method">
            {assessment_method}
        </div>

    </div>
    """
)


# ============================================================
# LIVE RISK TELEMETRY
# ============================================================

st.html("""
<div class="section-title">
    ⚡ LIVE RISK TELEMETRY
</div>

<div class="section-line"></div>
""")


c1, c2, c3, c4, c5 = st.columns(5)


with c1:

    st.html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Overall Risk
            </div>

            <div
                class="metric-value"
                style="color:{overall_color};"
            >
                {mean_risk:.3f}
            </div>

            <div class="metric-description">
                {overall_level} classification
            </div>

        </div>
        """
    )


with c2:

    st.html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Flood Area
            </div>

            <div class="metric-value">
                {observed_flood_area:.2f}
            </div>

            <div class="metric-description">
                km² observed
            </div>

        </div>
        """
    )


with c3:

    st.html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Elevated Risk
            </div>

            <div class="metric-value">
                {elevated_risk_area:.2f}
            </div>

            <div class="metric-description">
                km² affected
            </div>

        </div>
        """
    )


with c4:

    st.html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Built Exposure
            </div>

            <div class="metric-value">
                {affected_built_area:.2f}
            </div>

            <div class="metric-description">
                km² exposed
            </div>

        </div>
        """
    )


with c5:

    st.html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Peak Risk
            </div>

            <div class="metric-value">
                {max_risk:.3f}
            </div>

            <div class="metric-description">
                maximum modeled value
            </div>

        </div>
        """
    )


# ============================================================
# CURRENT SYSTEM RISK
# ============================================================

st.html(
    f"""
    <div
        class="risk-card"
        style="
            border:
                1px solid {overall_color}55;

            box-shadow:
                0 0 24px {overall_color}08;
        "
    >

        <div class="risk-label">
            CURRENT SYSTEM RISK
        </div>

        <div
            class="risk-value"
            style="
                color:{overall_color};
            "
        >
            {overall_icon} {overall_level}
        </div>

        <div class="risk-score">
            Multi-hazard risk index: {mean_risk:.3f}
            &nbsp; • &nbsp;
            Threshold: {RISK_THRESHOLD:.2f}
        </div>

    </div>
    """
)


# ============================================================
# DECISION SUPPORT
# ============================================================

st.html("""
<div class="section-title">
    🧭 DECISION SUPPORT
</div>

<div class="section-line"></div>
""")


d1, d2, d3 = st.columns(3)


with d1:

    st.html(
        f"""
        <div class="decision-card">

            <div class="decision-title">
                🌊 FLOOD
            </div>

            <div class="decision-value">
                {observed_flood_area:.2f} km²
            </div>

            <div class="decision-text">
                Sentinel-1 SAR indicates this area as
                an observed flood candidate based on
                temporal backscatter change and
                permanent-water masking.
            </div>

        </div>
        """
    )


with d2:

    st.html(
        f"""
        <div class="decision-card">

            <div class="decision-title">
                ⛰️ LANDSLIDE
            </div>

            <div class="decision-value">
                {mean_landslide:.3f}
            </div>

            <div class="decision-text">
                Mean modeled landslide susceptibility
                derived from slope, rainfall, vegetation
                condition and elevation.
            </div>

        </div>
        """
    )


with d3:

    st.html(
        f"""
        <div class="decision-card">

            <div class="decision-title">
                🏙️ EXPOSURE
            </div>

            <div class="decision-value">
                {mean_exposure:.3f}
            </div>

            <div class="decision-text">
                Combined built-up and population exposure
                indicator across the analyzed region.
            </div>

        </div>
        """
    )


# ============================================================
# PRIORITY ALERTS
# ============================================================

st.html("""
<div class="section-title">
    🚨 PRIORITY ALERTS
</div>

<div class="section-line"></div>
""")


if observed_flood_area > 0:

    st.info(
        f"""
        🌊 **Flood signal detected:** approximately
        **{observed_flood_area:.2f} km²** is classified
        as an observed flood candidate.
        """
    )


if elevated_risk_area > 0:

    st.warning(
        f"""
        ⚠️ **Elevated-risk zone:** approximately
        **{elevated_risk_area:.2f} km²** crosses the
        GeoResQ threshold of **{RISK_THRESHOLD:.2f}**.
        """
    )


if affected_built_area > 0:

    st.warning(
        f"""
        🏙️ **Built-up exposure:** approximately
        **{affected_built_area:.2f} km²** of built-up
        area overlaps elevated-risk zones.
        """
    )


# ============================================================
# RISK INDICATOR LEVELS
# ============================================================

with st.expander(
    "🚦 Risk Indicator Levels",
    expanded=False
):

    indicator_table = pd.DataFrame(
        [
            [
                "🟢 Low",
                "0.00 – 0.24",
                "Limited modeled hazard/exposure"
            ],

            [
                "🟡 Moderate",
                "0.25 – 0.39",
                "Moderate disaster risk"
            ],

            [
                "🟠 High",
                "0.40 – 0.59",
                "Elevated risk requiring attention"
            ],

            [
                "🔴 Very High",
                "0.60 – 1.00",
                "Very high modeled risk"
            ],
        ],

        columns=[
            "Risk Level",
            "Risk Score",
            "Interpretation"
        ]
    )

    st.dataframe(
        indicator_table,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FULL INDICATOR SUMMARY
# ============================================================

with st.expander(
    "📊 Full GeoResQ Indicator Summary",
    expanded=False
):

    summary_df = pd.DataFrame(
        [
            [
                "Observed Flood",
                round(
                    observed_flood_area,
                    3
                ),
                "km²",
                "Sentinel-1 SAR change"
            ],

            [
                "Flood Hazard",
                round(
                    mean_flood,
                    3
                ),
                "0–1",
                "HAND + rainfall + observed flood"
            ],

            [
                "Landslide Hazard",
                round(
                    mean_landslide,
                    3
                ),
                "0–1",
                "Slope + rainfall + NDVI + elevation"
            ],

            [
                "Exposure",
                round(
                    mean_exposure,
                    3
                ),
                "0–1",
                "Built-up + population"
            ],

            [
                "Multi-Hazard Risk",
                round(
                    mean_risk,
                    3
                ),
                "0–1",
                "40% flood + 30% landslide + 30% exposure"
            ],

            [
                "Elevated Risk Area",
                round(
                    elevated_risk_area,
                    3
                ),
                "km²",
                "Risk ≥ 0.40"
            ],

            [
                "Affected Built Area",
                round(
                    affected_built_area,
                    3
                ),
                "km²",
                "Built-up ∩ elevated risk"
            ],

            [
                "Affected Settlement Area",
                round(
                    affected_settlement_area,
                    3
                ),
                "km²",
                "Settlements ∩ elevated risk"
            ],
        ],

        columns=[
            "Indicator",
            "Value",
            "Unit",
            "Method"
        ]
    )

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# DATA SOURCES
# ============================================================

with st.expander(
    "🛰️ Data Sources & Technical Pipeline",
    expanded=False
):

    data_sources = pd.DataFrame(
        [
            [
                "Sentinel-1",
                "Flood detection",
                "SAR backscatter change"
            ],

            [
                "Sentinel-2",
                "Vegetation",
                "NDVI"
            ],

            [
                "SRTM",
                "Terrain",
                "Elevation + slope"
            ],

            [
                "CHIRPS",
                "Rainfall",
                "Recent precipitation"
            ],

            [
                "MERIT Hydro",
                "Hydrology",
                "Height Above Nearest Drainage"
            ],

            [
                "Dynamic World",
                "Land use",
                "Built-up probability"
            ],

            [
                "GHSL",
                "Population",
                "Population exposure"
            ],
        ],

        columns=[
            "Dataset",
            "Purpose",
            "Indicator"
        ]
    )

    st.dataframe(
        data_sources,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        """
        ### GeoResQ Pipeline

        **Satellite Data**

        ↓

        **Image Processing**

        ↓

        **Geospatial Analysis**

        ↓

        **Hazard & Exposure Indicators**

        ↓

        **Multi-Hazard Risk Model**

        ↓

        **Interactive Risk Map**

        ↓

        **Decision Support**

        ### Multi-Hazard Model

        **Risk =**

        **40% Flood Hazard**
        +
        **30% Landslide Hazard**
        +
        **30% Exposure**

        ### Elevated Risk

        Pixels with:

        **Risk ≥ 0.40**

        are classified as elevated-risk zones.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="footer-box">

    <b style="color:#71879a;">
        GEORESQ
    </b>
    • DISASTER RISK INTELLIGENCE

    <br>

    Sentinel-1 • Sentinel-2 • SRTM • CHIRPS •
    MERIT Hydro • Dynamic World • GHSL

    <br><br>

    Prototype decision-support system.
    Risk indicators should be validated against
    official disaster-management data before
    operational use.

</div>
""")