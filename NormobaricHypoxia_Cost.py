#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Normobaric Hypoxia Training Budget Calculator with Physiological Parameters

This script calculates the weekly and total costs associated with using Compressed Air, Nitrogen, and Oxygen
gases for a normobaric hypoxia training program based on user inputs.
It also calculates physiological parameters for an average adult at different altitudes.

Author: Diego Malpica
Date: 21-01-2025

Assumptions:
- The primary gas used is compressed air from the air tank (21% O₂, 78% N₂).
- Nitrogen is added to the compressed air to simulate altitude (hypoxic conditions).
- 100% Oxygen is provided during the recovery phase.
- Physiological responses are based on average adult data and standard physiological models.
- Standard gas cylinder sizes: Type T (50L), Type K (45L), Type G (50L) at 200 bar pressure.
"""

import sys

# Default values for all calculations
DEFAULTS = {
    "students_per_week": 20,
    "weeks": 26,
    "session_duration_minutes": 20,
    "recovery_duration_minutes": 5,
    "price_air": 17853,
    "price_nitrogen": 17838,
    "price_oxygen": 19654,
    "contingency_percentage": 0.10,
    "altitude_ft": 25000,
    # Standard gas cylinder volumes (m3) at 200 bar
    "air_cylinder_volume": 10,  # Type T (50L)
    "nitrogen_cylinder_volume": 9,  # Type K (45L)
    "oxygen_cylinder_volume": 10,  # Type G (50L)
}

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

def calculate_student_capacity(air_cylinder_volume: float, nitrogen_cylinder_volume: float, oxygen_cylinder_volume: float, 
                            session_duration_minutes: float, ventilation_rate: float, recovery_duration_minutes: float) -> dict:
    """
    Calculate how many students can be trained with given gas cylinder volumes.
    
    Parameters:
    - air_cylinder_volume: Volume of compressed air cylinder in m3
    - nitrogen_cylinder_volume: Volume of nitrogen cylinder in m3
    - oxygen_cylinder_volume: Volume of oxygen cylinder in m3
    - session_duration_minutes: Duration of each session in minutes
    - ventilation_rate: Ventilation rate in L/min
    - recovery_duration_minutes: Duration of recovery in minutes
    
    Returns:
    - Dictionary with capacity details
    """
    # Calculate consumption per student session
    air_per_session = (ventilation_rate * session_duration_minutes) / 1000  # m3
    nitrogen_per_session = air_per_session * 0.05  # m3
    oxygen_per_session = (ventilation_rate * recovery_duration_minutes) / 1000  # m3
    
    # Calculate maximum students for each gas type
    max_students_air = int(air_cylinder_volume / air_per_session)
    max_students_nitrogen = int(nitrogen_cylinder_volume / nitrogen_per_session)
    max_students_oxygen = int(oxygen_cylinder_volume / oxygen_per_session)
    
    # The limiting factor will be the minimum of all three
    max_students = min(max_students_air, max_students_nitrogen, max_students_oxygen)
    
    return {
        "max_students_total": max_students,
        "max_students_air": max_students_air,
        "max_students_nitrogen": max_students_nitrogen,
        "max_students_oxygen": max_students_oxygen,
        "air_per_session_m3": air_per_session,
        "nitrogen_per_session_m3": nitrogen_per_session,
        "oxygen_per_session_m3": oxygen_per_session
    }

def display_menu():
    """
    Display the main menu options.
    """
    print("\n=== Normobaric Hypoxia Training Calculator Menu ===")
    print("1. Calculate Physiological Parameters")
    print("2. Calculate Gas Consumption and Costs")
    print("3. Calculate Training Capacity from Cylinder Volumes")
    print("4. Run All Calculations")
    print("5. Exit")
    print("===============================================")

def get_basic_inputs() -> dict:
    """
    Get the basic inputs needed for most calculations.
    """
    inputs = {}
    inputs["session_duration_minutes"] = get_user_input(
        f"Enter the duration of each session in minutes (default is {DEFAULTS['session_duration_minutes']}): ", 
        DEFAULTS['session_duration_minutes']
    )
    inputs["recovery_duration_minutes"] = get_user_input(
        f"Enter the recovery duration in minutes (default is {DEFAULTS['recovery_duration_minutes']}): ", 
        DEFAULTS['recovery_duration_minutes']
    )
    inputs["altitude_ft"] = get_user_input(
        f"Enter the simulated altitude in feet (default is {DEFAULTS['altitude_ft']} ft): ", 
        DEFAULTS['altitude_ft']
    )
    return inputs

def run_physiological_calculation():
    """
    Run only the physiological parameters calculation.
    """
    inputs = get_basic_inputs()
    physio_params = calculate_physiological_parameters(inputs["altitude_ft"])
    
    print("\n=== Physiological Parameters ===\n")
    for key, value in physio_params.items():
        if isinstance(value, float):
            print(f"{key.replace('_', ' ').title()}: {value:.2f}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")
    return physio_params

def run_consumption_calculation():
    """
    Run only the gas consumption and cost calculation.
    """
    inputs = get_basic_inputs()
    students_per_week = get_user_input(
        f"Enter the number of students per week (default is {DEFAULTS['students_per_week']}): ", 
        DEFAULTS['students_per_week'], 
        int
    )
    weeks = get_user_input(
        f"Enter the number of weeks for the training program (default is {DEFAULTS['weeks']}): ", 
        DEFAULTS['weeks'], 
        int
    )
    
    # Get gas prices
    price_air = get_user_input(
        f"Enter the price of Compressed Air per m3 in COP (default is {DEFAULTS['price_air']}): ", 
        DEFAULTS['price_air']
    )
    price_nitrogen = get_user_input(
        f"Enter the price of Nitrogen per m3 in COP (default is {DEFAULTS['price_nitrogen']}): ", 
        DEFAULTS['price_nitrogen']
    )
    price_oxygen = get_user_input(
        f"Enter the price of Oxygen per m3 in COP (default is {DEFAULTS['price_oxygen']}): ", 
        DEFAULTS['price_oxygen']
    )
    contingency_percentage = get_user_input(
        f"Enter the contingency percentage as a decimal (default is {DEFAULTS['contingency_percentage']}): ", 
        DEFAULTS['contingency_percentage']
    )
    
    physio_params = calculate_physiological_parameters(inputs["altitude_ft"])
    ventilation_rate = physio_params['ventilation_rate_L_per_min']
    
    results = calculate_gas_consumption(
        students_per_week, weeks, inputs["session_duration_minutes"], ventilation_rate,
        inputs["recovery_duration_minutes"], price_air, price_nitrogen, price_oxygen, contingency_percentage
    )
    
    print("\n=== Budget Summary ===\n")
    for key, value in results.items():
        if isinstance(value, float):
            print(f"{key.replace('_', ' ').title()}: {value:.2f}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")
    return results

def run_capacity_calculation():
    """
    Run only the cylinder capacity calculation.
    """
    inputs = get_basic_inputs()
    print("\n=== Gas Cylinder Configuration ===")
    print("Standard cylinder sizes: Type T (50L), Type K (45L), Type G (50L) at 200 bar pressure")
    
    air_cylinder_volume = get_user_input(
        f"Enter the Compressed Air cylinder volume in m3 (default is {DEFAULTS['air_cylinder_volume']}): ", 
        DEFAULTS['air_cylinder_volume']
    )
    nitrogen_cylinder_volume = get_user_input(
        f"Enter the Nitrogen cylinder volume in m3 (default is {DEFAULTS['nitrogen_cylinder_volume']}): ", 
        DEFAULTS['nitrogen_cylinder_volume']
    )
    oxygen_cylinder_volume = get_user_input(
        f"Enter the Oxygen cylinder volume in m3 (default is {DEFAULTS['oxygen_cylinder_volume']}): ", 
        DEFAULTS['oxygen_cylinder_volume']
    )
    
    physio_params = calculate_physiological_parameters(inputs["altitude_ft"])
    ventilation_rate = physio_params['ventilation_rate_L_per_min']
    
    capacity_results = calculate_student_capacity(
        air_cylinder_volume, nitrogen_cylinder_volume, oxygen_cylinder_volume,
        inputs["session_duration_minutes"], ventilation_rate, inputs["recovery_duration_minutes"]
    )
    
    print("\n=== Cylinder Capacity Analysis ===\n")
    for key, value in capacity_results.items():
        if isinstance(value, float):
            print(f"{key.replace('_', ' ').title()}: {value:.2f}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")
    return capacity_results

def run_all_calculations():
    """
    Run all calculations in sequence.
    """
    physio_params = run_physiological_calculation()
    consumption_results = run_consumption_calculation()
    capacity_results = run_capacity_calculation()
    return physio_params, consumption_results, capacity_results

def main():
    """
    Main function to execute the Budget Calculator with menu system.
    """
    print("=== Normobaric Hypoxia Training Budget Calculator ===")
    print("= by Diego Malpica =\n")
    
    while True:
        display_menu()
        choice = get_user_input("Enter your choice (1-5): ", 1, int)
        
        if choice == 1:
            run_physiological_calculation()
        elif choice == 2:
            run_consumption_calculation()
        elif choice == 3:
            run_capacity_calculation()
        elif choice == 4:
            run_all_calculations()
        elif choice == 5:
            print("\nThank you for using the calculator. Goodbye!")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please select a number between 1 and 5.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCalculation interrupted by user.")
        sys.exit(0)
