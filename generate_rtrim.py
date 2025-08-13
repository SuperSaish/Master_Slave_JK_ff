import csv
import re
import argparse

def check_condition(input_value, condition_str):
    """Checks if the given input_value matches the condition string from CSV."""
    condition_str = condition_str.strip().strip('_')
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
    gen1_4_1, gen1_4_2, gen1_4_3 = [], [], []
    gen5_1, gen5_2, gen5_3 = [], [], []

    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if check_condition(input_proc, row['PROC']) and check_condition(input_rel, row['REL']):
                gen1_4_1.append(row['GEN1_4_1'])
                gen1_4_2.append(row['GEN1_4_2'])
                gen1_4_3.append(row['GEN1_4_3'])
                gen5_1.append(row['GEN5_1'])
                gen5_2.append(row['GEN5_2'])
                gen5_3.append(row['GEN5_3'])

    return gen1_4_1, gen1_4_2, gen1_4_3, gen5_1, gen5_2, gen5_3

def main():
    parser = argparse.ArgumentParser(description="Generate rtrim_threshold.txt from RTRIM.csv")
    parser.add_argument('-PROC', type=str, required=True, help='PROC value')
    parser.add_argument('-REL', type=str, required=True, help='REL value')
    parser.add_argument('-CSV', type=str, default='RTRIM.csv', help='CSV file path')
    parser.add_argument('-OUT', type=str, default='rtrim_threshold.txt', help='Output file path')
    args = parser.parse_args()

    g1_1, g1_2, g1_3, g5_1, g5_2, g5_3 = find_matching_rows(args.CSV, args.PROC, args.REL)

    with open(args.OUT, "w") as file:
        file.write(f'set RTRIM_THRESHOLD_1_GEN1_4 "{" ".join(g1_1)}"\n')
        file.write(f'set RTRIM_THRESHOLD_2_GEN1_4 "{" ".join(g1_2)}"\n')
        file.write(f'set RTRIM_THRESHOLD_3_GEN1_4 "{" ".join(g1_3)}"\n')
        file.write(f'set RTRIM_THRESHOLD_1_GEN5 "{" ".join(g5_1)}"\n')
        file.write(f'set RTRIM_THRESHOLD_2_GEN5 "{" ".join(g5_2)}"\n')
        file.write(f'set RTRIM_THRESHOLD_3_GEN5 "{" ".join(g5_3)}"\n')

    print(f"Generated {args.OUT} successfully.")

if __name__ == "__main__":
    main()
