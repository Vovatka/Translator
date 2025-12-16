#!/bin/bash
# run_tests_compact.sh

echo "Запуск 10 тестов..."
echo "=================="

for i in {1..10}; do
    file="test$i.txt"
    
    if [ -f "$file" ]; then
        echo -e "\n\nТЕСТ $i: $file"
        echo "============================"
        python main.py "$file"
        echo "Код возврата: $?"
    else
        echo -e "\nFile $file not found"
    fi
done
