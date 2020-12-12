python ir/p4/query.py -q "Concordia COVID-19 faculty" -ra tfidf -o output/1_1_tfidf.txt
python ir/p4/query.py -q "Concordia COVID-19 faculty" -ra bm25 -o output/1_1_bm25.txt

python ir/p4/query.py -q "SARS-CoV Concordia faculty" -ra tfidf -o output/1_2_tfidf.txt
python ir/p4/query.py -q "SARS-CoV Concordia faculty" -ra bm25 -o output/1_2_bm25.txt

python ir/p4/query.py -q "water management sustainability Concordia" -ra tfidf -o output/2_1_tfidf.txt
python ir/p4/query.py -q "water management sustainability Concordia" -ra bm25 -o output/2_1_bm25.txt
