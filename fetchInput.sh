day=$1
inputFile="src/input/day$day.txt"
if [[ ! -f $inputFile ]]; then
  curl -sS --cookie "session=$(cat cookie.txt)" "https://adventofcode.com/2021/day/$day/input" -o $inputFile
  echo "Fetched $inputFile"
else
  echo "$inputFile already exists"
fi

sourceFile="src/day$day.py"
if [[ ! -f $sourceFile ]]; then
  cp src/skeleton.py src/day$day.py
  sed -i "s/'REPLACE_ME'/$day/g" src/day$day.py
  echo "Created $sourceFile"
else
  echo "$sourceFile already exists"
fi