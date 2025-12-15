# Arithmetic Expression Language Translator

## Grammar
```ebnf
<Program> ::= <StatementList>
<StatementList> ::= <Statement> | <StatementList> <Statement>
<Statement> ::= <Declaration> | <Assignment> | <Expression>
<Declaration> ::= int ID = <Expression> ;
<Assignment> ::= ID = <Expression> ;
<Expression> ::= <Term> | <Expression> + <Term> | <Expression> - <Term>
<Term> ::= <Factor> | <Term> * <Factor> | <Term> / <Factor>
<Factor> ::= IntLiteral | ID | ( <Expression> ) | - <Factor>
```

**Примеры IntLiteral:**
- `0`
- `1234`
- `-34`

**Примеры ID:**
- `x`
- `a1`
- `value_147`

Грамматика допускает написание нескольких минусов перед числом или переменной.
Например `---9` будет преобразовано в `-9`

## Использование и запуск
1. clone/download files
2. run `python3 main.py [filename]` (Можно воспользоваться `input.txt`, в котором содержатся базовые примеры.)

**Обработка ошибок:**
Транслятор обнаруживает и сообщает о следующих типах ошибок:
1. Лексические ошибки:
  - Неизвестные символы в исходном коде
  - Некорректные числовые литералы (например: 12a3)
2. Синтаксические ошибки:
  - Нарушение грамматики языка
  - Отсутствие обязательных символов (например, точки с запятой)
  - Непарные скобки
3. Семантические ошибки:
  - Использование необъявленной переменной
  - Использование неинициализированной переменной
  - Деление на ноль

**Все сообщения об ошибках включают:**
- Тип ошибки
- Номер строки и позицию в строке
- Описание ошибки

## Author:
***Ткаченко Владимир КМБО-05-23***
