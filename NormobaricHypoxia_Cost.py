#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Normobaric Hypoxia Training Budget Calculator with Physiological Parameters

This script calculates the weekly and total costs associated with using Compressed Air, Nitrogen, and Oxygen
gases for a normobaric hypoxia training program based on user inputs.
It also calculates physiological parameters for an average adult at different altitudes.

Author: Diego Malpica
Date: 25-09-2024

Assumptions:
- The primary gas used is compressed air from the air tank (21% O₂, 78% N₂).
- Nitrogen is added to the compressed air to simulate altitude (hypoxic conditions).
- 100% Oxygen is provided during the recovery phase.
- The main gas consumption is from the air tank.
- The machine uses tanks with a pressure of 2600 psi and volume of 6.5 m³.
- Physiological responses are based on average adult data and standard physiological models.
"""

def get_positive_float(prompt, default_value=None):
    """
    Prompt the user to enter a positive float value.
    Continues prompting until a valid positive float is entered.
    Press Enter to keep the default value.
    """
    while True:
        try:
            value = input(prompt).strip()
            if value == '':
                return default_value  # User wants to keep default
            value = float(value)
            if value <= 0:
                print("Please enter a positive value or press Enter to keep the default.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a numeric value or press Enter to keep the default.")

def get_positive_int(prompt, default_value=None):
    """
    Prompt the user to enter a positive integer value.
    Continues prompting until a valid positive integer is entered.
    Press Enter to keep the default value.
    """
    while True:
        try:
            value = input(prompt).strip()
            if value == '':
                return default_value  # User wants to keep default
            value = int(value)
            if value <= 0:
                print("Please enter a positive integer or press Enter to keep the default.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter an integer or press Enter to keep the default.")

# [Previous code sections remain unchanged]

def calculate_physiological_parameters(altitude_ft, duration_minutes):
    """
    Calculate physiological parameters for an average adult at a given altitude and duration.

    Parameters:
    - altitude_ft: Altitude in feet.
    - duration_minutes: Duration at altitude in minutes.

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
    PaO2 = PiO2 - (5)  # Approximate alveolar-arterial gradient
    SaO2 = 100 * (PaO2 ** 3) / (PaO2 ** 3 + 150 ** 3)

    # Adjust ventilation rate based on hypoxic ventilatory response
    # Updated model: Ventilation increases by 100% per 1,000 m above 1,500 m
    altitude_above_1500_m = max(0, altitude_m - 1500)
    ventilation_increase_factor = (altitude_above_1500_m / 1000) * 1.0  # 100% increase per 1,000 m
    ventilation_rate = AVG_VENTILATION_RATE_SL * (1 + ventilation_increase_factor)

    # Cap ventilation rate to a maximum value (e.g., 60 L/min) to avoid unrealistic values
    ventilation_rate = min(ventilation_rate, 60)

    # Adjust heart rate based on hypoxia
    # Simplified model: HR increases by 1 bpm per 100 m above 1,000 m
    altitude_above_1000_m = max(0, altitude_m - 1000)
    heart_rate_increase = altitude_above_1000_m / 100
    heart_rate = AVG_HEART_RATE_SL + heart_rate_increase

    # Duration effect (acclimatization is not considered for short durations)
    # For sessions less than 1 hour, acute responses are considered

    return {
        "altitude_ft": altitude_ft,
        "altitude_m": altitude_m,
        "pressure_at_altitude_mmHg": pressure_at_altitude,
        "PaO2_mmHg": PaO2,
        "SaO2_percent": SaO2,
        "ventilation_rate_L_per_min": ventilation_rate,
        "heart_rate_bpm": heart_rate,
        "duration_minutes": duration_minutes
    }

# [Rest of the code remains unchanged]


