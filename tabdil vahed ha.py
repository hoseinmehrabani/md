def convert_length(value, from_unit, to_unit):
    length_units = {
        'm': 1.0,
        'cm': 0.01,
        'km': 1000.0,
        'in': 0.0254,
        'ft': 0.3048,
        'yd': 0.9144
    }
    return value * length_units[from_unit] / length_units[to_unit]

def convert_weight(value, from_unit, to_unit):
    weight_units = {
        'kg': 1.0,
        'g': 0.001,
        'lb': 0.453592,
        'oz': 0.0283495
    }
    return value * weight_units[from_unit] / weight_units[to_unit]

def convert_temperature(value, from_unit, to_unit):
    if from_unit == 'C' and to_unit == 'F':
        return (value * 9/5) + 32
    elif from_unit == 'F' and to_unit == 'C':
        return (value - 32) * 5/9
    elif from_unit == 'C' and to_unit == 'K':
        return value + 273.15
    elif from_unit == 'K' and to_unit == 'C':
        return value - 273.15
    elif from_unit == 'F' and to_unit == 'K':
        return (value - 32) * 5/9 + 273.15
    elif from_unit == 'K' and to_unit == 'F':
        return (value - 273.15) * 9/5 + 32
    else:
        return value  # If units are the same

# نمونه استفاده
print(convert_length(10, 'm', 'cm'))  # 1000.0
print(convert_weight(1, 'kg', 'lb'))   # 2.20462
print(convert_temperature(100, 'C', 'F'))  # 212.0
