import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# --- Define Input Variables (Antecedents) ---
# Universe range for speech_comfort: 0 (very cold) to 4 (hot)
speech_comfort = ctrl.Antecedent(np.arange(0, 5, 1), 'speech_comfort')
# Universe range for temperature: 16°C to 32°C
temperature = ctrl.Antecedent(np.arange(16, 33, 1), 'temperature')
# Universe range for humidity: 30% to 80%
humidity = ctrl.Antecedent(np.arange(30, 81, 1), 'humidity')

# --- Define Output Variables (Consequents) ---
# Universe range for temp_adjust: -5°C (decrease large) to 5°C (increase large)
temp_adjust = ctrl.Consequent(np.arange(-7, 6, 1), 'temp_adjust')
# Universe range for fan_speed: 0 (off) to 5 (high)
fan_speed = ctrl.Consequent(np.arange(0, 6, 1), 'fan_speed')

# --- Membership Functions for Input Variables ---

# Speech Comfort Level (numerical mapping from voice input)
speech_comfort['very_cold'] = fuzz.trimf(speech_comfort.universe, [0, 0, 1])
speech_comfort['cold'] = fuzz.trimf(speech_comfort.universe, [0, 1, 2])
speech_comfort['comfortable'] = fuzz.trimf(speech_comfort.universe, [1, 2, 3])
speech_comfort['warm'] = fuzz.trimf(speech_comfort.universe, [2, 3, 4])
speech_comfort['hot'] = fuzz.trimf(speech_comfort.universe, [3, 4, 4])

# Temperature
temperature['very_cold'] = fuzz.trimf(temperature.universe, [16, 16, 18])
temperature['cold'] = fuzz.trimf(temperature.universe, [17, 18.5, 20])
temperature['cool'] = fuzz.trimf(temperature.universe, [19, 20.5, 22])
temperature['comfortable'] = fuzz.trimf(temperature.universe, [21, 22.5, 24])
temperature['warm'] = fuzz.trimf(temperature.universe, [23, 24.5, 26])
temperature['hot'] = fuzz.trimf(temperature.universe, [25, 27, 29])
temperature['very_hot'] = fuzz.trimf(temperature.universe, [28, 32, 32])

# Humidity
humidity['low'] = fuzz.trimf(humidity.universe, [30, 30, 45])
humidity['normal'] = fuzz.trimf(humidity.universe, [40, 55, 70])
humidity['high'] = fuzz.trimf(humidity.universe, [60, 80, 80])

# --- Membership Functions for Output Variables ---

# Temperature Adjustment
temp_adjust['decrease_extreme']     = fuzz.trimf(temp_adjust.universe, [-7, -7, -6])
temp_adjust['decrease_very_large']  = fuzz.trimf(temp_adjust.universe, [-7, -6, -5])
temp_adjust['decrease_large']       = fuzz.trimf(temp_adjust.universe, [-6, -5, -4])
temp_adjust['decrease_medium']      = fuzz.trimf(temp_adjust.universe, [-5, -4, -2])
temp_adjust['decrease_small']       = fuzz.trimf(temp_adjust.universe, [-3, -2, -1])
temp_adjust['no_change']            = fuzz.trimf(temp_adjust.universe, [-1,  0,  1])
temp_adjust['increase_small']       = fuzz.trimf(temp_adjust.universe, [ 1,  2,  3])
temp_adjust['increase_medium']      = fuzz.trimf(temp_adjust.universe, [ 2,  4,  5])
temp_adjust['increase_large']       = fuzz.trimf(temp_adjust.universe, [ 4,  5,  6])
temp_adjust['increase_very_large']  = fuzz.trimf(temp_adjust.universe, [ 5,  6,  7])
temp_adjust['increase_extreme']     = fuzz.trimf(temp_adjust.universe, [ 6,  7,  7])

# Fan Speed
fan_speed['off'] = fuzz.trimf(fan_speed.universe, [0, 0, 1])
fan_speed['low'] = fuzz.trimf(fan_speed.universe, [1, 2, 3])
fan_speed['medium'] = fuzz.trimf(fan_speed.universe, [2, 3, 4])
fan_speed['high'] = fuzz.trimf(fan_speed.universe, [4, 5, 5])

speech_levels  = ['very_cold','cold','comfortable','warm','hot']
temp_levels    = ['very_cold','cold','cool','comfortable','warm','hot','very_hot']
humidity_levels= ['low','normal','high']

