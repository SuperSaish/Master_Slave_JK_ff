import csv
import re
import argparse

def check_condition(input_value, condition_str):
    """Checks if the given input_value matches the condition string from CSV."""
    condition_str = condition_str.strip()
    condition_str = condition_str.strip('_')
    input_value = input_value.strip('_')

    if condition_str.upper() == "NONE":
        return True

    try:
        input_value = float(input_value)
    except ValueError:
        return str(input_value.lower()) == str(condition_str.lower())

    try:
        if float(condition_str) == input_value:
            return True
    except ValueError:
        pass

    single_match = re.match(r'(>=|<=|>|<|==)\s*(\d+(\.\d+)?)', condition_str)
    if single_match:
        operator, number = single_match.group(1), float(single_match.group(2))
        return eval(f"{input_value} {operator} {number}")

    compound_match = re.findall(r'(>=|<=|>|<|==)\s*(\d+(\.\d+)?)', condition_str)
    if compound_match and '&' in condition_str:
        return all(eval(f"{input_value} {op} {float(num)}") for op, num, _ in compound_match)

    return False

def find_matching_rows(csv_file_path, input_proc, input_rel):
    """Returns GEN1_4 and GEN5 values for matching rows."""
    #gen1_4_1, gen1_4_2, gen1_4_3 = [], [], []
    #gen5_1, gen5_2, gen5_3 = [], [], []
    Gen41, Gen42, Gen43, Gen51, Gen52, Gen53 = [] , [] , [] , [] ,[] ,[] 
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if check_condition(input_proc, row[0]) and check_condition(input_rel, row[1]):
                #matching_parameters[row[1],row[2],row[3],row[4],row[5],row[6].append(row[1])
                Gen41.append(row[2])
                Gen42.append(row[3])
                Gen43.append(row[4])
                Gen51.append(row[5])
                Gen52.append(row[6])
                Gen53.append(row[7])

    return Gen41, Gen42, Gen43, Gen51, Gen52, Gen53

def main():
    parser = argparse.ArgumentParser(description="Generate rtrim_threshold.txt from RTRIM.csv")
    parser.add_argument('-PROC', type=str, required=True, help='Argument PROC')
    parser.add_argument('-REL', type=str, required=True, help='Argument REL')
    csv_file='RTRIM.csv'
    args = parser.parse_args()

    Gen41, Gen42, Gen43, Gen51, Gen52, Gen53= find_matching_rows(csv_file, args.PROC, args.REL)
    #global matching_parameters
    #matching_parameters = {'Gen41': [], 'Gen42': [], 'Gen43': [], 'Gen51': [], 'Gen52': [], 'Gen53': []}
    #find_matching_rows(csv_file, args.PROC, args.REL)


    
    with open("param_thresh_set.def", "w") as file:
        file.write(f"set RTRIM_THRESHOLD_1_GEN1_4 0x{' '.join(['Gen41'])}")
        file.write(f"set RTRIM_THRESHOLD_2_GEN1_4 0x{' '.join(['Gen42'])}")
        file.write(f"set RTRIM_THRESHOLD_3_GEN1_4 0x{' '.join(['Gen43'])}")
        file.write(f"set RTRIM_THRESHOLD_1_GEN5 0x{' '.join(['Gen51'])}")
        file.write(f"set RTRIM_THRESHOLD_2_GEN5 0x{' '.join(['Gen52'])}")
        file.write(f"set RTRIM_THRESHOLD_3_GEN5 0x{' '.join(['Gen53'])}")

    #print(f" Generated successfully.")

if __name__ == "__main__":
    main()
