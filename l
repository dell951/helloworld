#!/bin/bash

PS3='Choose an option: '
export COLUMNS=0
options=("Format C" "Format formated" "Scrap C" "Scrap Formated" "move C" "move formated" "Refresh lists" "What I have")
select opt in "${options[@]}"
do
     case $opt in
             "Format C")
                       echo "formatCzimu.py /volume2/Downloaded/c"
                              formatCzimu.py /volume2/Downloaded/c ;;
             "Format formated")
                       echo "formathjd2048.py /volume2/formated"
                              formathjd2048.py /volume2/formated && formatCzimu.py /volume2/formated ;;
             "Scrap C")
                       echo "runscrapper.sh /volume2/Downloaded/c "
                              nohup runscrapper.sh /volume2/Downloaded/c & ;;
             "Scrap Formated")
                       echo "nohup runscrapper.sh /volume2/formated"
                              nohup runscrapper.sh /volume2/formated & ;;
             "move C")
                       echo "nohup mv -n /volume2/Downloaded/c/* /volume1/3TB/czimu &"
					          nohup mv -n /volume2/Downloaded/c/*.nfo /volume1/3TB/czimu & mv -n /volume2/Downloaded/c/* /volume1/3TB/czimu & ;;
             "move formated")
                       echo "nohup mv -n /volume2/formated/* /volume1/3TB/iReady2 &"
                              nohup mv -n /volume2/formated/*.nfo /volume1/3TB/iReady2 & mv -n /volume2/formated/* /volume1/3TB/iReady2 & ;;                                                            
             "Refresh lists")
                       echo "nohup generate_allmine.sh &"
                             nohup generate_allmine.sh & ;;
             "What I have")
                       echo "list"
                              ls -la /volume2/formated & ls -la /volume2/Downloaded/c ;;
                           *) exit 0;;
     esac
done
