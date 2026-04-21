# Dataset: USROP_A 3 N-SH-F-15d

## Overview

Real-time drilling data from the **USROP_A 3 N-SH-F-15d** well, containing approximately **53,000 observations** of surface and downhole drilling parameters recorded at high frequency.

## Columns

| Column         | Unit   | Description                  |
|----------------|--------|------------------------------|
| `Sr No.`       | —      | Row index                    |
| `MD`           | m      | Measured Depth               |
| `WOB`          | kkgf   | Weight on Bit                |
| `SPPA`         | kPa    | Standpipe Pressure           |
| `Torque`       | kN·m   | Torque                       |
| `ROP`          | m/h    | Rate of Penetration (target) |
| `RPM`          | rpm    | Rotations Per Minute         |
| `TFLO`         | L/min  | Total Flow Rate              |
| `Mud Weight`   | g/cm³  | Mud Weight                   |
| `Hole Diameter`| mm     | Hole Diameter                |
| `HKLD`         | kkgf   | Hookload                     |
| `TVD`          | m      | True Vertical Depth          |
| `Gamma gAPI`   | gAPI   | Gamma Ray                    |

## Notes

- The CSV file has two header rows: row 1 contains column names, row 2 contains units. When loading with pandas, use `skiprows=[1]` to skip the units row.
- The bit diameter (`Db = 444.5 mm`) is constant for this well and is used as a parameter in the Bingham ROP model.
