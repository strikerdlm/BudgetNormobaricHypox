#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Normobaric Hypoxia Training Budget Calculator with Physiological Parameters

This script calculates the weekly and total costs associated with using Compressed Air, Nitrogen, and Oxygen
gases for a normobaric hypoxia training program based on user inputs.
It also calculates physiological parameters for an average adult at different altitudes.

Author: Diego Malpica
Date: 04-10-2024

Assumptions:
- The primary gas used is compressed air from the air tank (21% O₂, 78% N₂).
- Nitrogen is added to the compressed air to simulate altitude (hypoxic conditions).
- 100% Oxygen is provided during the recovery phase.
- Physiological responses are based on average adult data and standard physiological models.
"""

import sys

def get_user_input(prompt: str, default_value=None, value_type=float):
    """
    Prompt the user to enter a value, allowing for a default if no input is given.
    
    Parameters:
    - prompt: The prompt text to display to the user.
    - default_value: Default value if the user presses Enter.
    - value_type: The expected type of the input value (float, int).
    
    Returns:
    - The user input value, converted to the appropriate type.
    """
    while True:
        try:
            value = input(prompt).strip()
            if value == '':
                return default_value
            return value_type(value)
        except ValueError:
            print(f"Invalid input. Please enter a valid {value_type.__name__}.")

def calculate_physiological_parameters(altitude_ft: float) -> dict:
    """
    Calculate physiological parameters for an average adult at a given altitude.

    Parameters:
    - altitude_ft: Altitude in feet.

    Returns:
    - Dictionary containing physiological parameters.
    """
    # Constants
    SEA_LEVEL_PRESSURE = 760  # mmHg
    AVG_VENTILATION_RATE_SL = 6  # L/min at sea level (resting)
    AVG_HEART_RATE_SL = 70  # bpm at sea level (resting)

    # Calculate atmospheric pressure at altitude
    altitude_m = altitude_ft * 0.3048  # Convert feet to meters
    pressure_at_altitude = SEA_LEVEL_PRESSURE * (1 - (2.25577e-5 * altitude_m)) ** 5.25588  # Barometric formula

    # Calculate inspired oxygen partial pressure (PiO2)
    FiO2 = 0.2095  # Fraction of inspired oxygen in dry air
    PiO2 = (pressure_at_altitude - 47) * FiO2  # Subtract water vapor pressure (47 mmHg)

    # Estimate arterial oxygen saturation (SaO2)
    PaO2 = PiO2 - 5  # Approximate alveolar-arterial gradient
    SaO2 = 100 * (PaO2 ** 3) / (PaO2 ** 3 + 150 ** 3)

    # Adjust ventilation rate based on hypoxic ventilatory response
    altitude_above_1500_m = max(0, altitude_m - 1500)
    ventilation_increase_factor = (altitude_above_1500_m / 1000)  # 100% increase per 1,000 m
    ventilation_rate = AVG_VENTILATION_RATE_SL * (1 + ventilation_increase_factor)
    ventilation_rate = min(ventilation_rate, 60)  # Cap ventilation rate to avoid unrealistic values

    # Adjust heart rate based on hypoxia
    altitude_above_1000_m = max(0, altitude_m - 1000)
    heart_rate_increase = altitude_above_1000_m / 100
    heart_rate = AVG_HEART_RATE_SL + heart_rate_increase

    return {
        "altitude_ft": altitude_ft,
        "altitude_m": altitude_m,
        "pressure_at_altitude_mmHg": pressure_at_altitude,
        "PaO2_mmHg": PaO2,
        "SaO2_percent": SaO2,
        "ventilation_rate_L_per_min": ventilation_rate,
        "heart_rate_bpm": heart_rate
    }

def calculate_gas_consumption(sessions_per_week: int, weeks: int, session_duration_minutes: float, ventilation_rate: float, recovery_duration_minutes: float, price_air: float, price_nitrogen: float, price_oxygen: float, contingency_percentage: float = 0.10) -> dict:
    """
    Calculate gas consumption and costs for the training program.
    
    Parameters:
    - sessions_per_week: Number of sessions per week.
    - weeks: Number of weeks.
    - session_duration_minutes: Duration of each session in minutes.
    - ventilation_rate: Ventilation rate in L/min.
    - recovery_duration_minutes: Duration of recovery in minutes.
    - price_air: Price of compressed air per m3.
    - price_nitrogen: Price of nitrogen per m3.
    - price_oxygen: Price of oxygen per m3.
    - contingency_percentage: Additional cost contingency.
    
    Returns:
    - Dictionary with consumption and cost details.
    """
    # Calculate per-session consumption in m3
    air_consumed_per_session = (ventilation_rate * session_duration_minutes) / 1000  # Convert to m3
    nitrogen_consumed_per_session = air_consumed_per_session * 0.05  # Additional nitrogen
    oxygen_consumed_per_session = (ventilation_rate * recovery_duration_minutes) / 1000  # During recovery

    # Weekly consumption
    weekly_air_consumption = air_consumed_per_session * sessions_per_week
    weekly_nitrogen_consumption = nitrogen_consumed_per_session * sessions_per_week
    weekly_oxygen_consumption = oxygen_consumed_per_session * sessions_per_week

    # Total consumption over training period
    total_air_consumption = weekly_air_consumption * weeks
    total_nitrogen_consumption = weekly_nitrogen_consumption * weeks
    total_oxygen_consumption = weekly_oxygen_consumption * weeks

    # Costs
    total_cost_air = total_air_consumption * price_air
    total_cost_nitrogen = total_nitrogen_consumption * price_nitrogen
    total_cost_oxygen = total_oxygen_consumption * price_oxygen

    total_cost = total_cost_air + total_cost_nitrogen + total_cost_oxygen
    total_cost_with_contingency = total_cost * (1 + contingency_percentage)

    return {
        "weekly_air_consumption_m3": weekly_air_consumption,
        "weekly_nitrogen_consumption_m3": weekly_nitrogen_consumption,
        "weekly_oxygen_consumption_m3": weekly_oxygen_consumption,
        "total_air_consumption_m3": total_air_consumption,
        "total_nitrogen_consumption_m3": total_nitrogen_consumption,
        "total_oxygen_consumption_m3": total_oxygen_consumption,
        "total_cost_air_COP": total_cost_air,
        "total_cost_nitrogen_COP": total_cost_nitrogen,
        "total_cost_oxygen_COP": total_cost_oxygen,
        "total_cost_COP": total_cost,
        "total_cost_with_contingency_COP": total_cost_with_contingency
    }

def main():
    """
    Main function to execute the Budget Calculator.
    """
    print("=== Normobaric Hypoxia Training Budget Calculator ===\n")

    # Default values
    DEFAULTS = {
        "students_per_week": 20,
        "weeks": 26,
        "session_duration_minutes": 20,
        "recovery_duration_minutes": 5,
        "price_air": 17853,
        "price_nitrogen": 17838,
        "price_oxygen": 19654,
        "contingency_percentage": 0.10,
        "altitude_ft": 25000
    }

    # User inputs
    students_per_week = get_user_input(f"Enter the number of students per week (default is {DEFAULTS['students_per_week']}): ", DEFAULTS['students_per_week'], int)
    weeks = get_user_input(f"Enter the number of weeks for the training program (default is {DEFAULTS['weeks']}): ", DEFAULTS['weeks'], int)
    session_duration_minutes = get_user_input(f"Enter the duration of each session in minutes (default is {DEFAULTS['session_duration_minutes']}): ", DEFAULTS['session_duration_minutes'])
    recovery_duration_minutes = get_user_input(f"Enter the recovery duration in minutes (default is {DEFAULTS['recovery_duration_minutes']}): ", DEFAULTS['recovery_duration_minutes'])
    altitude_ft = get_user_input(f"Enter the simulated altitude in feet (default is {DEFAULTS['altitude_ft']} ft): ", DEFAULTS['altitude_ft'])

    # Calculate physiological parameters
    physio_params = calculate_physiological_parameters(altitude_ft)
    ventilation_rate = physio_params['ventilation_rate_L_per_min']

    # Additional user inputs
    price_air = get_user_input(f"Enter the price of Compressed Air per m3 in COP (default is {DEFAULTS['price_air']}): ", DEFAULTS['price_air'])
    price_nitrogen = get_user_input(f"Enter the price of Nitrogen per m3 in COP (default is {DEFAULTS['price_nitrogen']}): ", DEFAULTS['price_nitrogen'])
    price_oxygen = get_user_input(f"Enter the price of Oxygen per m3 in COP (default is {DEFAULTS['price_oxygen']}): ", DEFAULTS['price_oxygen'])
    contingency_percentage = get_user_input(f"Enter the contingency percentage as a decimal (default is {DEFAULTS['contingency_percentage']}): ", DEFAULTS['contingency_percentage'])

    # Calculate gas consumption and costs
    results = calculate_gas_consumption(
        students_per_week, weeks, session_duration_minutes, ventilation_rate,
        recovery_duration_minutes, price_air, price_nitrogen, price_oxygen, contingency_percentage
    )

    # Display results
    print("\n=== Physiological Parameters ===\n")
    for key, value in physio_params.items():
        if isinstance(value, float):
            print(f"{key.replace('_', ' ').title()}: {value:.2f}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")

    print("\n=== Budget Summary ===\n")
    for key, value in results.items():
        if isinstance(value, float):
            print(f"{key.replace('_', ' ').title()}: {value:.2f}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")

    print("\n=== End of Calculation ===")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCalculation interrupted by user.")
        sys.exit(0)
