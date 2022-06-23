cat tests.txt | python3 ../computorv2.py > tests_out.txt 2> /dev/null
diff tests_out.txt output.txt > diff.txt
if [ $? -eq 0 ]
then
    rm diff.txt 2> /dev/null
    echo '\033[1mcomputorv2 [\033[32mOK\033[1;30m]\033[0m'
else
    cat diff.txt
    echo '\n\033[1mcomputorv2 [\033[31mKO\033[1;30m]\033[0m'
fi
rm tests_out.txt .computorv2_history
