#!/usr/bin/bash
#SBATCH --time=03:00:00
#SBATCH --mem=8gb
#SBATCH --job-name=master_flex
#SBATCH --partition=nodes

##############################################################################################
##   Master script to run FLEXPART trajectories for previous month for sites:               ##
##                  - Cape Verde                                                            ##
##                  - Hateruma Island                                                       ##
##                  - Mace Head (No box processing)                                         ##
##                  - Tudor Hill (No box post-processing)                                   ##
##   Cape Verde script also downloads relevant GFS inputs. Therefore this script will wait  ##
##   until that job has completed before setting off the remaining sites simultaneously.    ##
##############################################################################################

cd ./cvao/05x05/
sbatch --wait run_cvao_FLEXPART.py

cd ../../hateruma/
sbatch run_hat_FLEXPART.py

cd ../mace_head/
sbatch run_mh_FLEXPART.py

cd ../tudor_hill/
sbatch run_tud_FLEXPART.py

cd ../ragged_point/
sbatch run_rag_FLEXPART.py

echo FLEXPART trajectories done for this month. 
