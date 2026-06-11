# Sentinel-1 SAR Preprocessing Workflow

## Software

* ESA SNAP 13

## Input Data

* Sentinel-1 GRD (Interferometric Wide Swath, IW Mode)
* Polarizations: VV and VH
* External Digital Elevation Model (SRTM DEM)

## Processing Chain

### 1. Read

Import Sentinel-1 GRD products into ESA SNAP.

### 2. Apply Orbit File

Apply precise orbit information to improve geometric accuracy and geolocation.

### 3. Multilook

Reduce speckle effects and improve radiometric quality.

### 4. Remove GRD Border Noise

Remove low-intensity border noise present in Sentinel-1 GRD products.

### 5. Radiometric Calibration

Convert SAR digital numbers (DN) into calibrated backscatter coefficients (Sigma0).

### 6. Speckle Filtering

Reduce speckle noise while preserving important image features and spatial patterns.

### 7. Linear to dB Conversion

Convert calibrated backscatter values from linear scale to decibel (dB) scale for analysis and visualization.

### 8. Terrain Correction

Correct geometric distortions caused by terrain and sensor geometry using the SRTM DEM.

#### Terrain Correction Parameters

* DEM Source: External SRTM DEM
* DEM Resampling Method: Bilinear Interpolation
* Image Resampling Method: Bilinear Interpolation
* Pixel Spacing: 30 m
* Apply Earth Gravitational Model: Enabled

### 9. Write

Export the processed Sentinel-1 SAR product in GeoTIFF format for subsequent analysis.

---

## Workflow Diagram

```text
Read
↓
Apply Orbit File
↓
Multilook
↓
Remove GRD Border Noise
↓
Calibration
↓
Speckle Filter
↓
LinearToFromdB
↓
Terrain Correction
↓
Write
```

---

## Output Products

* VV Backscatter Image
* VH Backscatter Image
* Terrain-Corrected SAR Data
* GeoTIFF Export Products

---

## Current Status

### Completed

* Sentinel-1 GRD Data Download
* SRTM DEM Download
* DEM Mosaic Generation
* SAR Preprocessing Workflow Development
* Terrain Correction
* SAR Mosaic Generation

### Ongoing

* VV and VH Backscatter Verification
* SAR Mosaic Validation
* Statistical Analysis of Backscatter Values

---

## Next Steps

### SAR Feature Generation

* VV/VH Ratio
* VH/VV Ratio
* Backscatter Difference (VV − VH)
* Backscatter Sum (VV + VH)

### Texture Feature Extraction

* GLCM Contrast
* GLCM Homogeneity
* GLCM Entropy
* GLCM Correlation
* GLCM Energy

### Optical Data Processing

* Sentinel-2 Data Download
* Atmospheric Correction
* Cloud Masking
* NDVI Generation
* EVI Generation
* SAVI Generation

### Future Work

* Water Cloud Model (WCM) Development
* Biomass Estimation
* Machine Learning Model Development
* Validation and Accuracy Assessment
