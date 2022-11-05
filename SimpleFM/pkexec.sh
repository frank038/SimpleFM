#!/bin/bash

##### su command - root password is required
# if [[ "$1" -eq 1 ]]; then
#   echo "$2" | su root -c "chattr +i '$3'"
# elif [[ "$1" -eq 2 ]]; then
#   echo "$2" | su root -c "chattr -i '$3'"
# elif [[ "$1" -eq 3 ]]; then
#   echo "$2" | su root -c "chown `whoami` '$3'"
# elif [[ "$1" -eq 4 ]]; then
#   echo "$2" | su root -c "chgrp `whoami` '$3'"
# fi

##### sudo command
if [[ "$1" -eq 1 ]]; then
  echo "$2" | sudo -S chattr +i "$3"
elif [[ "$1" -eq 2 ]]; then
  echo "$2" | sudo -S chattr -i "$3"
elif [[ "$1" -eq 3 ]]; then
  echo "$2" | sudo -S chown `whoami` "$3"
elif [[ "$1" -eq 4 ]]; then
  echo "$2" | sudo -S chgrp `whoami` "$3"
fi

exit 0
