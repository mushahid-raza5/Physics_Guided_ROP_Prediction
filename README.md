# Drilling Rate of Penetration (ROP) Prediction Using Statistical Modeling

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

A comprehensive statistical analysis project that models and predicts **Rate of Penetration (ROP)** in oil &amp; gas drilling operations using real-world well data. The project applies classical regression techniques alongside domain-specific petroleum engineering models to identify key drilling parameters that influence ROP.

> **Course:** Statistics for Data Science — University of Chicago

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Dataset](#dataset)
- [Methodology](#methodology)
- [Key Results](#key-results)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Technologies Used](#technologies-used)
- [Reports](#reports)
- [Author](#author)
- [License](#license)

---

## 🎯 Project Overview

Rate of Penetration (ROP) is one of the most critical performance indicators in drilling engineering. Optimizing ROP directly reduces drilling time and costs. This project investigates the statistical relationships between drilling parameters and ROP using data from a real well (**USROP_A 3 N-SH-F-15d**).

### Objectives

1. **Explore** the relationships between drilling parameters and ROP through comprehensive EDA.
2. **Build** multiple regression models (Log-MLR and Bingham) to predict ROP.
3. **Compare** model performance and identify the most influential drilling parameters.
4. **Validate** model assumptions using diagnostic tests (VIF, Breusch–Pagan).

---

## 📊 Dataset

| Property        | Detail                             |
|-----------------|------------------------------------|
| **Source**       | USROP_A 3 N-SH-F-15d well data    |
| **Records**     | ~53,000 observations               |
| **Features**    | 13 columns (12 predictors + index) |
| **Target**      | Rate of Penetration (ROP)          |
| **Location**    | `data/`                            |

### Feature Descriptions

| Feature          | Unit   | Description                 |
|------------------|--------|-----------------------------|
| `MD`             | m      | Measured Depth              |
| `WOB`            | kkgf   | Weight on Bit               |
| `SPPA`           | kPa    | Standpipe Pressure          |
| `Torque`         | kN·m   | Torque                      |
| `ROP`            | m/h    | Rate of Penetration (target)|
| `RPM`            | rpm    | Rotations Per Minute        |
| `TFLO`           | L/min  | Total Flow Rate             |
| `Mud Weight`     | g/cm³  | Mud Weight                  |
| `Hole Diameter`  | mm     | Hole Diameter               |
| `HKLD`           | kkgf   | Hookload                    |
| `TVD`            | m      | True Vertical Depth         |
| `Gamma gAPI`     | gAPI   | Gamma Ray                   |

### Summary Statistics

|            |   Min   |   Max    |  Mean   |   Std   |
|------------|---------|----------|---------|---------|
| **ROP**    |   0.79  |  99.21   |  21.58  |   9.63  |
| **WOB**    |   0.005 |  19.86   |   6.18  |   4.66  |
| **RPM**    |   0.00  | 140.35   | 130.63  |  19.35  |
| **Torque** |   1.10  |  36.49   |  19.15  |   7.89  |
| **TFLO**   |1083.31  |4453.12   |2933.60  |1090.26  |

---

## 🔬 Methodology

### 1. Exploratory Data Analysis (EDA)
- Distribution analysis of ROP (histogram)
- Scatter plots of key drilling parameters vs. ROP:
  - **WOB vs ROP** — Weight on Bit influence
  - **RPM vs ROP** — Rotational speed influence
  - **Torque vs ROP** — Torque influence
  - **TFLO vs ROP** — Flow rate influence

### 2. Statistical Diagnostics
- **Variance Inflation Factor (VIF)** — Multicollinearity detection
- **Breusch–Pagan Test** — Heteroscedasticity assessment
- **Correlation Analysis** — Feature interdependencies

### 3. Regression Models

| Model             | Technique                                          | Purpose                          |
|--------------------|----------------------------------------------------|----------------------------------|
| **Log-MLR**        | Log-transformed Multiple Linear Regression (OLS)   | General statistical modeling     |
| **Bingham Model**  | Nonlinear curve fitting (`scipy.optimize.curve_fit`)| Domain-specific ROP prediction   |

### 4. Model Comparison
- Overlay plots comparing predicted vs. observed ROP
- Fixed-variable analysis (e.g., ROP vs RPM at median WOB)
- Visual assessment of model fit quality

---

## 📈 Key Results

- The **Bingham drilling model** captures the nonlinear relationship between WOB, RPM, and ROP effectively.
- **WOB** and **RPM** are the most statistically significant predictors of ROP.
- The **Log-MLR** model provides a good baseline but tends to overestimate ROP at extreme parameter values.
- Diagnostic tests confirm the presence of heteroscedasticity, supporting the use of log-transformed models.

---

## 📁 Repository Structure

```
Statistics-For-Data-Science-Final-Project/
│
├── README.md                                    # Project documentation
├── LICENSE                                      # MIT License
├── requirements.txt                             # Python dependencies
├── .gitignore                                   # Git ignore rules
│
├── data/
│   └── USROP_A 3 N-SH-F-15d - Final.csv        # Raw drilling dataset (~53K records)
│
├── notebooks/
│   └── Final_Project_Statistics.ipynb           # Main analysis notebook
│
└── reports/
    ├── Mushahid_Raza_Final_Project.pdf           # Final project report
    └── Mushahid_Raza_Final_Project.pptx          # Presentation slides
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Jupyter Notebook or JupyterLab

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mushahid-raza5/Drilling-ROP-Statistical-Analysis.git
   cd Drilling-ROP-Statistical-Analysis
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate        # macOS/Linux
   venv\Scripts\activate           # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the notebook**
   ```bash
   jupyter notebook notebooks/Final_Project_Statistics.ipynb
   ```

> **Note:** The notebook references the dataset using a relative path. If you encounter a file-not-found error, update the `file_path` variable in the first code cell to point to `../data/USROP_A 3 N-SH-F-15d - Final.csv`.

---

## 🛠️ Technologies Used

| Technology         | Purpose                        |
|--------------------|--------------------------------|
| **Python 3.13**    | Core programming language      |
| **NumPy**          | Numerical computing            |
| **Pandas**         | Data manipulation &amp; analysis   |
| **Matplotlib**     | Data visualization             |
| **Seaborn**        | Statistical visualization      |
| **Statsmodels**    | OLS regression &amp; diagnostics   |
| **SciPy**          | Nonlinear curve fitting        |
| **Jupyter**        | Interactive notebook environment|

---

## 📄 Reports

- 📕 **[Final Report (PDF)](reports/Mushahid_Raza_Final_Project.pdf)** — Comprehensive written analysis
- 📊 **[Presentation (PPTX)](reports/Mushahid_Raza_Final_Project.pptx)** — Summary slide deck

---

## 👤 Author

**Mushahid Raza**
- 🎓 University of Chicago
- 🔗 [GitHub Profile](https://github.com/mushahid-raza5)

---

## 📝 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- University of Chicago — Statistics for Data Science course
- USROP drilling data providers
- Open-source Python scientific computing community
