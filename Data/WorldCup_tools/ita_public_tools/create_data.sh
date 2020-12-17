#!/bin/bash
start_day=$1
end_day=$2
for ((day=$start_day; day<=$end_day; day++)) 
do
	for((part=1; part<=9; part++))
	do
		gzip -dc input/wc_day$day"_"$part.gz | bin/recreate state/object_mappings.sort > data/tmp.csv
		output=$?
		if [[ $output == 255 ]];then
			break
		fi
			mv data/tmp.csv data/wc_day"$day"_"$part".csv
	done
done
rm data/tmp.csv
