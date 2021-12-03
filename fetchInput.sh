day=$1
curl -sS --cookie "session=$(cat cookie.txt)" "https://adventofcode.com/2021/day/$day/input" -o src/input/day$day.txt
cp src/skeleton.py src/day$day.py
sed -i "s/'REPLACE_ME'/$day/g" src/day$day.py