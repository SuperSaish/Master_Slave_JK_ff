#!/depot/Python/Python-3.8.0/bin/python3

import logging
import os
import subprocess
import re
from parse_re_gen import *

class cls_comp_info:
    def __init__(self, process, base_ipxact_label, new_ipxact_label, name_xls_re_gen_file, name_re_gen_file, ver_asm, header_set_excel_rev_new, header_adpt_revision_new, header_reg_addr_def_new, num_change_list):
        
        self.process                    = process
        self.base_ipxact_label          = base_ipxact_label
        self.new_ipxact_label           = new_ipxact_label
        self.name_xls_re_gen_file       = name_xls_re_gen_file
        self.name_re_gen_file           = name_re_gen_file
        self.ver_asm                    = ver_asm
        self.header_set_excel_rev_new   = header_set_excel_rev_new
        self.header_adpt_revision_new   = header_adpt_revision_new
        self.header_reg_addr_def_new    = header_reg_addr_def_new
        self.num_change_list            = num_change_list
        self.start_step = 0
        self.end_step   = 7

    # Logging definitions ##################################################################################################
    def init_logger(self,path, file_log):
        file_path = "{}/{}".format(path, file_log)
        if os.path.exists(file_path):
            os.remove(file_path)
        else :
            pass
        logging.basicConfig(filename=file_path, level=logging.INFO)
    
    def write_log(msg, severity="info"):
        if severity == "debug":
            logging.debug(msg)
        elif severity == "warning":
            logging.warning(msg)
        elif severity == "error":
            logging.error(msg)
        elif severity == "critical":
            logging.critical(msg)
        else:
            logging.info(msg)
            
        print(msg)
    
    ########################################################################################################################
    
    # definitions in main ##################################################################################################
    def get_env_var(self,base_ipxact_label, new_ipxact_label):
        # input from env
        sds_root = subprocess.getstatusoutput("echo $SDS_ROOT")[1]
        if re.search("/$", sds_root):
            sds_root = sds_root[:-1]
        else:
            pass
        
        num_pma_char = 0
        for num_char in range(int(len(base_ipxact_label))):
            if base_ipxact_label[num_char:num_char+3] == "pma":
                num_pma_char = num_char
                break
            else:
                pass
        num_raw_char = 0
        for num_char in range(int(len(base_ipxact_label))):
            if base_ipxact_label[num_char:num_char+3] == "raw":
                num_raw_char = num_char
                break
            else:
                pass
        num_fw_char = 0
        for num_char in range(int(len(base_ipxact_label))):
            if base_ipxact_label[num_char:num_char+2] == "fw":
                num_fw_char = num_char
                break
            else:
                pass
        
        ver_pma = base_ipxact_label[num_pma_char+4:num_raw_char-1]
        ver_raw = base_ipxact_label[num_raw_char+4:num_fw_char-1]
        ver_fw = new_ipxact_label[num_fw_char+3:]
    
    
        p4_cmd_info = "p4 info | grep \"Client name\""
        p4_client_name = subprocess.getstatusoutput(p4_cmd_info)[1].split()[2]
    
        return sds_root, ver_pma, ver_raw, ver_fw, p4_client_name
    
    
    def get_file_list_to_change(self,sds_root, process):
        write_log("[INFO] Getting file lists...")
        list_files_update = []
        path_pcs_raw_tech = "{sds_root}/pcs_raw/firmware/code/{process}".format(sds_root=sds_root, process=process)
        path_current_snapshot = "{path_pcs_raw_tech}/current_snapshot".format(path_pcs_raw_tech=path_pcs_raw_tech)
        path_current_snapshot_ipxact = "{path_current_snapshot}/ipxact".format(path_current_snapshot=path_current_snapshot)
        path_pma_ipxact = "{sds_root}/pma/tech/{process}/ipxact".format(sds_root=sds_root, process=process)
        
        list_files_pcs_raw_tech = [
                "firmware.header",
                "reg_addr.def",
                ]
        list_files_current_snapshot = [
                "16k_asm_to_rom.pl",
                "adapt_set.def.asic.xls",
                "adapt_set.def.cosim.xls",
                "cal_set.def.asic.xls",
                "cal_set.def.cosim.xls",
                "Makefile",
                "adapt_set.def.asic",
                "adapt_set.def.cosim",
                "batch_make",
                "cal_set.def.asic",
                "cal_set.def.cosim",
                "firmware.header",
                "reg_addr.def",
                "sds_fw_cregs.v",
                "sds_pcs_raw_ext_rom.bin",
                "sds_pcs_raw_ext_rom.fastsim",
                "sds_pcs_raw_mem_rst.annotated.asic",
                "sds_pcs_raw_mem_rst.annotated.cosim",
                "sds_pcs_raw_mem_rst.comments",
                "sds_pcs_raw_mem_rst.errors.asic",
                "sds_pcs_raw_mem_rst.errors.cosim",
                "sds_pcs_raw_mem_rst.fw_labels",
                "sds_pcs_raw_mem_rst.fastsim.sram",
                "sds_pcs_raw_mem_rst.labels",
                "sds_pcs_raw_mem_rst.m",
                "sds_pcs_raw_mem_rst.mvector",
                "sds_pcs_raw_mem_rst.no_comment",
                "sds_pcs_raw_mem_rst.param",
                "sds_pcs_raw_mem_rst.param.asic",
                "sds_pcs_raw_mem_rst.param.cosim",
                "sds_pcs_raw_mem_rst.rom.fw_labels",
                "sds_pcs_raw_mem_rst.sram",
                "sds_pcs_raw_mem_rst.sram.fw_labels",
                "sds_pcs_raw_mem_rst.temp",
                "sds_pcs_raw_mem_rst.v",
                "sds_pcs_raw_mem_rst.version",
                "sds_pcs_raw_mem_rst_asic.v",
                "sds_pcs_raw_mem_rst_cosim.v",
                "sds_pcs_raw_mem_rst_rtl.v",
                "sds_pcs_raw_mem_sram.fw",
                "sds_pcs_raw_mem_sram_cr_para.fw",
                "sds_pcs_raw_mem_sram_fastsim.fw",
                "sds_pcs_raw_mem_sram_side_load_ecc.bin",
                "startup_off_cal_adapt.asm",
                ]
        list_files_current_snapshot_ipxact = [
                "sds_pcs_raw_ext_rom.bin",
                "sds_pcs_raw_ext_rom.fastsim",
                "sds_pcs_raw_mem_rst.sram",
                "sds_pcs_raw_mem_rst.v",
                "sds_pcs_raw_mem_sram.fw",
                "sds_pcs_raw_mem_sram_fastsim.fw",
                ]
        list_files_pma_ipxact = [
                "sds_pcs_raw_ext_rom.bin",
                "sds_pcs_raw_ext_rom.fastsim",
                "sds_pcs_raw_mem_rst.v",
                "sds_pcs_raw_mem_sram_cr_para.fw",
                "sds_pcs_raw_mem_sram_fastsim.fw",
                "sds_pcs_raw_mem_sram_side_load_ecc.bin",
                "reg_addr.def",
                ]
        
        for file_pcs_raw_tech in list_files_pcs_raw_tech:
            file_to_append = path_pcs_raw_tech+"/"+file_pcs_raw_tech
            if os.path.exists(file_to_append):
                list_files_update.append(file_to_append)
            else:
                write_log("[WARN] File {file_to_append} is not existed".format(file_to_append=file_to_append), "warning")
    
        for file_current_snapshot in list_files_current_snapshot:
            file_to_append = path_current_snapshot+"/"+file_current_snapshot
            if os.path.exists(file_to_append):
                list_files_update.append(file_to_append)
            else:
                write_log("[WARN] File {file_to_append} is not existed".format(file_to_append=file_to_append), "warning")
        
        for file_current_snapshot_ipxact in list_files_current_snapshot_ipxact:
            file_to_append = path_current_snapshot_ipxact+"/"+file_current_snapshot_ipxact
            if os.path.exists(file_to_append):
                list_files_update.append(file_to_append)
            else:
                write_log("[WARN] File {file_to_append} is not existed".format(file_to_append=file_to_append), "warning")
        
        for file_pma_ipxact in list_files_pma_ipxact:
            file_to_append = path_pma_ipxact+"/"+file_pma_ipxact
            if os.path.exists(file_to_append):
                list_files_update.append(file_to_append)
            else:
                write_log("[WARN] File {file_to_append} is not existed".format(file_to_append=file_to_append), "warning")
        
        return list_files_update
    
    
    # P4 definisionts ######################################################################################################
    def p4_check_and_update(self,path, ver_update):
        p4_cmd_have = "p4 have {}".format(path)
        ver_have = subprocess.getstatusoutput(p4_cmd_have)[1]
        ver_have = int(ver_have.split()[0].split("#")[1])
        ver_update = int(ver_update)
    
        write_log("[INFO] Checking file : {path}".format(path=path))
        if ver_update == ver_have:
            write_log("[INFO] Current revision number is same as planed to update : {ver_update}".format(ver_update=ver_update))
            write_log("[INFO] Do not update from {path}".format(path=path))
        else:
            write_log("[INFO] Current revision number : {ver_have}".format(ver_have=ver_have))
            write_log("[INFO] Revision number need to be updated to {ver_update}".format(ver_update=ver_update))
            write_log("[INFO] Synch with new revision")
            p4_cmd_sync = "p4 sync {path}#{ver_update}".format(path=path, ver_update=ver_update)
            os.system(p4_cmd_sync)
    
    def p4_check_and_open_for_edit(self,path):
        rev_num_latest = self.p4_get_latest_rev_num(path)
        self.p4_check_and_update(path, rev_num_latest)
        p4_cmd_opened = "p4 opened {path}".format(path=path)
        check_opened = subprocess.getstatusoutput(p4_cmd_opened)[1]
    
        if "file(s) not opened on this client." in check_opened:
            write_log("[INFO] {path} now open for edit.".format(path=path))
            p4_cmd_edit = "p4 edit {path}".format(path=path)
            os.system(p4_cmd_edit)
        else:
            write_log("[INFO] {path} already opened for edit.".format(path=path))
    
    def p4_get_latest_rev_num(self,path):
        print(path)
        p4_cmd_filelog = "p4 filelog {path}".format(path=path)
        p4_filelog = subprocess.getstatusoutput(p4_cmd_filelog)[1]
        print(p4_filelog)
        p4_latest_rev_num = p4_filelog.split("\n")[1].split()[1].replace("#", "")
        return p4_latest_rev_num
    
    def p4_sync_with_label(self,path, ipxact_label):
        p4_cmd_revert = "p4 revert {path}".format(path=path)
        write_log("[INFO] Revert {path} before sync".format(path=path))
        os.system(p4_cmd_revert)
    
        p4_cmd_sync = "p4 sync {path}@{ipxact_label}".format(path=path, ipxact_label=ipxact_label)
        write_log("[INFO] Sync {path} with label {ipxact_label} before editing".format(path=path, ipxact_label=ipxact_label))
        os.system(p4_cmd_sync)

        if os.path.exists(path):
            pass
        else:
            write_log("[WARN] label {ipxact_label} is not existed with {path}".format(ipxact_label=ipxact_label, path=path))
            self.p4_sync_with_latest_rev(path)
    
    def p4_sync_with_latest_rev(self,path):
        p4_cmd_revert = "p4 revert {path}".format(path=path)
        write_log("[INFO] Revert {path} before sync".format(path=path))
        os.system(p4_cmd_revert)
    
        p4_cmd_sync = "p4 sync {path}".format(path=path)
        os.system(p4_cmd_sync)
        write_log("[INFO] Sync {path} with latest revision".format(path=path))
    ########################################################################################################################
    
    
    
    def step0_check_sync(self,sds_root, process, name_xls_re_gen_file):
        path_curr = subprocess.getstatusoutput("pwd")[1]
        write_log("[INFO] STEP0 is started")
        if re.search(sds_root, path_curr):
            pass
        else:
            write_log("[ERR] Please check current workspace env", "error")
            write_log("[ERR] - $SDS_ROOT :  {sds_root}".format(sds_root=sds_root), "error")
            write_log("[ERR] - Current Directory :  {path_curr}".format(path_curr=path_curr), "error")
            exit()
        
        path_process = "{sds_root}/pma/tech/{process}".format(sds_root=sds_root, process=process)
        if os.path.exists(path_process):
            pass
        else:
            write_log("[ERR] Please check input process", "error")
            write_log("[ERR] Current input process: {process}".format(process=process), "error")
            exit()
        
        path_re_gen_file = "{sds_root}/pcs_raw/firmware/code/{xls_re_gen_file}".format(sds_root=sds_root, xls_re_gen_file=name_xls_re_gen_file)
        if os.path.exists(path_re_gen_file):
            pass
        else:
            write_log("[ERR] Please check input xls_re_gen file name", "error")
            write_log("[ERR] Current xls_re_gen file name: {xls_re_gen_file}".format(xls_re_gen_file=name_xls_re_gen_file), "error")
            exit()
        write_log("[INFO] STEP0 is ended")
    
    
    
    
    # Step1 ################################################################################################################
    def step1_check_testchip_dir(self,sds_root, process):
    # 1. make testchip dir in $SDS_ROOT/pma/tech/{process}/ipxact/ , if it is not existed
        path_testchip_dir = "{sds_root}/pma/tech/{process}/ipxact/testchip".format(sds_root=sds_root, process=process)
        write_log("[INFO] STEP1 : Check testchip dir existed in {path_testchip_loc}".format(path_testchip_loc=path_testchip_dir.replace("/testchip", "")))
        
        if os.path.exists(path_testchip_dir):
            write_log("[INFO] testchip dir already existed at {path_testchip_dir}".format(path_testchip_dir=path_testchip_dir))
        else:
            write_log("[INFO] testchip dir not existed at {path_testchip_dir}".format(path_testchip_dir=path_testchip_dir))
            write_log("[INFO] Creating testchip dir at {path_testchip_dir}".format(path_testchip_dir=path_testchip_dir))
            os.system("mkdir {}".format(path_testchip_dir))
        
        write_log("[INFO] STEP1 : Done ")
        write_log("")
    
    ########################################################################################################################
    
    # Step2 ################################################################################################################
    def step2_sync_asm(self,sds_root, ver_asm):
    # 2. sync proper version of startup_off_cal_adapt.asm file in $SDS_ROOT/pcs_raw/firmware/code/
        path_asm = "{sds_root}/pcs_raw/firmware/code/startup_off_cal_adapt.asm".format(sds_root=sds_root)
        write_log("[INFO] STEP2 : Check and update asm file at {path_asm}".format(path_asm=path_asm))
        
        self.p4_check_and_update(path_asm, ver_asm)
    
        write_log("[INFO] STEP2 : Done")
        write_log("")
    
    ########################################################################################################################
    
    # Step3 ################################################################################################################
    def step3_update_fw_header_and_reg_addr(self,sds_root, process, base_ipxact_label, header_fw_new, header_adpt_revision_new, header_set_excel_rev_new, header_reg_addr_def_new):
    # 3. sync latest firmware.header for updating, if needed
    # TODO : Think about HOW TO HANDLE REG_ADDR.DEF
        
        write_log("[INFO] STEP3 : Update Firmware header and Check and Update reg_addr.def")
        self.step3_1_update_fw_header(sds_root, process, base_ipxact_label, header_fw_new, header_adpt_revision_new, header_set_excel_rev_new, header_reg_addr_def_new)
        self.step3_2_update_reg_addr_def(sds_root, process, base_ipxact_label, header_reg_addr_def_new)
    
        write_log("[INFO] STEP3 : Done")
        write_log("")
    
    # sub definision : Step3-1 #######################
    def step3_1_sub_check_version_in_fw_header(self,file_line_fw_header, index, ver_old, ver_new):
        file_line_fw_header = file_line_fw_header.replace(ver_old, ver_new)
        if ver_new >= ver_old:
            write_log("[INFO] - {index} : {ver_old} > {ver_new}".format(index=index, ver_old=ver_old, ver_new=ver_new))
        else:
            write_log("[WARN] - {index} : {ver_old} is newer than {ver_new}".format(index=index, ver_old=ver_old, ver_new=ver_new), "warning")
            write_log("[WARN] - {index} : Please check the {index} version".format(index=index), "warning")
    
        return file_line_fw_header
    
    # Step3-1 ########################################
        # 3-1. update FW version and Adaptation Spec revision number and hfsm excel revision number in firmware.header
        # 3-1-1. check REG_ADDR_DEF number and compare with the revision number of $SDS_ROOT/pma/tech/{process}/ipxact/sds_cregs.v
        #        if they are different, it could be updated. else jump to step number 5
        # 3-1-2. update REG_ADDR_DEF to latest revision number of sds_cregs.v firmware.header
    def step3_1_update_fw_header(self,sds_root, process, base_ipxact_label, header_fw_new, header_adpt_revision_new, header_set_excel_rev_new, header_reg_addr_def_new):
        write_log("[INFO] STEP3-1 : Update Firmware header")
        path_fw_header = "{sds_root}/pcs_raw/firmware/code/{process}/firmware.header".format(sds_root=sds_root, process=process)
    
        self.p4_sync_with_label(path_fw_header, base_ipxact_label)
    
        with open(path_fw_header, "r") as file_rd_fw_header:
            file_rd_fw_header_content = file_rd_fw_header.readlines()
        write_log("[INFO] Open {path_fw_header} for checking update.".format(path_fw_header=path_fw_header))
        
        fw_header_content = ""
        for file_line_fw_header in file_rd_fw_header_content:
            index_fw = "FW"
            index_adpt_revision = "ADPT_REVISION"
            index_set_excel_rev = "SET_EXCEL_REV"
            index_reg_addr_def = "REG_ADDR_DEF"
            list_fw_header = file_line_fw_header.split()
            if len(list_fw_header) > 1:
                if list_fw_header[1] == index_fw:
                    header_fw_old = list_fw_header[3]
                    file_line_fw_header = self.step3_1_sub_check_version_in_fw_header(file_line_fw_header, index_fw, header_fw_old, header_fw_new)
                elif list_fw_header[1] == index_adpt_revision:
                    header_adpt_revision_old = list_fw_header[3]
                    file_line_fw_header = self.step3_1_sub_check_version_in_fw_header(file_line_fw_header, index_adpt_revision, header_adpt_revision_old, header_adpt_revision_new)
                elif list_fw_header[1] == index_set_excel_rev:
                    header_set_excel_rev_old = list_fw_header[3]
                    file_line_fw_header = self.step3_1_sub_check_version_in_fw_header(file_line_fw_header, index_set_excel_rev, header_set_excel_rev_old, header_set_excel_rev_new)
                elif list_fw_header[1] == index_reg_addr_def:
                    header_reg_addr_old = list_fw_header[3]
                    path_sds_cregs = "{sds_root}/pma/tech/{process}/ipxact/sds_cregs.v".format(sds_root=sds_root, process=process)
                    
                    if header_reg_addr_def_new != "":
                        pass
                    else:
                        p4_cmd_have = "p4 have {path}".format(path=path_sds_cregs)
                        header_reg_addr_def_new = subprocess.getstatusoutput(p4_cmd_have)[1]
                        header_reg_addr_def_new = header_reg_addr_def_new.split()[0].split("#")[1]
                    file_line_fw_header = self.step3_1_sub_check_version_in_fw_header(file_line_fw_header, index_reg_addr_def, header_reg_addr_old, header_reg_addr_def_new)
                else:
                    pass
            else:
                pass
            fw_header_content += file_line_fw_header
        
        write_log("[INFO] Get latest revision for updating : {path_fw_header}".format(path_fw_header=path_fw_header))
        self.p4_check_and_open_for_edit(path_fw_header)
        write_log("[INFO] Write new contents to {path_fw_header}".format(path_fw_header=path_fw_header))
        with open(path_fw_header, "w") as file_wr_fw_header:
            file_wr_fw_header.write(fw_header_content)
        write_log("[INFO] Update complete : {path_fw_header}".format(path_fw_header=path_fw_header))
    
        write_log("[INFO] STEP3-1 : Done")
    
    ##################################################
    
    # Step3-2 ########################################
        # 3-2 check REG_ADDR_DEF is updated or not
    def step3_2_update_reg_addr_def(self,sds_root, process, base_ipxact_label, header_reg_addr_def_new):
        write_log("[INFO] STEP3-2 : Check and Update reg_addr.def")
        path_sds_cregs = "{sds_root}/pma/tech/{process}/ipxact/sds_cregs.v".format(sds_root=sds_root, process=process)
        if header_reg_addr_def_new != "":
            p4_check_and_update(path_sds_cregs, header_reg_addr_def_new)
        else:
            self.p4_sync_with_label(path_sds_cregs, base_ipxact_label)
            p4_cmd_have = "p4 have {path}".format(path=path_sds_cregs)
            header_reg_addr_def_new = subprocess.getstatusoutput(p4_cmd_have)[1]
            header_reg_addr_def_new = int(header_reg_addr_def_new.split()[0].split("#")[1])
    
        path_fw_dir = "{sds_root}/pcs_raw/firmware/code/{process}".format(sds_root=sds_root, process=process)
        path_fw_dir_sds_cregs = "{path_fw_dir}/sds_cregs.v_{rev}".format(path_fw_dir=path_fw_dir, rev=header_reg_addr_def_new)
        path_fw_dir_reg_addr_def_old = "{path_fw_dir}/reg_addr.def".format(path_fw_dir=path_fw_dir)
        path_fw_dir_reg_addr_def_new = "{path_fw_dir}/reg_addr.def_{rev}".format(path_fw_dir=path_fw_dir, rev=header_reg_addr_def_new)
        path_pma_ipxact_reg_addr = "{sds_root}/pma/tech/{process}/ipxact/reg_addr.def".format(sds_root=sds_root, process=process)
    
        self.p4_sync_with_label(path_fw_dir_reg_addr_def_old, base_ipxact_label)
        self.p4_sync_with_label(path_pma_ipxact_reg_addr, base_ipxact_label)
        
        # 3-2-1. copy $SDS_ROOT/pma/tech/{process}/ipxact/sds_cregs.v to $SDS_ROOT/pcs_raw/firmware/code/{process}/sds_cregs.v_revision#
        write_log("[INFO] Copy from {path_sds_cregs} to {path_fw_dir_sds_cregs}".format(path_sds_cregs=path_sds_cregs, path_fw_dir_sds_cregs=path_fw_dir_sds_cregs))
        os.system("cp -f {path_sds_cregs} {path_fw_dir_sds_cregs}".format(path_sds_cregs=path_sds_cregs, path_fw_dir_sds_cregs=path_fw_dir_sds_cregs))
        
        # 3-2-2. run $SDS_ROOT/pcs_raw/firmware/bin/16k_get_reg_addr.pl sds_cregs.v_revision# reg_addr.def_revision#
        write_log("[INFO] Run 16k_get_reg_addr script to generate new reg_addr.def")
        os.system("{sds_root}/pcs_raw/firmware/bin/16k_get_reg_addr.pl {path_fw_dir_sds_cregs} {path_fw_dir}/reg_addr.def_{rev}".format(sds_root=sds_root, path_fw_dir_sds_cregs=path_fw_dir_sds_cregs, path_fw_dir=path_fw_dir, rev=header_reg_addr_def_new))
        write_log("[INFO] CMD> {sds_root}/pcs_raw/firmware/bin/16k_get_reg_addr.pl {path_fw_dir_sds_cregs} {path_fw_dir}/reg_addr.def_{rev}".format(sds_root=sds_root, path_fw_dir_sds_cregs=path_fw_dir_sds_cregs, path_fw_dir=path_fw_dir, rev=header_reg_addr_def_new))
        write_log("[INFO] {path_fw_dir_reg_addr_def_new} generated".format(path_fw_dir_reg_addr_def_new=path_fw_dir_reg_addr_def_new))
        
        # 3-2-3. compare reg_addr.def and reg_addr.def_revision#
        if os.path.exists(path_fw_dir_reg_addr_def_old):
            pass
        else:
            self.p4_sync_with_latest_rev(path_fw_dir_reg_addr_def_old)
        check_diff = subprocess.getstatusoutput("diff {path_fw_dir_reg_addr_def_old} {path_fw_dir_reg_addr_def_new}".format(path_fw_dir_reg_addr_def_old=path_fw_dir_reg_addr_def_old, path_fw_dir_reg_addr_def_new=path_fw_dir_reg_addr_def_new))[1]
        flag_diff_reg_addr = False if check_diff == "" else True
        
        # 3-2-4. if there are difference, replace reg_addr.def with reg_addr.def_revision#
        #        else do nothing
        if flag_diff_reg_addr:
            write_log("[INFO] There are differences between {path_fw_dir_reg_addr_def_old} and {path_fw_dir_reg_addr_def_new}".format(path_fw_dir_reg_addr_def_old=path_fw_dir_reg_addr_def_old, path_fw_dir_reg_addr_def_new=path_fw_dir_reg_addr_def_new))
            write_log("[INFO] Difference : {check_diff}".format(check_diff=check_diff))
            self.p4_check_and_open_for_edit(path_fw_dir_reg_addr_def_old)
            write_log("[INFO] Change {path_fw_dir_reg_addr_def_old} with {path_fw_dir_reg_addr_def_new}".format(path_fw_dir_reg_addr_def_old=path_fw_dir_reg_addr_def_old, path_fw_dir_reg_addr_def_new=path_fw_dir_reg_addr_def_new))
            os.system("cp -f {path_fw_dir_reg_addr_def_new} {path_fw_dir_reg_addr_def_old}".format(path_fw_dir_reg_addr_def_new=path_fw_dir_reg_addr_def_new, path_fw_dir_reg_addr_def_old=path_fw_dir_reg_addr_def_old))
            self.p4_check_and_open_for_edit(path_pma_ipxact_reg_addr)
            write_log("[INFO] Copy {path_fw_dir_reg_addr_def_new} to {path_pma_ipxact_reg_addr}".format(path_fw_dir_reg_addr_def_new=path_fw_dir_reg_addr_def_new, path_pma_ipxact_reg_addr=path_pma_ipxact_reg_addr))
            os.system("cp -f {path_fw_dir_reg_addr_def_new} {path_pma_ipxact_reg_addr}".format(path_fw_dir_reg_addr_def_new=path_fw_dir_reg_addr_def_new, path_pma_ipxact_reg_addr=path_pma_ipxact_reg_addr))
    
        else:
            write_log("[INFO] There are no differences between {path_fw_dir_reg_addr_def_old} and {path_fw_dir_reg_addr_def_new}".format(path_fw_dir_reg_addr_def_old=path_fw_dir_reg_addr_def_old, path_fw_dir_reg_addr_def_new=path_fw_dir_reg_addr_def_new))
            write_log("[INFO] {path_fw_dir_reg_addr_def_old} is not to be updated".format(path_fw_dir_reg_addr_def_old=path_fw_dir_reg_addr_def_old))
            write_log("[INFO] {path_pma_ipxact_reg_addr} is not to be updated".format(path_pma_ipxact_reg_addr=path_pma_ipxact_reg_addr))
        
        # 3-2-5. remove temp files
        if os.path.exists(path_fw_dir_sds_cregs):
            write_log("[INFO] Remove temp file {path_fw_dir_sds_cregs}".format(path_fw_dir_sds_cregs=path_fw_dir_sds_cregs))
            os.system("rm -f {path_fw_dir_sds_cregs}".format(path_fw_dir_sds_cregs=path_fw_dir_sds_cregs))
        else:
            pass
        if os.path.exists(path_fw_dir_reg_addr_def_new):
            write_log("[INFO] Remove temp file {path_fw_dir_reg_addr_def_new}".format(path_fw_dir_reg_addr_def_new=path_fw_dir_reg_addr_def_new))
            os.system("rm -f {path_fw_dir_reg_addr_def_new}".format(path_fw_dir_reg_addr_def_new=path_fw_dir_reg_addr_def_new))
        else:
            pass
        
        write_log("[INFO] STEP3-2 : Done")
    
    ##################################################
    ########################################################################################################################
    
    # Step4 ################################################################################################################
    def step4_compile(self,sds_root, process, p4_client_name, name_re_gen_file, name_xls_re_gen_file, ver_fw):
    # 4. compile firmware using re_gen.fw_x...
        # 4-1. check macro before run re_gen_fw
        # 4-2. check after compile if there are error or not
        write_log("[INFO] STEP4 : Compile using re_gen script")
        
        write_log("[INFO] Generating re_gen file from {name_xls_re_gen_file}".format(name_xls_re_gen_file=name_xls_re_gen_file))
        parse_re_gen(sds_root, process, name_re_gen_file, name_xls_re_gen_file, ver_fw)
        
        path_fw_code_dir = "{sds_root}/pcs_raw/firmware/code".format(sds_root=sds_root)
        path_re_gen_file = "{path_fw_code_dir}/{name_re_gen_file}".format(path_fw_code_dir=path_fw_code_dir, name_re_gen_file=name_re_gen_file)
        path_comp_scr = "./compile.csh"
        path_re_gen_log = "{sds_root}/re_gen.log".format(sds_root=sds_root)
    
        if os.path.exists(path_comp_scr):
            os.system("rm -f {path_comp_scr}".format(path_comp_scr=path_comp_scr))
        else:
            pass
        
        write_log("[INFO] Generating script for compile")
        comp_scr_content = "alias cp 'cp -f'\nalias mv 'mv -f'\nalias so 'source'\nsetenv P4CLIENT {p4_client_name}\ncd $SDS_ROOT/pcs_raw/firmware/code\nsource {name_re_gen_file} | tee {path_re_gen_log}\nexec csh".format(p4_client_name=p4_client_name, name_re_gen_file=name_re_gen_file, path_re_gen_log=path_re_gen_log)
        with open(path_comp_scr, "w") as comp_scr:
            comp_scr.write(comp_scr_content)
        write_log("[INFO] Compile script generated at {path_comp_scr}".format(path_comp_scr=path_comp_scr))
    
        write_log("[INFO] Compile is proceeding at popup terminal")
        write_log("[INFO] re_gen file : {path_re_gen_file}".format(path_re_gen_file=path_re_gen_file))
        compile_cmd = "xterm +s -T compile -e csh -c 'source {path_comp_scr}'".format(path_comp_scr=path_comp_scr)
        os.system(compile_cmd)
        write_log("[INFO] Remove compile script at {path_comp_scr}".format(path_comp_scr=path_comp_scr))
        os.system("rm -f {path_comp_scr}".format(path_comp_scr=path_comp_scr))
        re_gen_log = subprocess.getstatusoutput("cat {path_re_gen_log}".format(path_re_gen_log=path_re_gen_log))[1]
        write_log("[INFO] re_gen logging START")
        write_log(re_gen_log)
        os.system("rm -f {path_re_gen_log}".format(path_re_gen_log=path_re_gen_log))
        write_log("[INFO] re_gen logging END")
    
        write_log("[INFO] Checking re_gen log")
        if ("Warning:" in re_gen_log) or ("Error:" in re_gen_log):
            write_log("[ERR] There are warnings during source re_gen script", "error")
            write_log("[ERR] Please check the log file", "error")
            exit()
        else:
            pass
        
        # 4-4. Check CHECKPOINT Dir # of files
        write_log("[INFO] Compile is completed")
        path_check_point = "{sds_root}/pcs_raw/firmware/code/CHECKPOINT.{process}".format(sds_root=sds_root, process=process)
        list_check_point = []
        for dir_name in os.listdir(path_check_point):
            path_sub_dir = "{path_check_point}/{dir_name}".format(path_check_point=path_check_point, dir_name=dir_name)
            written_time = os.path.getctime(path_sub_dir)
            list_check_point.append((dir_name, written_time))
        recent_dir = sorted(list_check_point, key=lambda x: x[1], reverse=True)[0][0]
        path_check_point_sub_dir = "{path_check_point}/{recent_dir}".format(path_check_point=path_check_point, recent_dir=recent_dir)
        num_of_file_check_point = len(os.listdir(path_check_point_sub_dir))
        write_log("[INFO] Checking the recent check point directory...")
        write_log("[INFO] The number of files in {path_check_point_sub_dir}".format(path_check_point_sub_dir=path_check_point_sub_dir))
        if num_of_file_check_point >= 30:
            write_log("[INFO] There are {num_of_file_check_point} files".format(num_of_file_check_point=num_of_file_check_point))
        else:
            write_log("[ERR] Please check the compile result in following directory.", "error")
            write_log("[ERR] {path_check_point_sub_dir}".format(path_check_point_sub_dir=path_check_point_sub_dir), "error")
            write_log("[ERR] Some files are missing.", "error")
            exit()
        
        write_log("[INFO] Compile is completed")
        write_log("[INFO] STEP4 : Done")
        write_log("")
    
    
    
    ########################################################################################################################
            
    # Step5 ################################################################################################################
    def step5_p4_submit(self,sds_root, process, header_fw_new, ver_asm, ver_pma, ver_raw, header_set_excel_rev_new, header_adpt_revision_new):
    # 5. submit to p4
        # 5-1. check file list that opened for edit
        # 5-2. write the descriptions
        # 5-3. submit
        write_log("[INFO] STEP5 : Submit compiled firmware")
        
        # 5-1. check file list that opened for edit
        path_depot = "//dwh/e32/main/dev"
        list_all_files_opened_for_edit = subprocess.getstatusoutput("p4 opened")[1].split("\n")
        all_files_opened_for_edit = []
        for file_opened_for_edit in list_all_files_opened_for_edit:
            all_files_opened_for_edit.append(file_opened_for_edit.split("#")[0].replace(path_depot, sds_root))
        
        flag_check_list = True
        list_file_check = []
        write_log("[INFO] Check files that are opened for edit or not")
        write_log("[INFO] Checking files...")
        list_files_update = self.get_file_list_to_change(sds_root, process)
        path_pcs_raw_tech = "{sds_root}/pcs_raw/firmware/code/{process}".format(sds_root=sds_root, process=process)
        path_fw_header = "{path_pcs_raw_tech}/firmware.header".format(path_pcs_raw_tech=path_pcs_raw_tech)
        path_raw_reg_addr = "{path_pcs_raw_tech}/reg_addr.def".format(path_pcs_raw_tech=path_pcs_raw_tech)
        path_pma_reg_addr = "{sds_root}/pma/tech/{process}/ipxact/reg_addr.def".format(sds_root=sds_root, process=process)
        for file_update in list_files_update:
            write_log("[INFO] Check file opened for edit: {file_update}".format(file_update=file_update))
            if file_update in all_files_opened_for_edit:
                pass
            elif (file_update == path_fw_header) or (file_update == path_raw_reg_addr) or (file_update == path_pma_reg_addr):
                pass
            else:
                flag_check_list = False
                list_file_check.append(file_update)

        if flag_check_list:
            pass
        else:
            write_log("[WARN] File not opened for edit. Please check it", "warning")
            for file_check in list_file_check:
                write_log("[WARN] Not opened for edit: {file_check}".format(file_check=file_check), "warning")
                if os.path.exists(file_check):
                    write_log("[INFO] File added to client: {file_check}".format(file_check=file_check))
                    p4_cmd_add = "p4 add {file_check}".format(file_check=file_check)
                    os.system(p4_cmd_add)
                else:
                    pass
    
        # 5-2. write the descriptions
        path_sds_cregs = "{sds_root}/pma/tech/{process}/ipxact/sds_cregs.v".format(sds_root=sds_root, process=process)
        p4_cmd_have = "p4 have {path}".format(path=path_sds_cregs)
        header_reg_addr_def = subprocess.getstatusoutput(p4_cmd_have)[1]
        header_reg_addr_def = header_reg_addr_def.split()[0].split("#")[1]
        project = process.split("_")[0]
        
        p4_description = ""
        p4_description = p4_description+"Compile FW {header_fw_new} for {project}\n".format(header_fw_new=header_fw_new, project=project)
        p4_description = p4_description+"- ASM : {ver_asm}\n".format(ver_asm=ver_asm)
        p4_description = p4_description+"- PMA : {ver_pma}\n".format(ver_pma=ver_pma)
        p4_description = p4_description+"- RAW : {ver_raw}\n".format(ver_raw=ver_raw)
        p4_description = p4_description+"- SET_EXCEL_REV : {header_set_excel_rev_new}\n".format(header_set_excel_rev_new=header_set_excel_rev_new)
        p4_description = p4_description+"- ADPT_REVISION : {header_adpt_revision_new}\n".format(header_adpt_revision_new=header_adpt_revision_new)
        p4_description = p4_description+"- REG_ADDR_DEF  : {header_reg_addr_def}".format(header_reg_addr_def=header_reg_addr_def)
        write_log("[INFO] Description for submit:")
        write_log(p4_description)
        
        # 5-3. submit
        p4_cmd_submit = "p4 submit -d \"{p4_description}\"".format(p4_description=p4_description)
        write_log("[INFO] Now submiting opened files for edit.")
        
        write_log("[INFO] Submit with following command :")
        write_log(p4_cmd_submit)
        os.system(p4_cmd_submit)
    
        write_log("[INFO] STEP5 : Done")
        write_log("")
    
    def step6_label(self,sds_root, process, base_ipxact_label, new_ipxact_label):
    # 6. tagging submitted files
        # 6-1. dry copy tag from old : p4 tag -n -l <new_label> $SDS_ROOT/...@<old_label>
        # 6-2. copy tag from old : p4 tag -l <new_label> $SDS_ROOT/...@<old_label>
        # 6-3. tagging label to change list submitted : p4 label ~~~
        
        write_log("[INFO] STEP6 : Copy Label")
    
        p4_cmd_dry_cp = "p4 tag -n -l {new_label} {sds_root}/...@{old_label}".format(new_label=new_ipxact_label, sds_root=sds_root, old_label=base_ipxact_label)
        p4_cmd_cp = "p4 tag -l {new_label} {sds_root}/...@{old_label}".format(new_label=new_ipxact_label, sds_root=sds_root, old_label=base_ipxact_label)
        write_log("[INFO] Tag with following command :")
        write_log(p4_cmd_dry_cp)
        dry_cp_log = subprocess.getstatusoutput(p4_cmd_dry_cp)[1]
        write_log(dry_cp_log)

        write_log(p4_cmd_cp)
        cp_log = subprocess.getstatusoutput(p4_cmd_cp)[1]
        write_log(cp_log)
       
        write_log("[INFO] STEP6 : Done")
        write_log("")
    
    def step7_tag(self, sds_root, process, new_ipxact_label, p4_client_name, base_ipxact_label, num_change_list):
        write_log("[INFO] STEP7 : Tagging files with new label")
    
        if num_change_list == "":
            p4_cmd_change_list = "p4 changes -c {client}".format(client=p4_client_name)
            num_change_list = subprocess.getstatusoutput(p4_cmd_change_list)[1].split()[1]
        else:
            pass
    
        if num_change_list == "":
            write_log("[ERR] There's no submittion from this p4 workspace", "error")
            write_log("[ERR] Please check the workspace", "error")
            exit()

        write_log("[INFO] STEP7 : Tag submitted firmware")
        list_files_update = self.get_file_list_to_change(sds_root, process)
        write_log("[INFO] Checking Default change list number {num_change_list}".format(num_change_list=num_change_list))
        for file_update in list_files_update:
            p4_cmd_changes = "p4 changes {file_update}".format(file_update=file_update)
            txt_file_change_list = subprocess.getstatusoutput(p4_cmd_changes)[1]
            if txt_file_change_list == "":
                pass
            else:
                num_file_change_list = txt_file_change_list.split("\n")[0].split()[1]
                if num_file_change_list == num_change_list:
                    p4_cmd_tag = "p4 tag -l {new_label} {file_update}@{num_change_list}".format(new_label=new_ipxact_label, process=process, file_update=file_update, num_change_list=num_change_list)
                else:
                    p4_cmd_have = "p4 have {file_update}".format(file_update=file_update)
                    p4_have_result = subprocess.getstatusoutput(p4_cmd_have)[1]
                    if p4_have_result == "":
                        write_log("[WARN] Please check the file {file_update}".format(file_update=file_update), "warning")
                    else:
                        self.p4_sync_with_label(file_update, base_ipxact_label)
                        p4_have_result = subprocess.getstatusoutput(p4_cmd_have)[1]
                        print(p4_have_result)
                        ver_have = p4_have_result.split()[0].split("#")[1]
                        write_log("[WARN] Default change list number {num_change_list} not exists at {file_update}".format(num_change_list=num_change_list, file_update=file_update), "warning")
                        write_log("[WARN] Synced revision number of file: {ver_have}".format(ver_have=ver_have), "warning")
                        write_log("[WARN] Tagging label at revision number", "warning")
                        p4_cmd_tag = "p4 tag -l {new_label} {file_update}#{ver_have}".format(new_label=new_ipxact_label, process=process, file_update=file_update, ver_have=ver_have)
                write_log("[INFO] Tag with submitted files")
                write_log(p4_cmd_tag)
                os.system(p4_cmd_tag)
    
        write_log("[INFO] STEP7 : Done")
        write_log("")

    def find_step(self,step_num=None):
        if(step_num==0):
            self.step0_check_sync(self.sds_root, self.process, self.name_xls_re_gen_file)
        elif(step_num==1):
            self.step1_check_testchip_dir(self.sds_root, self.process)
        elif(step_num==2):
            self.step2_sync_asm(self.sds_root, self.ver_asm)
        elif(step_num==3):
            self.step3_update_fw_header_and_reg_addr(self.sds_root, self.process, self.base_ipxact_label, self.header_fw_new, self.header_adpt_revision_new, self.header_set_excel_rev_new, self.header_reg_addr_def_new)
        elif(step_num==4):
            self.step4_compile(self.sds_root, self.process, self.p4_client_name, self.name_re_gen_file, self.name_xls_re_gen_file, self.ver_fw)
        elif(step_num==5):
            self.step5_p4_submit(self.sds_root, self.process, self.header_fw_new, self.ver_asm, self.ver_pma, self.ver_raw, self.header_set_excel_rev_new, self.header_adpt_revision_new)
        elif(step_num==6):
            self.step6_label(self.sds_root, self.process, self.base_ipxact_label, self.new_ipxact_label)
        elif(step_num==7):
            self.step7_tag(self.sds_root, self.process, self.new_ipxact_label, self.p4_client_name, self.base_ipxact_label, self.num_change_list)
        else:
            write_log("[ERR] Please check your step", "error")
            exit()


    def auto_comp(self):
        self.init_logger("./", "auto_comp.log")
        
        self.sds_root, self.ver_pma, self.ver_raw, self.ver_fw, self.p4_client_name = self.get_env_var(self.base_ipxact_label, self.new_ipxact_label)
        self.header_fw_new = self.ver_fw

        for step in range(self.start_step,self.end_step+1):
            self.find_step(step_num=step)

