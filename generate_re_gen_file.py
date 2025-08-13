import csv
import re
import argparse

def check_condition(input_value, condition_str):
    #For checking the proc values

    condition_str = condition_str.strip()
    condition_str = condition_str.strip('_')
    input_value = input_value.strip('_')
    if condition_str == "NONE":
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

def find_matching_rows(csv_file_path, input_value_proc, input_value_raw, input_value_pma, input_value_fw, input_value_rel):
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 2 and check_condition(input_value_proc, row[2]) and check_condition(input_value_raw, row[3]) and check_condition(input_value_pma, row[4]) and check_condition(input_value_fw, row[5]) and check_condition(input_value_rel, row[6]):
                matching_parameters[row[0]].append(row[1])

def main():
    parser = argparse.ArgumentParser(description="Process five arguments.")
    parser.add_argument('-PMA', type=str, required=True, help='Argument PMA')
    parser.add_argument('-PROC', type=str, required=True, help='Argument PROC')
    parser.add_argument('-RAW', type=str, required=True, help='Argument RAW')
    parser.add_argument('-FW', type=str, required=True, help='Argument FW')
    parser.add_argument('-REL', type=str, required=True, help='Argument REL')
    csv_file = 'trial_csv.csv'
    args = parser.parse_args()

    global matching_parameters
    matching_parameters = {'RAW': [], 'PMA': [], 'REL': [], 'ARCH': [], 'DM_RANGE_CTRL': []}
    find_matching_rows(csv_file, args.PROC, args.RAW, args.PMA, args.FW, args.REL)
    print(f"{matching_parameters}")
    r = "Madhu"
    fruit = "mango"

    with open("example_re_gen.txt", "w") as file:
        file.write(f"""#!/bin/csh
set echo
set process='x351_e32_tsmc3pff'
set ARCH='{' '.join(matching_parameters['ARCH'])}'
set REL='{' '.join(matching_parameters['REL'])}'
set RAW='{' '.join(matching_parameters['RAW'])}'
set PMA='{' '.join(matching_parameters['PMA'])}'
set BUF_9BIT=''
set DATA_DEL_2='DATA_DEL_2'
set DM_RANGE_CTRL='{' '.join(matching_parameters['DM_RANGE_CTRL'])}'
set TC=''
cp -pf startup_off_cal_adapt.asm startup_off_cal_adapt.asm.BAK
grep -v '^INSTR_CP_OR.*REG_RESET_MASK' startup_off_cal_adapt.asm >! startup_off_cal_adapt.asm.MASKED; mv startup_off_cal_adapt.asm.MASKED startup_off_cal_adapt.asm
source re_gen_fw_all_32K
${{root_dir}}/pcs_raw/firmware/bin/sram_32K.pl sds_pcs_raw_ext_rom.bin
cp -pf sds_pcs_raw_ext_sram.bin sds_pcs_raw_mem_sram.fw
${{root_dir}}/pcs_raw/firmware/bin/sram_32K.pl sds_pcs_raw_ext_rom.fastsim
cp -pf sds_pcs_raw_ext_sram.bin sds_pcs_raw_mem_sram_fastsim.fw
cp -pf sds_pcs_raw_mem_sram.fw ${{root_dir}}/pma/tech/${{process}}/ipxact/sds_pcs_raw_mem_sram.fw
cp -pf sds_pcs_raw_mem_sram_fastsim.fw ${{root_dir}}/pma/tech/${{process}}/ipxact/sds_pcs_raw_mem_sram_fastsim.fw
cp -pf ${{root_dir}}/pma/tech/${{process}}/ipxact/sds_pcs_raw_* ../../../${{process}}/current_snapshot
unset ARCH
unset REL
unset RAW
unset PMA
unset BUF_9BIT
unset DATA_DEL_2
unset DM_RANGE_CTRL
unset TC
cp -pf ../../../startup_off_cal_adapt.asm ../startup_off_cal_adapt.asm.mask_rmvd
cp -pf ../../../startup_off_cal_adapt.asm.BAK ../../../startup_off_cal_adapt.asm
cp -pf ../../../startup_off_cal_adapt.asm.BAK ../startup_off_cal_adapt.asm
cp -pf ../../../startup_off_cal_adapt.asm.BAK ../../../${{process}}/current_snapshot/startup_off_cal_adapt.asm
../../../../bin/gen_ecc.pl sds_pcs_raw_ext_rom.bin
cp -pf sds_pcs_raw_mem_sram.fw sds_pcs_raw_mem_sram_cr_para.fw
cp -pf sds_pcs_raw_mem_sram_cr_para.fw sds_pcs_raw_mem_sram_side_load_ecc.bin ${{root_dir}}/pma/tech/${{process}}/ipxact/
cp -pf sds_pcs_raw_mem_sram_cr_para.fw sds_pcs_raw_mem_sram_side_load_ecc.bin ../../../${{process}}/current_snapshot
python3 ../../../../bin/fw_mod.py
cd ..
cp -pf sds_pcs_raw_mem_rst.annotated.asic ${{root_dir}}/pcs_raw/firmware/code/${{process}}/current_snapshot/ -avr
cp -pf sds_pcs_raw_mem_rst.annotated.cosim ${{root_dir}}/pcs_raw/firmware/code/${{process}}/current_snapshot/ -avr
cp -pf sds_pcs_raw_mem_rst.rom.fw_labels ${{root_dir}}/pcs_raw/firmware/code/${{process}}/current_snapshot/ -avr
cp -pf sds_pcs_raw_mem_rst.sram.fw_labels ${{root_dir}}/pcs_raw/firmware/code/${{process}}/current_snapshot/ -avr 

unset echo""")

if __name__ == "__main__":
    main()
    

