#!/usr/bin/env python3
import json
import math
import re

# Ask for machine parameters to get key configuration settings
# 1. Distance between belt pivot points:
#   Measure directly or measure between shafts - pulley diameter
# 2. Belt length in home position

converted_machine_width_mm = None
calculated_x_minmax_mm = None
calculated_machine_height_mm = None
calculated_y_minmax_mm = None
input_machine_width = None
input_home_belt_length = None
converted_belt_length_mm = None
input_user_units = None

while True:
    input_machine_width = input(
        f"Enter distance between belt pivot points: ")
    input_multiplier = 1.0
    try:
        if input_machine_width.lower().endswith('in'):
            input_multiplier = 25.4
            input_machine_width = input_machine_width.lower().removesuffix("in").strip()
        if input_machine_width.lower().endswith('mm'):
            input_machine_width = input_machine_width.lower().removesuffix("mm").strip()
        if re.search("^\d+ \d+/\d+", input_machine_width):  # fraction
            (whole, frac) = input_machine_width.split(" ")
            whole = int(whole)
            (num, den) = map(float, frac.split("/"))
            converted_machine_width_mm = (whole + num/den) * input_multiplier
            break
        elif re.search("^\d+\.\d+", input_machine_width):  # decimal
            converted_machine_width_mm = float(
                input_machine_width) * input_multiplier
            break
        elif re.search("^\d+", input_machine_width):  # integer
            converted_machine_width_mm = int(
                input_machine_width) * input_multiplier
            break
    except Exception as e:
        print(e)
        print(
            f"Try again. Enter a value like '600mm', '600', '34.5 in', '34 1/2 in'.")

while True:
    input_pulley_adjustment = input(
        f"Enter optional pulley diameter adjustment: ")
    input_multiplier = 1.0
    try:
        if input_pulley_adjustment.lower().endswith('in'):
            input_multiplier = 25.4
            input_pulley_adjustment = input_pulley_adjustment.lower().removesuffix("in").strip()
        if input_pulley_adjustment.lower().endswith('mm'):
            input_pulley_adjustment = input_pulley_adjustment.lower().removesuffix("mm").strip()
        if input_pulley_adjustment == "":
            break
        if re.search("^\d+ \d+/\d+", input_pulley_adjustment):  # fraction
            (whole, frac) = input_pulley_adjustment.split(" ")
            whole = int(whole)
            (num, den) = map(float, frac.split("/"))
            converted_machine_width_mm -= (whole + num/den) * input_multiplier
            break
        elif re.search("^\d+\.\d+", input_pulley_adjustment):  # decimal
            converted_machine_width_mm -= float(
                input_pulley_adjustment) * input_multiplier
            break
        elif re.search("^\d+", input_pulley_adjustment):  # integer
            converted_machine_width_mm -= int(
                input_pulley_adjustment) * input_multiplier
            break
    except Exception as e:
        print(e)
        print(
            f"Try again. Enter a value like '6mm', '6', '0.5 in', '1/2 in'.")

calculated_x_minmax_mm = converted_machine_width_mm/2.0
print(f"Machine width: {converted_machine_width_mm} mm")
print(f"X min/max: -{calculated_x_minmax_mm} - {calculated_x_minmax_mm}")

while True:
    input_home_belt_length = input(
        f"Enter belt length from pivot point to pen point: ")
    input_multiplier = 1.0
    if input_home_belt_length.lower().endswith('in'):
        input_multiplier = 25.4
        input_home_belt_length = input_home_belt_length.lower().removesuffix("in").strip()
        if input_home_belt_length.lower().endswith('mm'):
            input_home_belt_length = input_home_belt_length.lower().removesuffix("mm").strip()
    try:
        if re.search("^\d+ \d+/\d+", input_home_belt_length):  # fraction
            (whole, frac) = input_home_belt_length.split(" ")
            whole = int(whole)
            (num, den) = map(float, frac.split("/"))
            converted_belt_length_mm = (whole + num/den) * input_multiplier
            break
        elif re.search("^\d+\.\d+", input_home_belt_length):  # decimal
            converted_belt_length_mm = float(
                input_home_belt_length) * input_multiplier
            break
        elif re.search("^\d+", input_home_belt_length):  # integer
            converted_belt_length_mm = int(
                input_home_belt_length) * input_multiplier
            break
    except Exception as e:
        print(e)
        print(
            f"Try again. Enter a value like '600mm', '600', '34.5 in', '34 1/2 in'.")

print(f"Belt length: {converted_belt_length_mm} mm")

# belt^2 = height^2 + (width/2)^2 ==> height = sqrt(belt^2 - (width/2)^2)
calculated_machine_height_mm = math.sqrt(
    converted_belt_length_mm**2 - calculated_x_minmax_mm**2)
print(f"Calculated drawing area height: {calculated_machine_height_mm} mm")
calculated_y_minmax_mm = calculated_machine_height_mm/2.0
print(f"Y min/max: -{calculated_y_minmax_mm} - {calculated_y_minmax_mm}")

config = {
    "POLARGRAPH_MAX_BELT_LEN": converted_belt_length_mm,
    "X_BED_SIZE": converted_machine_width_mm,
    "Y_BED_SIZE": calculated_machine_height_mm,
    "MANUAL_X_HOME_POS": 0,
    "MANUAL_Y_HOME_POS": -calculated_y_minmax_mm,
}

print(json.dumps(config, sort_keys=True, indent=2))
