#!/bin/csh -f
#

# ===========================
# Logging helpers
# ===========================
alias write_log  'echo "[INFO] \!*"'
alias write_warn 'echo "[WARN] \!*"'
alias write_err  'echo "[ERR]  \!*"'

# ===========================
# Step0: Check env & args
# ===========================
if (! $?SDS_ROOT) then
    write_err "SDS_ROOT not set. Please export SDS_ROOT before running."
    exit 1
endif

if ($#argv < 8) then
    write_err "Usage: $0 <process> <PROC> <PMA> <RAW> <FW> <REL> <HF_SIGDET> <header_reg_addr_def_new>"
    exit 1
endif

set sds_root                    = $SDS_ROOT
set process                     = $1
set PROC			= $2
set PMA				= $3
set RAW				= $4
set FW				= $5
set REL				= $6
set HF_SIGDET			= $7
set header_reg_addr_def_new	= $8

write_log "SDS_ROOT = $sds_root"
write_log "Process  = $process"
write_log "PROC     = $PROC"
write_log "PMA  = $PMA"
write_log "RAW  = $RAW"
write_log "FW  = $FW"
write_log "REL  = $REL"
write_log "HF_SIGDET =  $HF_SIGDET"
write_log "REG_ADDR_DEF = ${header_reg_addr_def_new}"

echo "All inputs are correct? (Enter 1 for Yes, anything else for No)"
  set correct_condition=$<
  if ($correct_condition == 1) then
      echo "success"
      # continue  # would go to next loop iteration
  else
      echo "try again"
      exit  # This will stop the script immediately
 endif


# ===========================
# Step1: Check testchip dir
# ===========================

set testchip_dir = "$sds_root/pma/tech/$process/ipxact/testchip"
if (! -d $testchip_dir) then
    write_log "Creating testchip dir: $testchip_dir"
    mkdir -p $testchip_dir
else
    write_log "Testchip dir exists: $testchip_dir"
endif


# ===========================
# Step2: Sync ASM file
# ===========================
set path_asm = "$sds_root/pcs_raw/firmware/code/startup_off_cal_adapt.asm"
write_log "Syncing ASM file: $path_asm"
if ($FW == 2.8_5) then
	p4 sync -f ${path_asm}"#"148
else if ($FW == 2.9) then
	p4 sync -f ${path_asm}"#"158
else if ($FW == 2.8_6) then
	p4 sync -f ${path_asm}"#"156
else if ($FW == 2.8_9) then
	p4 sync -f ${path_asm}"#"157
else if ($FW == 3.0) then
	p4 sync -f ${path_asm}"#"160
else if ($FW == 2.9_1) then
	cp -f $sds_root/pcs_raw/firmware/code/dev/2_9_1/startup_off_cal_adapt.asm ${path_asm}
endif


# ===========================
# Step3: Firmware header sync & update & xls sheets copy
# ===========================
set path_fw_header = "$sds_root/pcs_raw/firmware/code/$process/firmware.header"
echo $path_fw_header


if ($FW == 3.1 | $FW == 2.9_1) then
	if (`echo "$PMA >= 3.1" | bc` == 1) then
		if ($HF_SIGDET == 0) then
			cp -rf $sds_root/../0.4/*xls $sds_root/pcs_raw/firmware/code/$process
        		./fw_header.csh $PMA $RAW $FW 0.4 0.57 $header_reg_addr_def_new $process
		else if ($HF_SIGDET == 1) then
			cp -rf $sds_root/../1.4/*xls $sds_root/pcs_raw/firmware/code/$process
        		./fw_header.csh $PMA $RAW $FW 1.4 0.57 $header_reg_addr_def_new $process
       		endif

	else if (`echo "$PMA < 3.1" | bc` == 1) then
		if ($HF_SIGDET == 0) then
			cp -rf $sds_root/../0.63/*xls $sds_root/pcs_raw/firmware/code/$process
        		./fw_header.csh $PMA $RAW $FW 0.63 0.57 $header_reg_addr_def_new $process
		else if ($HF_SIGDET == 1) then
			cp -rf $sds_root/../0.8/*xls $sds_root/pcs_raw/firmware/code/$process
        		./fw_header.csh $PMA $RAW $FW 0.8 0.57 $header_reg_addr_def_new $process
		endif
	endif
endif
	
if ($FW == 3.0 | $FW == 2.9 | $FW == 2.8_9) then
	if (`echo "$PMA >= 3.1" | bc` == 1) then
		if ($HF_SIGDET == 0) then
			cp -rf $sds_root/../0.3/*xls $sds_root/pcs_raw/firmware/code/$process
        		./fw_header.csh $PMA $RAW $FW 0.3 0.56 $header_reg_addr_def_new $process
		else if ($HF_SIGDET == 1) then
			cp -rf $sds_root/../1.2/*xls $sds_root/pcs_raw/firmware/code/$process
        		./fw_header.csh $PMA $RAW $FW 1.2 0.56 $header_reg_addr_def_new $process
       		endif

	else if (`echo "$PMA < 3.1" | bc` == 1) then
		if ($HF_SIGDET == 0) then
			cp -rf $sds_root/../0.62/*xls $sds_root/pcs_raw/firmware/code/$process
        		./fw_header.csh $PMA $RAW $FW 0.62 0.56 $header_reg_addr_def_new $process
		else if ($HF_SIGDET == 1) then
			cp -rf $sds_root/../0.7/*xls $sds_root/pcs_raw/firmware/code/$process
        		./fw_header.csh $PMA $RAW $FW 0.7 0.56 $header_reg_addr_def_new $process
		endif
	endif
endif

if ($FW == 2.8_6) then
	if (`echo "$PMA >= 3.1" | bc` == 1) then
		cp -rf $sds_root/../0.3/*xls $sds_root/pcs_raw/firmware/code/$process
	   	./fw_header.csh $PMA $RAW $FW 0.3 0.54 $header_reg_addr_def_new $process
	else if (`echo "$PMA < 3.1" | bc` == 1) then
		cp -rf $sds_root/../0.62/*xls $sds_root/pcs_raw/firmware/code/$process
        	./fw_header.csh $PMA $RAW $FW 0.62 0.54 $header_reg_addr_def_new $process
	endif
endif

if ($FW == 2.8_5) then
	cp -rf $sds_root/../0.62/*xls $sds_root/pcs_raw/firmware/code/$process
     	./fw_header.csh $PMA $RAW $FW 0.62 0.54 $header_reg_addr_def_new $process
endif

cp -f firmware.header path_fw_header


# ===========================
# Step4: Update reg_addr.def
# ===========================
set path_sds_cregs = "$sds_root/pma/tech/$process/ipxact/sds_cregs.v"
set path_fw_dir    = "$sds_root/pcs_raw/firmware/code/$process"

set path_fw_reg_addr_def_old = "$path_fw_dir/reg_addr.def"
set path_fw_reg_addr_def_new = "$path_fw_dir/reg_addr.def_${header_reg_addr_def_new}"

write_log "Generating new reg_addr.def..."
$sds_root/pcs_raw/firmware/bin/16k_get_reg_addr.pl $path_sds_cregs $path_fw_reg_addr_def_new

if (-e $path_fw_reg_addr_def_old) then
    diff $path_fw_reg_addr_def_old $path_fw_reg_addr_def_new > /dev/null
    if ($status != 0) then
        write_log "reg_addr.def differs → updating"
        cp -f $path_fw_reg_addr_def_new $path_fw_reg_addr_def_old
    else
        write_log "reg_addr.def is already up to date"
    endif
else
    write_log "Creating reg_addr.def from new version"
    cp -f $path_fw_reg_addr_def_new $path_fw_reg_addr_def_old
endif

# ===========================
# Step5: Generate param_thresh_set.def
# ===========================

set path_param_thresh = "$sds_root/pcs_raw/firmware/code/$process"

write_log "Generating param_thresh_set.def..."
python3 generate_rtrim.py -PROC $PROC -REL $REL
cp -f param_thresh_set.def $path_param_thresh


# ===========================
# Step6: Generate re_gen_fw file
# ===========================

set path_re_gen = "$sds_root/pcs_raw/firmware/code"

write_log "Generating re_gen_fw.${process}"
python3 generate_re_gen_file.py -PMA $PMA -RAW $RAW -PROC $PROC -REL $REL -FW $FW -process $process 
cp -f re_gen_fw.${process} $path_re_gen

echo "Want to continue? (Enter 1 for Yes, anything else for No)"
  set correct_condition1=$<
  if ($correct_condition1 == 1) then
      echo "success"
      # continue  # would go to next loop iteration
  else
      exit  # This will stop the script immediately
 endif

# ===========================
# Step7: Source re_gen_fw file
# ===========================
	
cd path_re_gen
#alias cp 'cp -f'
#alias mv 'mv -f'
source re_gen_fw.$process

echo "Want to continue to rate_restore? (Enter 1 for Yes, anything else for No)"
  set correct_condition2=$<
  if ($correct_condition2 == 1) then
      echo "success"
      # continue  # would go to next loop iteration
  else
      exit  # This will stop the script immediately
 endif

# ===========================
# Step8: Rate restore
# ===========================

mkdir $sds_root/pma/tech/$process/rate_restore
cp -rf $sds_root/pcs_raw/firmware/code/$process/current_snapshot/sds_pcs_raw_ext_rom.bin                        	$sds_root/pma/tech/$process/rate_restore/
cp -rf $sds_root/pcs_raw/firmware/code/$process/current_snapshot/sds_pcs_raw_ext_rom.fastsim                   		$sds_root/pma/tech/$process/rate_restore/
cp -rf $sds_root/pcs_raw/firmware/code/$process/current_snapshot/sds_pcs_raw_mem_sram_cr_para.fw		      	$sds_root/pma/tech/$process/rate_restore/
cp -rf $sds_root/pcs_raw/firmware/code/$process/current_snapshot/sds_pcs_raw_mem_sram_fastsim.fw 		     	$sds_root/pma/tech/$process/rate_restore/
cp -rf $sds_root/pcs_raw/firmware/code/$process/current_snapshot/sds_pcs_raw_mem_sram_side_load_ecc.bin 	      	$sds_root/pma/tech/$process/rate_restore/
cp -rf $sds_root/pcs_raw/firmware/code/$process/current_snapshot/sds_pcs_raw_mem_rst.v			      		$sds_root/pma/tech/$process/rate_restore/
cp -rf $sds_root/pcs_raw/firmware/bin/fw_rate_restore_image_gen.py 					      		$sds_root/pma/tech/$process/rate_restore/
cp -rf $sds_root/pcs_raw/firmware/bin/rate_restore_ecc_enc_dec.pl 					      		$sds_root/pma/tech/$process/rate_restore/
cp -rf $sds_root/pcs_raw/firmware/bin/rate_restore_gen_ecc.pl 						      		$sds_root/pma/tech/$process/rate_restore/
cp -rf $sds_root/pma/tech/$process/ipxact/reg_addr.def  							      	$sds_root/pma/tech/$process/rate_restore/
cp -rf $sds_root/pma/tech/$process/ipxact/Rate_Restore.csv						     		$sds_root/pma/tech/$process/rate_restore/

cd $sds_root/pma/tech/$process/rate_restore/

python3 fw_rate_restore_image_gen.py

cp -rf $sds_root/pma/tech/$process/rate_restore/sds_pcs_raw* 								$sds_root/pma/tech/$process/ipxact/
cp -rf $sds_root/pma/tech/$process/rate_restore/sds_pcs_raw* 								$sds_root/pcs_raw/firmware/code/$process/current_snapshot/
rm -rf $sds_root/pcs_raw/firmware/code/$process/current_snapshot/*old*
cp -rf $sds_root/pma/tech/$process/rate_restore/sds_pcs_raw_ext_rom.bin                        				$sds_root/pcs_raw/firmware/code/$process/current_snapshot/ipxact/
cp -rf $sds_root/pma/tech/$process/rate_restore/sds_pcs_raw_ext_rom.fastsim                    				$sds_root/pcs_raw/firmware/code/$process/current_snapshot/ipxact/
cp -rf $sds_root/pma/tech/$process/rate_restore/sds_pcs_raw_mem_sram_fastsim.fw 		    			$sds_root/pcs_raw/firmware/code/$process/current_snapshot/ipxact/
cp -rf $sds_root/pma/tech/$process/rate_restore/sds_pcs_raw_mem_rst.v			     				$sds_root/pcs_raw/firmware/code/$process/current_snapshot/ipxact/




