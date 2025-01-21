# Normobaric Hypoxia Training Budget Calculator

## Description

The **Normobaric Hypoxia Training Budget Calculator** is a Python script designed to estimate the gas consumption and budget required for a normobaric hypoxia training program. It calculates the weekly and total costs associated with using compressed air, nitrogen, and oxygen gases, and integrates physiological parameters to adjust ventilation rates based on altitude.

This tool is ideal for aviation training centers, sports facilities, or any organization that conducts hypoxia training sessions simulating high-altitude conditions.

## Features

- **Interactive Menu System**: Easy-to-use interface with the following options:
  1. Calculate Physiological Parameters
  2. Calculate Gas Consumption and Costs
  3. Calculate Training Capacity from Cylinder Volumes
  4. Run All Calculations

- **Physiological Integration**: Calculates physiological parameters for an average adult at different altitudes, including:
  - Atmospheric pressure (mmHg)
  - Partial pressure of oxygen (PaO2)
  - Arterial oxygen saturation (SaO2)
  - Ventilation rate (L/min)
  - Heart rate (bpm)

- **Gas Consumption Analysis**: 
  - Calculates consumption for compressed air, nitrogen, and oxygen
  - Provides weekly and total consumption in cubic meters
  - Accounts for standard gas cylinder sizes (Type T, Type K, Type G at 200 bar pressure)
  - Estimates maximum training capacity based on available gas volumes

- **Customizable Parameters**: Allows users to input or accept default values for:
  - Number of students per week (default: 20)
  - Number of weeks for the training program (default: 26)
  - Session duration (default: 20 minutes)
  - Recovery duration (default: 5 minutes)
  - Simulated altitude (default: 25,000 ft)
  - Gas prices (Compressed Air, Nitrogen, Oxygen)
  - Contingency percentage (default: 10%)
  - Gas cylinder volumes

## Installation

### Requirements

- Python 3.x
- Standard Python libraries (sys)

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/strikerdlm/hypoxia-budget-calculator.git
   ```

## Usage

Run the script using Python:

```bash
python GasCalc_updated.py
```

Follow the interactive menu to perform desired calculations. The program allows you to:
- Calculate physiological parameters at specific altitudes
- Estimate gas consumption and associated costs
- Determine training capacity based on available gas cylinders
- Run all calculations in sequence

## Author

Diego Malpica
