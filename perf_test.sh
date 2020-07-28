#!/bin/sh
echo "Running test"
echo "" > test_output.txt
echo "a length: 40, b_length 40" >> test_output.txt
python3 testInput/generate_tables.py 40 40 testInput/a_table.txt testInput/b_table.txt
python3 fhipe/join_multiThread.py testInput/a_table.txt testInput/b_table.txt >> test_output.txt
python3 testInput/generate_tables.py 40 40 testInput/a_table.txt testInput/b_table.txt
python3 fhipe/join_multiThread.py testInput/a_table.txt testInput/b_table.txt >> test_output.txt
python3 testInput/generate_tables.py 40 40 testInput/a_table.txt testInput/b_table.txt
python3 fhipe/join_multiThread.py testInput/a_table.txt testInput/b_table.txt >> test_output.txt
echo "a length: 80, b_length 40" >> test_output.txt
python3 testInput/generate_tables.py 80 40 testInput/a_table.txt testInput/b_table.txt
python3 fhipe/join_multiThread.py testInput/a_table.txt testInput/b_table.txt >> test_output.txt
python3 testInput/generate_tables.py 80 40 testInput/a_table.txt testInput/b_table.txt
python3 fhipe/join_multiThread.py testInput/a_table.txt testInput/b_table.txt >> test_output.txt
python3 testInput/generate_tables.py 80 40 testInput/a_table.txt testInput/b_table.txt
python3 fhipe/join_multiThread.py testInput/a_table.txt testInput/b_table.txt >> test_output.txt
echo "a length: 120, b_length 40" >> test_output.txt
python3 testInput/generate_tables.py 120 40 testInput/a_table.txt testInput/b_table.txt
python3 fhipe/join_multiThread.py testInput/a_table.txt testInput/b_table.txt >> test_output.txt
python3 testInput/generate_tables.py 120 40 testInput/a_table.txt testInput/b_table.txt
python3 fhipe/join_multiThread.py testInput/a_table.txt testInput/b_table.txt >> test_output.txt
python3 testInput/generate_tables.py 120 40 testInput/a_table.txt testInput/b_table.txt
python3 fhipe/join_multiThread.py testInput/a_table.txt testInput/b_table.txt >> test_output.txt