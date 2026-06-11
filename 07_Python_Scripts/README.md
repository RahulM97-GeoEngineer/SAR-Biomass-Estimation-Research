# Sentinel-1 Mosaic Automation

## Purpose

Automatically mosaic multiple Sentinel-1 terrain-corrected tiles acquired on the same date.

## Features

- Automatic file discovery
- Date-wise grouping
- GeoTIFF mosaicking
- CRS validation
- Statistics generation
- Processing log generation

## Input

Terrain-corrected Sentinel-1 GeoTIFF files.

## Output

- Mosaic_YYYYMMDD.tif
- mosaic_log.txt
- mosaic_statistics.csv

## Software

- Python
- Rasterio
- NumPy
- Pandas

## Application

The mosaics are used for:

- VV/VH Ratio Generation
- Texture Feature Extraction
- Water Cloud Model Development
- Biomass Estimation
