#!/bin/bash

PS3='Choose an option: '
export COLUMNS=0
options=("Format C" "Format formated" "Scrap C" "Scrap Formated" "move C" "move formated" "Refresh lists" "What I have")
select opt in "${options[@]}"
do
     case $opt in
             "Format C")
                       echo "formatCzimu.py /volume5/Downloaded/c"
                              formatCzimu.py /volume5/Downloaded/c ;;
             "Format formated")
                       echo "formathjd2048.py /volume5/formated"
                              formathjd2048.py /volume5/formated && formatCzimu.py /volume5/formated ;;
             "Scrap C")
                       echo "runscrapper.sh /volume5/Downloaded/c "
                              nohup runscrapper.sh /volume5/Downloaded/c & ;;
             "Scrap Formated")
                       echo "nohup runscrapper.sh /volume5/formated"
                              nohup runscrapper.sh /volume5/formated & ;;
             "move C")
                       echo "nohup mv -n /volume5/Downloaded/c/* /volume1/3TB/czimu &"
					          nohup mv -n /volume5/Downloaded/c/*.nfo /volume1/3TB/czimu & mv -n /volume5/Downloaded/c/* /volume1/3TB/czimu & ;;
             "move formated")
                       echo "nohup mv -n /volume5/formated/* /volume1/3TB/iReady2 &"
                              nohup mv -n /volume5/formated/*.nfo /volume1/3TB/iReady2 & mv -n /volume5/formated/* /volume1/3TB/iReady2 & ;;                                                            
             "Refresh lists")
                       echo "nohup generate_allmine.sh &"
                             nohup generate_allmine.sh & ;;
             "What I have")
                       echo "list"
                              ls -la /volume5/formated & ls -la /volume5/Downloaded/c ;;
                           *) exit 0;;
     esac
done