def calculate_gas_consumption(
    students_per_week,
    weeks,
    session_duration_minutes,
    ventilation_rate_L_per_min,
    price_air_m3,
    price_nitrogen_m3,
    price_oxygen_m3,
    recovery_duration_minutes,
    contingency_percentage=0.10
):
    """
    Calculate gas consumption and costs for the training program.

    Returns a dictionary with consumption and cost details.
    """
    # Number of sessions per week
    sessions_per_week = students_per_week  # Assuming one session per student per week

    # Total sessions
    total_sessions = sessions_per_week * weeks

    # Air consumption per session per student (main gas consumption)
    total_air_consumed_per_session_m3 = (ventilation_rate_L_per_min * session_duration_minutes) / 1000  # Convert to m³

    # Nitrogen consumption (to adjust the mixture for altitude simulation)
    # Assuming a percentage of nitrogen is added per session
    total_nitrogen_consumed_per_session_m3 = total_air_consumed_per_session_m3 * 0.05  # Adjust as needed

    # Oxygen consumption during recovery (100% O₂)
    total_oxygen_consumed_per_session_m3 = (ventilation_rate_L_per_min * recovery_duration_minutes) / 1000  # Convert to m³

    # Weekly consumption
    weekly_air_consumption_m3 = total_air_consumed_per_session_m3 * sessions_per_week
    weekly_nitrogen_consumption_m3 = total_nitrogen_consumed_per_session_m3 * sessions_per_week
    weekly_oxygen_consumption_m3 = total_oxygen_consumed_per_session_m3 * sessions_per_week

    # Total consumption over training period
    total_air_consumption_m3 = weekly_air_consumption_m3 * weeks
    total_nitrogen_consumption_m3 = weekly_nitrogen_consumption_m3 * weeks
    total_oxygen_consumption_m3 = weekly_oxygen_consumption_m3 * weeks

    # Costs
    weekly_cost_air = weekly_air_consumption_m3 * price_air_m3
    weekly_cost_nitrogen = weekly_nitrogen_consumption_m3 * price_nitrogen_m3
    weekly_cost_oxygen = weekly_oxygen_consumption_m3 * price_oxygen_m3

    total_cost_air = weekly_cost_air * weeks
    total_cost_nitrogen = weekly_cost_nitrogen * weeks
    total_cost_oxygen = weekly_cost_oxygen * weeks

    total_cost = total_cost_air + total_cost_nitrogen + total_cost_oxygen
    total_cost_with_contingency = total_cost * (1 + contingency_percentage)

    return {
        "weekly_air_consumption_m3": weekly_air_consumption_m3,
        "weekly_nitrogen_consumption_m3": weekly_nitrogen_consumption_m3,
        "weekly_oxygen_consumption_m3": weekly_oxygen_consumption_m3,
        "total_air_consumption_m3": total_air_consumption_m3,
        "total_nitrogen_consumption_m3": total_nitrogen_consumption_m3,
        "total_oxygen_consumption_m3": total_oxygen_consumption_m3,
        "weekly_cost_air_COP": weekly_cost_air,
        "weekly_cost_nitrogen_COP": weekly_cost_nitrogen,
        "weekly_cost_oxygen_COP": weekly_cost_oxygen,
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
    DEFAULT_STUDENTS_PER_WEEK = 20
    DEFAULT_WEEKS = 26
    DEFAULT_SESSION_DURATION_MINUTES = 20
    DEFAULT_VENTILATION_RATE_L_PER_MIN = 40  # L/min due to hypoxia
    DEFAULT_RECOVERY_DURATION_MINUTES = 5    # Duration of recovery breathing 100% O₂
    DEFAULT_PRICE_AIR_M3 = 17853       # COP/m³
    DEFAULT_PRICE_NITROGEN_M3 = 17838  # COP/m³
    DEFAULT_PRICE_OXYGEN_M3 = 19654    # COP/m³
    DEFAULT_CONTINGENCY_PERCENTAGE = 0.10  # 10%
    DEFAULT_ALTITUDE_FT = 25000        # Simulated altitude
    DEFAULT_DURATION_AT_ALTITUDE_MINUTES = 20  # Duration at altitude

    # User inputs
    students_per_week = get_positive_int(
        f"Enter the number of students per week (default is {DEFAULT_STUDENTS_PER_WEEK}): ",
        DEFAULT_STUDENTS_PER_WEEK
    )

    weeks = get_positive_int(
        f"Enter the number of weeks for the training program (default is {DEFAULT_WEEKS}): ",
        DEFAULT_WEEKS
    )

    session_duration_minutes = get_positive_float(
        f"Enter the duration of each session in minutes (default is {DEFAULT_SESSION_DURATION_MINUTES}): ",
        DEFAULT_SESSION_DURATION_MINUTES
    )

    recovery_duration_minutes = get_positive_float(
        f"Enter the recovery duration in minutes (default is {DEFAULT_RECOVERY_DURATION_MINUTES}): ",
        DEFAULT_RECOVERY_DURATION_MINUTES
    )

    altitude_ft = get_positive_float(
        f"Enter the simulated altitude in feet (default is {DEFAULT_ALTITUDE_FT} ft): ",
        DEFAULT_ALTITUDE_FT
    )

    duration_at_altitude_minutes = get_positive_float(
        f"Enter the duration at altitude in minutes (default is {DEFAULT_DURATION_AT_ALTITUDE_MINUTES}): ",
        DEFAULT_DURATION_AT_ALTITUDE_MINUTES
    )

    # Calculate physiological parameters
    physio_params = calculate_physiological_parameters(altitude_ft, duration_at_altitude_minutes)

    # Update ventilation rate based on physiological parameters
    ventilation_rate_L_per_min = physio_params['ventilation_rate_L_per_min']

    price_air_m3 = get_positive_float(
        f"Enter the price of Compressed Air per m³ in COP (default is {DEFAULT_PRICE_AIR_M3}): ",
        DEFAULT_PRICE_AIR_M3
    )

    price_nitrogen_m3 = get_positive_float(
        f"Enter the price of Nitrogen per m³ in COP (default is {DEFAULT_PRICE_NITROGEN_M3}): ",
        DEFAULT_PRICE_NITROGEN_M3
    )

    price_oxygen_m3 = get_positive_float(
        f"Enter the price of Oxygen per m³ in COP (default is {DEFAULT_PRICE_OXYGEN_M3}): ",
        DEFAULT_PRICE_OXYGEN_M3
    )

    contingency_percentage = get_positive_float(
        f"Enter the contingency percentage as a decimal (default is {DEFAULT_CONTINGENCY_PERCENTAGE}): ",
        DEFAULT_CONTINGENCY_PERCENTAGE
    )

    # Call the calculation function
    results = calculate_gas_consumption(
        students_per_week,
        weeks,
        session_duration_minutes,
        ventilation_rate_L_per_min,
        price_air_m3,
        price_nitrogen_m3,
        price_oxygen_m3,
        recovery_duration_minutes,
        contingency_percentage
    )

    # Output physiological parameters
    print("\n=== Physiological Parameters ===\n")
    print(f"Simulated Altitude: {physio_params['altitude_ft']} ft ({physio_params['altitude_m']:.2f} m)")
    print(f"Atmospheric Pressure at Altitude: {physio_params['pressure_at_altitude_mmHg']:.2f} mmHg")
    print(f"Partial Pressure of Oxygen (PaO2): {physio_params['PaO2_mmHg']:.2f} mmHg")
    print(f"Arterial Oxygen Saturation (SaO2): {physio_params['SaO2_percent']:.2f}%")
    print(f"Ventilation Rate: {physio_params['ventilation_rate_L_per_min']:.2f} L/min")
    print(f"Heart Rate: {physio_params['heart_rate_bpm']:.2f} bpm")
    print(f"Duration at Altitude: {physio_params['duration_minutes']} minutes")

    # Output budget results
    print("\n=== Budget Summary ===\n")
    print(f"Students per Week: {students_per_week}")
    print(f"Total Weeks: {weeks}")
    print(f"Session Duration: {session_duration_minutes} minutes")
    print(f"Ventilation Rate: {ventilation_rate_L_per_min:.2f} L/min")
    print(f"Recovery Duration: {recovery_duration_minutes} minutes")
    print(f"Contingency Percentage: {contingency_percentage * 100:.1f}%\n")

    print(f"Weekly Air Consumption: {results['weekly_air_consumption_m3']:.2f} m³")
    print(f"Weekly Nitrogen Consumption: {results['weekly_nitrogen_consumption_m3']:.2f} m³")
    print(f"Weekly Oxygen Consumption: {results['weekly_oxygen_consumption_m3']:.2f} m³")
    print(f"Total Air Consumption: {results['total_air_consumption_m3']:.2f} m³")
    print(f"Total Nitrogen Consumption: {results['total_nitrogen_consumption_m3']:.2f} m³")
    print(f"Total Oxygen Consumption: {results['total_oxygen_consumption_m3']:.2f} m³\n")

    print(f"Weekly Cost for Air: {results['weekly_cost_air_COP']:.2f} COP")
    print(f"Weekly Cost for Nitrogen: {results['weekly_cost_nitrogen_COP']:.2f} COP")
    print(f"Weekly Cost for Oxygen: {results['weekly_cost_oxygen_COP']:.2f} COP")
    print(f"Total Cost for Air: {results['total_cost_air_COP']:.2f} COP")
    print(f"Total Cost for Nitrogen: {results['total_cost_nitrogen_COP']:.2f} COP")
    print(f"Total Cost for Oxygen: {results['total_cost_oxygen_COP']:.2f} COP\n")
    print(f"Total Cost (without contingency): {results['total_cost_COP']:.2f} COP")
    print(f"Total Cost (with {contingency_percentage * 100:.1f}% contingency): {results['total_cost_with_contingency_COP']:.2f} COP")

    print("\n=== End of Calculation ===")

if __name__ == "__main__":
    main()