def decide_temp_adjust(speech, temp):
    """Return one of the 11 temp_adjust labels."""
    if speech == 'hot':
        if   temp == 'very_hot': return 'decrease_extreme'
        elif temp == 'hot':      return 'decrease_very_large'
        elif temp == 'warm':     return 'decrease_large'
        elif temp == 'comfortable': return 'decrease_medium'
        elif temp in ['cool','cold']: return 'decrease_small'
        else:                   return 'no_change'
    if speech == 'warm':
        if   temp in ['very_hot','hot']: return 'decrease_large'
        elif temp == 'warm':             return 'decrease_medium'
        elif temp == 'comfortable':      return 'decrease_small'
        elif temp in ['cool','cold']:    return 'increase_small'
        else:                            return 'increase_medium'
    if speech == 'comfortable':
        if   temp in ['very_hot','hot']: return 'decrease_small'
        elif temp in ['very_cold','cold']: return 'increase_small'
        else:                            return 'no_change'
    if speech == 'cold':
        if   temp in ['very_cold','cold']: return 'increase_large'
        elif temp == 'cool':               return 'increase_medium'
        elif temp == 'comfortable':        return 'no_change'
        else:                              return 'no_change'
    if speech == 'very_cold':
        if   temp == 'very_cold':          return 'increase_extreme'
        elif temp == 'cold':               return 'increase_very_large'
        elif temp == 'cool':               return 'increase_large'
        elif temp == 'comfortable':        return 'increase_medium'
        else:                              return 'no_change'

def decide_fan_speed(speech, hum):
    """Return one of the 4 fan_speed labels."""
    if speech == 'hot':  return 'high'   if hum == 'high' else 'medium'
    if speech == 'warm': return 'medium' if hum != 'low'  else 'low'
    if speech == 'comfortable':
        return 'medium' if hum == 'high' else 'low'
    if speech == 'cold':      return 'low' if hum != 'low' else 'off'
    if speech == 'very_cold': return 'off'
    return 'low'

rule_list = []
for s in speech_levels:
    for t in temp_levels:
        for h in humidity_levels:
            ta_label = decide_temp_adjust(s, t)
            fs_label = decide_fan_speed(s, h)
            rule_list.append(
                ctrl.Rule(speech_comfort[s] & temperature[t] & humidity[h],
                          (temp_adjust[ta_label], fan_speed[fs_label]))
            )

print(f"Generated {len(rule_list)} rules.")  # Should print 105


# --- Control System Creation ---
# Creates the fuzzy control system and simulation engine.
ac_ctrl = ctrl.ControlSystem(rule_list)
ac_sim = ctrl.ControlSystemSimulation(ac_ctrl)

class FuzzyModel:
    def __init__(self):
        self.ac_ctrl = ac_ctrl  # use existing global controller
        # no need to store `ac_sim`, recreate each time
    
    @staticmethod
    def determine_comfort_numerical_value(input_text):
        lower_text = input_text.lower()
        if any(keyword in lower_text for keyword in ['hot', 'boiling', 'sweating']):
            return 4
        if any(keyword in lower_text for keyword in ['warm', 'muggy']):
            return 3
        if any(keyword in lower_text for keyword in ['cold', 'chilly']):
            return 1
        if any(keyword in lower_text for keyword in ['freezing', 'shivering', 'very cold']):
            return 0
        return 2

    def calculate_fuzzy_output(self, user_comfort_input_text, current_room_temperature, current_humidity):
        # Get the numerical comfort value based on voice input
        comfort_numerical_value = self.determine_comfort_numerical_value(user_comfort_input_text)

        # Set the inputs for the skfuzzy simulation
        ac_sim.input['speech_comfort'] = comfort_numerical_value
        ac_sim.input['temperature'] = current_room_temperature
        ac_sim.input['humidity'] = current_humidity

        temp_adjust_output = 0.0
        fan_speed_output = 0

        try:
            # Compute the fuzzy logic
            ac_sim.compute()

            # Retrieve the defuzzified outputs with checks for existence
            if 'temp_adjust' in ac_sim.output:
                temp_adjust_output = round(ac_sim.output['temp_adjust'], 1)
            else:
                # This should ideally not be hit with a comprehensive rule base, but kept for robustness
                print("Warning: 'temp_adjust' not found in fuzzy output. Defaulting to 0.0.")

            if 'fan_speed' in ac_sim.output:
                fan_speed_output = round(ac_sim.output['fan_speed'])
            else:
                # This should ideally not be hit with a comprehensive rule base, but kept for robustness
                print("Warning: 'fan_speed' not found in fuzzy output. Defaulting to 0.")

        except ValueError as e:
            # This can still happen if the computation itself fails for some fundamental reason (e.g., input out of universe)
            print(f"Error computing fuzzy logic: {e}. Returning default values.")

        return temp_adjust_output, fan_speed_output