"""
Extract Kummu v4 GDP data for the Democratic Republic of the Congo (DRC)
WITHOUT a local admin boundary file — pulls the ADM0 (country) boundary
on the fly from the geoBoundaries API.

geoBoundaries: https://www.geoboundaries.org  (open, free, no API key needed)
DRC ISO3 code: COD
"""

import requests
import geopandas as gpd


def get_country_boundary(iso3: str, adm_level: str = "ADM0") -> gpd.GeoDataFrame:
    """
    Download a country boundary from the geoBoundaries API without needing a
    local shapefile/geopackage.

    iso3: 3-letter ISO country code, e.g. "COD" for DRC, "GIN" for Guinea
    adm_level: "ADM0" (country), "ADM1" (province), "ADM2" (territory), etc.
    """
    api_url = f"https://www.geoboundaries.org/api/current/gbOpen/{iso3}/{adm_level}/"
    meta = requests.get(api_url, timeout=30).json()
    geojson_url = meta["gjDownloadURL"]

    gdf = gpd.read_file(geojson_url)
    print(f"Loaded {iso3} {adm_level} boundary: {len(gdf)} feature(s), CRS={gdf.crs}")
    return gdf


# --- Get DRC's country boundary (ISO3 = COD) ---
drc_gdf = get_country_boundary("COD", adm_level="ADM0")

# --- Run the windowed extraction for DRC — latest year only (2024) ---
tif_path = gdp_path + "\\rast_gdpTot_1990_2024_30arcsec.tif"

da_drc_2024 = preprocess_kummu_gdp_tif_windowed(
    tif_path=tif_path,
    year=2024,
    boundary_gdf=drc_gdf,
    out_path=gdp_path + "\\GDP_PPP_2024_COD.tif",
)

print("\nTotal DRC GDP 2024 (v4, sum of pixels):", float(da_drc_2024.sum()))
