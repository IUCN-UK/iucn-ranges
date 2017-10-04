#!/usr/bin/env bash
set -ue

CURDIR=$(cd `dirname $BASH_SOURCE`; pwd)

# By default, be verbose
#
VERBOSE="1"

# Number of CPUs
#
NPROCS=1


TMPDIR="${PWD}"

# GetOptions..
#
while getopts ":hqn:f:d:" opt
do
  case $opt in
    h) echo ""
     echo " Usage: $(basename $0) [-n ] -f "
     echo ""
     echo " Options:"
     echo " -h : this help message"
     echo " -n : number or processors to use [default: 1]"
     echo " -f : observations list file"
     echo " -q : quiet run"
     echo ""
     exit 0;;
    q) VERBOSE="0";;
    n) NPROCS="$OPTARG";;
    f) LIST="$OPTARG";;
    \?) echo "ERROR: Wrong option $OPTARG ";;
    :) echo "ERROR: Missing value for $OPTARG ";;
  esac
done

if [ ! -f "$LIST" ]
then
echo ""
echo "ERROR: file $LIST does not exist. Finishing."
exit 2
fi



#===========================
# Check PID..
#
check_process(){
kill -0 $1 2>/dev/null
echo $?
}
#===========================

# =====================================================================
# Read pipeline file names of each selected Halo..
#
fcnt=0
file=()
for fini in `cat $LIST`
do
  fcnt=$((fcnt+1))
  file[$fcnt]=$fini
done

[ "$VERBOSE" = "1" ] && echo "Number of Observations $fcnt"

# Check if any halo was found. If not, finish the run..
#
[ "$fcnt" -eq "0" ] && { echo "Empty list of observation?"; exit; }

# Start the distribution of jobs..
#
PIDs=()
ncnt=0

while [ "$ncnt" -le "$fcnt" ]
do

  if [ ${#PIDs[*]} -lt $NPROCS -a "$ncnt" -lt "$fcnt" ]
  then

    ncnt=$((ncnt+1))

    loader_script_goes_here.sh --arguments &

    PID=$!
    PIDs[$PID]=$PID
    CNTs[$PID]=$ncnt

  else
    sleep 1
  fi


  for PID in ${PIDs[*]};
  do
    if [ "$(check_process $PID)" -ne "0" ]; then
      _cnt=${CNTs[$PID]}
      _file=${file[$_cnt]}

      wait $PID
      PSTS=$?
      if [[ $PSTS -eq 0 ]]; then
        # [ "$VERBOSE" = "1" ] && \
        echo "Processing of '$_file' was successfully finished"
      else
        # [ "$VERBOSE" = "1" ] && \
        1>&2 echo "Processing of '$_file' failed"
      fi
      unset PIDs[$PID]
      unset CNTs[$PID]
    fi
  done

  [ "$ncnt" -eq "$fcnt" -a "${#PIDs[*]}" -eq "0" ] && break

done

# End
