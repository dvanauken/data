#!/usr/bin/env python3
"""
Download Natural Earth Vector GeoJSON files with organized directory structure
and configurable download options
"""

import requests
import time
import os
import signal
import sys

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print(f"\n\nInterrupted by user (Ctrl+C)")
    print("Exiting gracefully...")
    sys.exit(0)

def download_geojson_files():
    """Download geojson files with organized directory structure"""
    
    # TOP-LEVEL CONFIGURATION
    should_overwrite = True  # Global default - can be changed to False
    
    # Base URL for the geojson folder  
    base_url = "https://github.com/nvkelso/natural-earth-vector/raw/master/geojson/"
    
    # Dictionary with download configuration for each file
    # Format: source_filename: {"download": True/False, "directory": "path", "save_as": "filename"}
    geojson_files = {
        # COASTLINE FILES - High Priority
        "ne_10m_coastline.geojson": {"download": True, "directory": "features/coastlines", "save_as": "coastline_10m.geojson"},
        "ne_10m_minor_islands_coastline.geojson": {"download": True, "directory": "features/coastlines", "save_as": "coastline_island_10m.geojson", "should_overwrite": False},
        
        # LAND/OCEAN FILES - High Priority  
        "ne_10m_land.geojson": {"download": True, "directory": "features/land_ocean", "save_as": "land_10m.geojson"},
        "ne_10m_ocean.geojson": {"download": True, "directory": "features/land_ocean", "save_as": "ocean_10m.geojson"},
        "ne_10m_land_ocean_label_points.geojson": {"download": False, "directory": "features/land_ocean", "save_as": "ne_10m_land_ocean_label_points.geojson"},
        "ne_10m_land_ocean_seams.geojson": {"download": False, "directory": "features/land_ocean", "save_as": "ne_10m_land_ocean_seams.geojson"},
        "ne_10m_land_scale_rank.geojson": {"download": False, "directory": "features/land_ocean", "save_as": "ne_10m_land_scale_rank.geojson"},
        "ne_10m_ocean_scale_rank.geojson": {"download": False, "directory": "features/land_ocean", "save_as": "ne_10m_ocean_scale_rank.geojson"},
        
        # ADMIN/POLITICAL FILES
        "ne_10m_admin_0_countries.geojson": {"download": True, "directory": "features/admin/countries", "save_as": "admin_0.geojson"},
        "ne_10m_admin_0_countries_lakes.geojson": {"download": True, "directory": "features/admin/countries", "save_as": "admin_0_lakes.geojson"},
        "ne_10m_admin_0_boundary_lines_land.geojson": {"download": True, "directory": "features/admin/boundaries", "save_as": "admin_0_lines.geojson"},
        "ne_10m_admin_1_states_provinces.geojson": {"download": False, "directory": "features/admin/states_provinces", "save_as": "admin_1.geojson"},
        "ne_10m_admin_1_states_provinces_lakes.geojson": {"download": True, "directory": "features/admin/states_provinces", "save_as": "admin_1_lakes.geojson"},
        "ne_10m_admin_1_states_provinces_lines.geojson": {"download": True, "directory": "features/admin/states_provinces", "save_as": "admin_1_lines.geojson"},
        "ne_10m_admin_1_states_provinces_scale_rank.geojson": {"download": False, "directory": "features/admin/states_provinces", "save_as": "admin_1.geojson"},
        "ne_10m_admin_2_counties.geojson": {"download": True, "directory": "features/admin/counties", "save_as": "admin_2.geojson"},
        "ne_10m_admin_2_counties_lakes.geojson": {"download": True, "directory": "features/admin/counties", "save_as": "admin_2_lakes.geojson"},
        "ne_10m_admin_2_counties_scale_rank.geojson": {"download": False, "directory": "features/admin/counties", "save_as": "admin_2.geojson"},
        "ne_10m_admin_2_counties_scale_rank_minor_islands.geojson": {"download": False, "directory": "features/admin/counties", "save_as": "admin_2.geojson"},
        
        # BATHYMETRY FILES - Usually skip unless needed
        "ne_10m_bathymetry_A_10000.geojson": {"download": False, "directory": "features/bathymetry", "save_as": "ne_10m_bathymetry_A_10000.geojson"},
        "ne_10m_bathymetry_B_9000.geojson": {"download": False, "directory": "features/bathymetry", "save_as": "ne_10m_bathymetry_B_9000.geojson"},
        "ne_10m_bathymetry_C_8000.geojson": {"download": False, "directory": "features/bathymetry", "save_as": "ne_10m_bathymetry_C_8000.geojson"},
        "ne_10m_bathymetry_D_7000.geojson": {"download": False, "directory": "features/bathymetry", "save_as": "ne_10m_bathymetry_D_7000.geojson"},
        "ne_10m_bathymetry_E_6000.geojson": {"download": False, "directory": "features/bathymetry", "save_as": "ne_10m_bathymetry_E_6000.geojson"},
        "ne_10m_bathymetry_F_5000.geojson": {"download": False, "directory": "features/bathymetry", "save_as": "ne_10m_bathymetry_F_5000.geojson"},
        "ne_10m_bathymetry_G_4000.geojson": {"download": False, "directory": "features/bathymetry", "save_as": "ne_10m_bathymetry_G_4000.geojson"},
        "ne_10m_bathymetry_H_3000.geojson": {"download": False, "directory": "features/bathymetry", "save_as": "ne_10m_bathymetry_H_3000.geojson"},
        "ne_10m_bathymetry_I_2000.geojson": {"download": False, "directory": "features/bathymetry", "save_as": "ne_10m_bathymetry_I_2000.geojson"},
        "ne_10m_bathymetry_J_1000.geojson": {"download": False, "directory": "features/bathymetry", "save_as": "ne_10m_bathymetry_J_1000.geojson"},
        "ne_10m_bathymetry_K_200.geojson": {"download": False, "directory": "features/bathymetry", "save_as": "ne_10m_bathymetry_K_200.geojson"},
        "ne_10m_bathymetry_L_0.geojson": {"download": False, "directory": "features/bathymetry", "save_as": "ne_10m_bathymetry_L_0.geojson"},
        
        # WATER FEATURES
        "ne_10m_lakes.geojson": {"download": True, "directory": "features/lakes", "save_as": "ne_10m_lakes.geojson"},
        "ne_10m_lakes_australia.geojson": {"download": False, "directory": "features/lakes", "save_as": "ne_10m_lakes_australia.geojson"},
        "ne_10m_lakes_europe.geojson": {"download": False, "directory": "features/lakes", "save_as": "ne_10m_lakes_europe.geojson"},
        "ne_10m_lakes_historic.geojson": {"download": False, "directory": "features/lakes", "save_as": "ne_10m_lakes_historic.geojson"},
        "ne_10m_lakes_north_america.geojson": {"download": False, "directory": "features/lakes", "save_as": "ne_10m_lakes_north_america.geojson"},
        "ne_10m_lakes_pluvial.geojson": {"download": False, "directory": "features/lakes", "save_as": "ne_10m_lakes_pluvial.geojson"},
        "ne_10m_rivers_australia.geojson": {"download": False, "directory": "features/rivers", "save_as": "ne_10m_rivers_australia.geojson"},
        "ne_10m_rivers_europe.geojson": {"download": False, "directory": "features/rivers", "save_as": "ne_10m_rivers_europe.geojson"},
        "ne_10m_rivers_lake_centerlines.geojson": {"download": False, "directory": "features/rivers", "save_as": "ne_10m_rivers_lake_centerlines.geojson"},
        "ne_10m_rivers_lake_centerlines_scale_rank.geojson": {"download": False, "directory": "features/rivers", "save_as": "ne_10m_rivers_lake_centerlines_scale_rank.geojson"},
        "ne_10m_rivers_north_america.geojson": {"download": False, "directory": "features/rivers", "save_as": "ne_10m_rivers_north_america.geojson"},
        
        # POPULATED PLACES - Large files, usually skip
        "ne_10m_populated_places.geojson": {"download": False, "directory": "features/populated_places", "save_as": "ne_10m_populated_places.geojson"},
        "ne_10m_populated_places_simple.geojson": {"download": True, "directory": "features/populated_places", "save_as": "ne_10m_populated_places_simple.geojson"},
        
        # TRANSPORTATION - Large files, usually skip
        "ne_10m_roads.geojson": {"download": False, "directory": "features/transportation", "save_as": "ne_10m_roads.geojson"},
        "ne_10m_railroads.geojson": {"download": False, "directory": "features/transportation", "save_as": "ne_10m_railroads.geojson"},
        "ne_10m_railroads_north_america.geojson": {"download": False, "directory": "features/transportation", "save_as": "ne_10m_railroads_north_america.geojson"},
        "ne_10m_airports.geojson": {"download": True, "directory": "features/transportation", "save_as": "ne_10m_airports.geojson"},
        "ne_10m_ports.geojson": {"download": True, "directory": "features/transportation", "save_as": "ne_10m_ports.geojson"},
        
        # ISLANDS AND MINOR FEATURES
        "ne_10m_minor_islands.geojson": {"download": True, "directory": "features/islands", "save_as": "ne_10m_minor_islands.geojson"},
        "ne_10m_minor_islands_label_points.geojson": {"download": True, "directory": "features/islands", "save_as": "ne_10m_minor_islands_label_points.geojson"},
        "ne_10m_reefs.geojson": {"download": True, "directory": "features/islands", "save_as": "ne_10m_reefs.geojson"},
        
        # ICE FEATURES  
        "ne_10m_glaciated_areas.geojson": {"download": False, "directory": "features/ice_features", "save_as": "ne_10m_glaciated_areas.geojson"},
        "ne_10m_antarctic_ice_shelves_lines.geojson": {"download": False, "directory": "features/ice_features", "save_as": "ne_10m_antarctic_ice_shelves_lines.geojson"},
        "ne_10m_antarctic_ice_shelves_polys.geojson": {"download": False, "directory": "features/ice_features", "save_as": "ne_10m_antarctic_ice_shelves_polys.geojson"},
        
        # GEOGRAPHIC REFERENCE
        "ne_10m_geographic_lines.geojson": {"download": False, "directory": "features/geographic_reference", "save_as": "ne_10m_geographic_lines.geojson"},
        "ne_10m_geography_marine_polys.geojson": {"download": False, "directory": "features/geographic_reference", "save_as": "ne_10m_geography_marine_polys.geojson"},
        "ne_10m_geography_regions_elevation_points.geojson": {"download": False, "directory": "features/geographic_reference", "save_as": "ne_10m_geography_regions_elevation_points.geojson"},
        "ne_10m_geography_regions_points.geojson": {"download": False, "directory": "features/geographic_reference", "save_as": "ne_10m_geography_regions_points.geojson"},
        "ne_10m_geography_regions_polys.geojson": {"download": False, "directory": "features/geographic_reference", "save_as": "ne_10m_geography_regions_polys.geojson"},
        "ne_10m_time_zones.geojson": {"download": False, "directory": "features/geographic_reference", "save_as": "ne_10m_time_zones.geojson"},
        
        # GRATICULES - Usually skip unless making reference maps
        "ne_10m_graticules_1.geojson": {"download": False, "directory": "features/graticules", "save_as": "ne_10m_graticules_1.geojson"},
        "ne_10m_graticules_5.geojson": {"download": False, "directory": "features/graticules", "save_as": "ne_10m_graticules_5.geojson"},
        "ne_10m_graticules_10.geojson": {"download": False, "directory": "features/graticules", "save_as": "ne_10m_graticules_10.geojson"},
        "ne_10m_graticules_15.geojson": {"download": False, "directory": "features/graticules", "save_as": "ne_10m_graticules_15.geojson"},
        "ne_10m_graticules_20.geojson": {"download": False, "directory": "features/graticules", "save_as": "ne_10m_graticules_20.geojson"},
        "ne_10m_graticules_30.geojson": {"download": False, "directory": "features/graticules", "save_as": "ne_10m_graticules_30.geojson"},
        "ne_10m_wgs84_bounding_box.geojson": {"download": False, "directory": "features/graticules", "save_as": "ne_10m_wgs84_bounding_box.geojson"},
        
        # PROTECTED AREAS
        "ne_10m_parks_and_protected_lands_area.geojson": {"download": False, "directory": "features/protected_areas", "save_as": "ne_10m_parks_and_protected_lands_area.geojson"},
        "ne_10m_parks_and_protected_lands_line.geojson": {"download": False, "directory": "features/protected_areas", "save_as": "ne_10m_parks_and_protected_lands_line.geojson"},
        "ne_10m_parks_and_protected_lands_point.geojson": {"download": False, "directory": "features/protected_areas", "save_as": "ne_10m_parks_and_protected_lands_point.geojson"},
        "ne_10m_parks_and_protected_lands_scale_rank.geojson": {"download": False, "directory": "features/protected_areas", "save_as": "ne_10m_parks_and_protected_lands_scale_rank.geojson"},
        
        # URBAN AREAS
        "ne_10m_urban_areas.geojson": {"download": False, "directory": "features/urban_areas", "save_as": "ne_10m_urban_areas.geojson"},
        "ne_10m_urban_areas_landscan.geojson": {"download": False, "directory": "features/urban_areas", "save_as": "ne_10m_urban_areas_landscan.geojson"},
        
        # MISC PHYSICAL FEATURES
        "ne_10m_playas.geojson": {"download": True, "directory": "features/misc_physical", "save_as": "ne_10m_playas.geojson"},
        
        # DETAILED ADMIN FILES - Most are disabled by default
        "ne_10m_admin_0_antarctic_claim_limit_lines.geojson": {"download": False, "directory": "features/admin/detailed", "save_as": "ne_10m_admin_0_antarctic_claim_limit_lines.geojson"},
        "ne_10m_admin_0_antarctic_claims.geojson": {"download": False, "directory": "features/admin/detailed", "save_as": "ne_10m_admin_0_antarctic_claims.geojson"},
        "ne_10m_admin_0_boundary_lines_disputed_areas.geojson": {"download": False, "directory": "features/admin/detailed", "save_as": "ne_10m_admin_0_boundary_lines_disputed_areas.geojson"},
        "ne_10m_admin_0_boundary_lines_map_units.geojson": {"download": False, "directory": "features/admin/detailed", "save_as": "ne_10m_admin_0_boundary_lines_map_units.geojson"},
        "ne_10m_admin_0_boundary_lines_maritime_indicator.geojson": {"download": False, "directory": "features/admin/detailed", "save_as": "ne_10m_admin_0_boundary_lines_maritime_indicator.geojson"},
        "ne_10m_admin_0_boundary_lines_maritime_indicator_chn.geojson": {"download": False, "directory": "features/admin/detailed", "save_as": "ne_10m_admin_0_boundary_lines_maritime_indicator_chn.geojson"},
        "ne_10m_admin_0_disputed_areas.geojson": {"download": False, "directory": "features/admin/detailed", "save_as": "ne_10m_admin_0_disputed_areas.geojson"},
        "ne_10m_admin_0_disputed_areas_scale_rank_minor_islands.geojson": {"download": False, "directory": "features/admin/detailed", "save_as": "ne_10m_admin_0_disputed_areas_scale_rank_minor_islands.geojson"},
        "ne_10m_admin_0_label_points.geojson": {"download": False, "directory": "features/admin/detailed", "save_as": "ne_10m_admin_0_label_points.geojson"},
        "ne_10m_admin_0_map_subunits.geojson": {"download": False, "directory": "features/admin/detailed", "save_as": "ne_10m_admin_0_map_subunits.geojson"},
        "ne_10m_admin_0_map_units.geojson": {"download": False, "directory": "features/admin/detailed", "save_as": "ne_10m_admin_0_map_units.geojson"},
        "ne_10m_admin_0_pacific_groupings.geojson": {"download": False, "directory": "features/admin/detailed", "save_as": "ne_10m_admin_0_pacific_groupings.geojson"},
        "ne_10m_admin_0_scale_rank.geojson": {"download": False, "directory": "features/admin/detailed", "save_as": "ne_10m_admin_0_scale_rank.geojson"},
        "ne_10m_admin_0_scale_rank_minor_islands.geojson": {"download": False, "directory": "features/admin/detailed", "save_as": "ne_10m_admin_0_scale_rank_minor_islands.geojson"},
        "ne_10m_admin_0_seams.geojson": {"download": False, "directory": "features/admin/detailed", "save_as": "ne_10m_admin_0_seams.geojson"},
        "ne_10m_admin_0_sovereignty.geojson": {"download": False, "directory": "features/admin/detailed", "save_as": "ne_10m_admin_0_sovereignty.geojson"},
        "ne_10m_admin_1_label_points.geojson": {"download": False, "directory": "features/admin/detailed", "save_as": "ne_10m_admin_1_label_points.geojson"},
        "ne_10m_admin_1_label_points_details.geojson": {"download": False, "directory": "features/admin/detailed", "save_as": "ne_10m_admin_1_label_points_details.geojson"},
        "ne_10m_admin_1_seams.geojson": {"download": False, "directory": "features/admin/detailed", "save_as": "ne_10m_admin_1_seams.geojson"},
        "ne_10m_admin_2_label_points.geojson": {"download": False, "directory": "features/admin/detailed", "save_as": "ne_10m_admin_2_label_points.geojson"},
        "ne_10m_admin_2_label_points_details.geojson": {"download": False, "directory": "features/admin/detailed", "save_as": "ne_10m_admin_2_label_points_details.geojson"},
        
        # COUNTRY-SPECIFIC FILES - All disabled by default
        "ne_10m_admin_0_countries_arg.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_arg.geojson"},
        "ne_10m_admin_0_countries_bdg.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_bdg.geojson"},
        "ne_10m_admin_0_countries_bra.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_bra.geojson"},
        "ne_10m_admin_0_countries_chn.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_chn.geojson"},
        "ne_10m_admin_0_countries_deu.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_deu.geojson"},
        "ne_10m_admin_0_countries_egy.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_egy.geojson"},
        "ne_10m_admin_0_countries_esp.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_esp.geojson"},
        "ne_10m_admin_0_countries_fra.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_fra.geojson"},
        "ne_10m_admin_0_countries_gbr.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_gbr.geojson"},
        "ne_10m_admin_0_countries_grc.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_grc.geojson"},
        "ne_10m_admin_0_countries_idn.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_idn.geojson"},
        "ne_10m_admin_0_countries_ind.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_ind.geojson"},
        "ne_10m_admin_0_countries_iso.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_iso.geojson"},
        "ne_10m_admin_0_countries_isr.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_isr.geojson"},
        "ne_10m_admin_0_countries_ita.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_ita.geojson"},
        "ne_10m_admin_0_countries_jpn.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_jpn.geojson"},
        "ne_10m_admin_0_countries_kor.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_kor.geojson"},
        "ne_10m_admin_0_countries_mar.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_mar.geojson"},
        "ne_10m_admin_0_countries_nep.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_nep.geojson"},
        "ne_10m_admin_0_countries_nld.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_nld.geojson"},
        "ne_10m_admin_0_countries_pak.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_pak.geojson"},
        "ne_10m_admin_0_countries_pol.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_pol.geojson"},
        "ne_10m_admin_0_countries_prt.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_prt.geojson"},
        "ne_10m_admin_0_countries_pse.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_pse.geojson"},
        "ne_10m_admin_0_countries_rus.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_rus.geojson"},
        "ne_10m_admin_0_countries_sau.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_sau.geojson"},
        "ne_10m_admin_0_countries_swe.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_swe.geojson"},
        "ne_10m_admin_0_countries_tlc.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_tlc.geojson"},
        "ne_10m_admin_0_countries_tur.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_tur.geojson"},
        "ne_10m_admin_0_countries_twn.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_twn.geojson"},
        "ne_10m_admin_0_countries_ukr.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_ukr.geojson"},
        "ne_10m_admin_0_countries_usa.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_usa.geojson"},
        "ne_10m_admin_0_countries_vnm.geojson": {"download": False, "directory": "features/admin/country_specific", "save_as": "ne_10m_admin_0_countries_vnm.geojson"},
    }
    
    # Filter to only files marked for download
    files_to_download = {k: v for k, v in geojson_files.items() if v["download"]}
    
    print(f"Starting download of {len(files_to_download)} GeoJSON files...")
    print(f"Base directory: {os.getcwd()}")
    print(f"Files will be organized by category in subdirectories")
    
    success_count = 0
    failed_files = []
    created_dirs = set()
    
    for i, (filename, config) in enumerate(files_to_download.items(), 1):
        try:
            # Resolve should_overwrite for this file
            file_should_overwrite = config.get("should_overwrite", should_overwrite)
            
            # Create directory if it doesn't exist
            directory = config["directory"]
            if directory not in created_dirs:
                os.makedirs(directory, exist_ok=True)
                created_dirs.add(directory)
                print(f"Created directory: {directory}")
            
            # Check if file exists and if we should skip
            filepath = os.path.join(directory, config["save_as"])
            if os.path.exists(filepath) and not file_should_overwrite:
                print(f"[{i:3d}/{len(files_to_download)}] SKIP: {filename} (file exists, overwrite=False)")
                continue
            
            # Print what we're about to download
            print(f"[{i:3d}/{len(files_to_download)}] DOWNLOADING: {filename}")
            
            url = base_url + filename
            response = requests.get(url, headers={"User-Agent": "Python-NE-Downloader"})
            response.raise_for_status()
            
            # Save file
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            size_mb = len(response.content) / (1024 * 1024)
            
            # Highlight special files by category
            if 'coastline' in filename:
                print(f"    SUCCESS: Coastline file saved ({size_mb:.2f} MB)")
            elif any(keyword in filename for keyword in ['land', 'ocean']):
                print(f"    SUCCESS: Land/Ocean file saved ({size_mb:.2f} MB)")
            elif 'admin' in filename:
                print(f"    SUCCESS: Administrative file saved ({size_mb:.2f} MB)")
            elif any(keyword in filename for keyword in ['lake', 'river']):
                print(f"    SUCCESS: Water feature file saved ({size_mb:.2f} MB)")
            else:
                print(f"    SUCCESS: File saved ({size_mb:.2f} MB)")
            
            success_count += 1
            
            # Wait 1 second between downloads to be respectful
            if i < len(files_to_download):  # Don't wait after the last file
                time.sleep(1)
                
        except requests.RequestException as e:
            print(f"    ERROR: Failed to download: {e}")
    
    # Summary
    print(f"\nDownload complete!")
    print(f"SUCCESS: {success_count}/{len(files_to_download)} files downloaded")
    
    if failed_files:
        print(f"FAILED: {len(failed_files)} files")
        for failed in failed_files:
            print(f"   - {failed}")
    
    print(f"\nFiles organized in directories under: {os.getcwd()}")
    
    # Show directory structure created
    print(f"\nDirectory structure created:")
    for directory in sorted(created_dirs):
        file_count = len([f for f in files_to_download.values() if f["directory"] == directory])
        print(f"   {directory}/ ({file_count} files)")
    
    # Highlight key coastline files
    print(f"\nKey coastline files downloaded:")
    coastline_files = [filename for filename in files_to_download.keys() if 'coastline' in filename]
    for cf in coastline_files:
        config = files_to_download[cf]
        filepath = os.path.join(config["directory"], config["save_as"])
        if os.path.exists(filepath):
            print(f"   SUCCESS: {cf}")
        else:
            print(f"   MISSING: {cf}")

    print(f"\n=== COMPLETE ===")
    print("All downloads finished successfully!")
    sys.exit(0)

if __name__ == "__main__":
    try:
        download_geojson_files()
    except KeyboardInterrupt:
        print(f"\n\nProcess interrupted by user")
        print("Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nUnexpected error occurred: {e}")
        print("Exiting...")
        sys.exit(1)
    except Exception as e:
        print(f"    ERROR: Failed to save file: {e}")
        failed_files.append(filename)