#!/bin/bash

BASE_PATH="$(dirname "$0")"
source "$BASE_PATH/colors.sh"
EXIT_CODE=0


################################################################################
#                                   ISORT                                      #
################################################################################
echo -n "${Cyan}Formatting import with isort... $Color_Off"
out=$(isort france_connect/)
if [ ! -z "$out" ] ; then
  echo ""
  echo -e "$out"
fi
echo "${Green}Ok ✅ $Color_Off"
echo ""

################################################################################
#                                   BLACK                                      #
################################################################################
echo "${Cyan}Formatting code with black...$Color_Off"
black -l 120 france_connect/
echo ""


################################################################################
#                                PYCODESTYLE                                   #
################################################################################
echo -n "${Cyan}Running pycodestyle... $Color_Off"
out=$(pycodestyle france_connect/)
if [ "$?" -ne 0 ] ; then
  echo "${Red}Error !$Color_Off"
  echo -e "$out"
  EXIT_CODE=1
else
  echo "${Green}Ok ✅ $Color_Off"
fi
echo ""


################################################################################
#                                PYDOCSTYLE                                    #
################################################################################
echo -n "${Cyan}Running pydocstyle... $Color_Off"
out=$(pydocstyle --count france_connect/)
if [ "$?" -ne 0 ] ; then
  echo "${Red}Error !$Color_Off"
  echo -e "$out"
  EXIT_CODE=1
else
  echo "${Green}Ok ✅ $Color_Off"
fi
echo ""


################################################################################
#                                  BANDIT                                      #
################################################################################
echo -n "${Cyan}Running bandit... $Color_Off"
out=$(bandit --ini=setup.cfg -ll 2> /dev/null)
if [ "$?" -ne 0 ] ; then
  echo "${Red}Error !$Color_Off"
  echo -e "$out"
  EXIT_CODE=1
else
  echo "${Green}Ok ✅ $Color_Off"
fi
echo ""



################################################################################


if [ $EXIT_CODE = 1 ] ; then
   echo "${Red}⚠ You must fix the errors before committing ⚠$Color_Off"
   exit $EXIT_CODE
fi
echo "${Purple}✨ You can commit without any worry ✨$Color_Off"