file="books.txt"
while read -r line; do
wget "$line"
done <$file