import rasterio
from rasterio.merge import merge
from pathlib import Path
from collections import defaultdict
import re
import numpy as np
import pandas as pd

# =====================================================
# INPUT FOLDER
# =====================================================

input_folder = Path(r"add path of the folder ")

# =====================================================
# OUTPUT FOLDER
# =====================================================

output_folder = input_folder / "Mosaic"
output_folder.mkdir(exist_ok=True)

# =====================================================
# LOG AND STATISTICS FILES
# =====================================================

log_file = output_folder / "mosaic_log.txt"
stats_file = output_folder / "mosaic_statistics.csv"

statistics = []

# =====================================================
# FIND TIFF FILES
# =====================================================

all_files = list(input_folder.glob("*.tif"))

print(f"\nFound {len(all_files)} TIFF files")

if len(all_files) == 0:
    raise FileNotFoundError("No TIFF files found!")

# =====================================================
# GROUP FILES BY DATE
# =====================================================

date_groups = defaultdict(list)

for file in all_files:

    match = re.search(r'_(\d{8})T', file.name)

    if match:
        date = match.group(1)
        date_groups[date].append(file)

# =====================================================
# DISPLAY DATES
# =====================================================

print("\nDetected Acquisition Dates:")

for date, files in sorted(date_groups.items()):

    print(f"\nDate: {date}")

    for f in files:
        print("   ", f.name)

# =====================================================
# MOSAIC FUNCTION
# =====================================================

def create_mosaic(files, output_file, date):

    print("\n" + "=" * 70)
    print(f"PROCESSING DATE : {date}")
    print("=" * 70)

    src_files = []

    # -----------------------------------------
    # Open Files
    # -----------------------------------------

    for file in files:

        src = rasterio.open(file)

        print(f"\nOpening: {file.name}")
        print(" CRS   :", src.crs)
        print(" Bands :", src.count)
        print(" Size  :", src.width, "x", src.height)

        src_files.append(src)

    # -----------------------------------------
    # CRS CHECK
    # -----------------------------------------

    crs_list = [src.crs for src in src_files]

    if len(set(crs_list)) > 1:
        raise ValueError(
            f"CRS mismatch detected for date {date}"
        )

    # -----------------------------------------
    # MOSAIC
    # -----------------------------------------

    mosaic, transform = merge(
        src_files,
        method="first"
    )

    # -----------------------------------------
    # METADATA
    # -----------------------------------------

    meta = src_files[0].meta.copy()

    meta.update({
        "driver": "GTiff",
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": transform,
        "count": mosaic.shape[0],
        "dtype": mosaic.dtype,
        "compress": "lzw",
        "BIGTIFF": "YES"
    })

    # -----------------------------------------
    # SAVE MOSAIC
    # -----------------------------------------

    with rasterio.open(output_file, "w", **meta) as dst:
        dst.write(mosaic)

    for src in src_files:
        src.close()

    print(f"\nSaved: {output_file}")

    # -----------------------------------------
    # VERIFY OUTPUT
    # -----------------------------------------

    with rasterio.open(output_file) as check:

        arr = check.read(1).astype("float32")

        nodata = check.nodata

        if nodata is not None:
            arr[arr == nodata] = np.nan

        min_val = np.nanmin(arr)
        max_val = np.nanmax(arr)
        mean_val = np.nanmean(arr)
        std_val = np.nanstd(arr)

        print("\nVerification")
        print("-" * 40)
        print("CRS       :", check.crs)
        print("Width     :", check.width)
        print("Height    :", check.height)
        print("Min       :", min_val)
        print("Max       :", max_val)
        print("Mean      :", mean_val)
        print("Std Dev   :", std_val)

        statistics.append({
            "Date": date,
            "Width": check.width,
            "Height": check.height,
            "Min": min_val,
            "Max": max_val,
            "Mean": mean_val,
            "Std_Dev": std_val
        })

    # -----------------------------------------
    # LOG FILE
    # -----------------------------------------

    with open(log_file, "a") as log:

        log.write(
            f"{date} -> {output_file.name}\n"
        )

# =====================================================
# CREATE MOSAICS
# =====================================================

for date, files in sorted(date_groups.items()):

    if len(files) < 2:

        print(
            f"\nSkipping {date} "
            f"(only {len(files)} tile found)"
        )
        continue

    output_file = output_folder / f"Mosaic_{date}.tif"

    create_mosaic(
        files,
        output_file,
        date
    )

# =====================================================
# SAVE STATISTICS
# =====================================================

if statistics:

    df = pd.DataFrame(statistics)

    df.to_csv(
        stats_file,
        index=False
    )

    print("\nStatistics saved:")
    print(stats_file)

# =====================================================
# FINISHED
# =====================================================

print("\n" + "=" * 70)
print("ALL MOSAICS COMPLETED")
print("=" * 70)
