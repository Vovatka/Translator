***Автор: Ткаченко Владимир КМБО-05-23. Вариант 20-2-1***

## Задание 1
Разработать грамматику G по описанию (БНФ):

Выражения из присваиваний переменных типа `int`. Пример: `a = 0`; `b = 1`; `a = a + b`;

### Описане языка
Язык описывает последовательность операций присваивания значений переменным 
целочисленного типа.

**В язык входит:**
- Объявление и инициализация переменных типа `int`
- Присваивание значений переменным
- Арифметические операции: сложение `+`, вычитание `-`, умножение `*`, деление `/`
- Использование скобок `()` для изменения приоритета операций
- Использование ранее объявленных переменных в выражениях
- Последовательное выполнение операторов (через точку с запятой `;`)

**В язык не входит:**
- Другие типы данных (кроме `int`)
- Условные операторы (`if`, `else`)
- Циклы (`for`, `while`)
- Функции и процедуры
- Логические операции
- Операции сравнения

**Грамматика G:**
```ebnf
<Program> ::= <StatementList>

<StatementList> ::= <Statement> | <StatementList> <Statement>

<Statement> ::= <Declaration> | <Assignment>

<Declaration> ::= int ID = <Expression> ;

<Assignment> ::= ID = <Expression> ;

<Expression> ::= <Term> | <Expression> + <Term> | <Expression> - <Term>

<Term> ::= <Factor> | <Term> * <Factor> | <Term> / <Factor>

<Factor> ::= IntLiteral | ID | ( <Expression> ) | - <Factor>
```

**Терминалы:**
- IntLiteral - целочисленные литералы: `123`, `-45`, `0`
- ID - идентификаторы переменных: `a`, `b`, `counter`, `tmp`
- Ключевые слова: `int`
- Операторы: `+`, `-`, `*`, `/`, `=`
- Разделители: `;`, `(`, `)`

### Примеры:

1.  Простые объявления и присваивания:

    ```c
    int x = 10;
    int y = 20;
    z = x + y;
    ```

2.  Арифметические операции с приоритетом:

    ```c
    int a = 5;
    int b = 3;
    result = a * b + 2;
    value = a * (b + 2);
    ```

3.  Множественные операции:

    ```c
    int base = 100;
    int bonus = 25;
    int penalty = 10;
    total = base + bonus - penalty;
    result = total / 5 * 2;
    ```

4.  Последовательные вычисления:

    ```c
    int start = 0;
    start = start + 1;
    start = start * 10;
    start = start - 5;
    result = start / 2;
    ```

## Задание 2

### Класс и однозначность грамматики
Поскольку в левой части продукции всегда стоит один нетерминал, а в правой – любое
выражение, грамматика относится к классу *контекстно-свободных*. При этом она
однозначна (будет доказано в задании 4) и не является регулярной.

**Правила в грамматике G, нарушающие регулярность:**
- Смешанный порядок терминалов и нетерминалов. Напимер для `<Assignment> ::= ID = <Expression> ;`
Правая часть представляет собой терминал (ID) → терминал (=) → нетерминал (Expression) → терминал (;),
что не укладывается в правила вида A → aB A → Ba.
- Левая рекурсия:
    ```
    <Expression> ::= <Expression> + <Term>
    <Term> ::= <Term> * <Factor>
    ```
    Левая рекурсия невозможна в регулярных грамматиках, т.к. она требует стека, и следовательно,
    не может описана конечным автоматом.
- ```
  Лемма о накачке для регулярных языков:
  Если L регулярен, то ∃p > 0 такое, что ∀s ∈ L, |s| ≥ p можно разбить на s = xyz, где:
  |xy| ≤ p
  |y| ≥ 1
  ∀k ≥ 0: xyᵏz ∈ L
  ```
Рассмотрим язык L' < L (подмножество):

L' = { "ID" "=" "("^n "IntLiteral" ")"^n ";" | n ≥ 0 }

Где:
n - количество пар скобок

Примеры:
- n = 0: ID = a;
- n = 1: ID = (a);
- n = 2: ID = ((a));
- n = 3: ID = (((a)));

**Предположим, L' регулярен:**
1. Возьмем p из леммы о накачке
2. Рассмотрим строку s = "ID" "=" "("^p "IntLitaral" ")"^p ";" <= L', где |s| = 2p+4 >= p
3. Разобьем s = xyz, где |xy| <= p, |y| => 1
4. Поскольку |xy| <= p, y состоит только из символов "ID" "=" "(" (первые p символов)
5. Значит, y содержит только открывающие скобки
6. Накачаем: s' = xy^2z
7. Количество "(" увеличится
8. Количество ")" останется прежним
9. Получим: "ID" "=" "("^p+k "IntLiteral" ")"^p ; где k => 1
Это не принадлежит L', так как количество "(" не равно количеству ")"

Противоречие с леммой о накачке ?!

### Класс и однозначность языка
**Класс:**
Язык порождается контекстно-свободной грамматикой и не может быть описан конечным автоматом,
из-за левой рекурсии => язык *контекстно-свободный*

**Однозначность:**
Язык порождается однозначной грамматикой => язык по определению *однозначен*.

## Задание 3

### Cинтаксическое дерево и вывод произвольного предложения
Возьмём в качестве примера следующее предложение:
```
int a = 10;
b = a * 2 + 5;
```

**Полный разбор предложения:**
```ebnf
<Program> ->
<StatementList> ->
<StatementList><Statement> ->
<Statement><Statement> ->
<Declaration><Statement> ->
int ID = <Expression> ; <Statement> ->
int ID = <Term> ; <Statement> ->
int ID = <Factor> ; <Statement> ->
int ID = IntLiteral ; <Statement> ->
int ID = IntLiteral ; <Assignment> ->
int ID = IntLiteral ; ID = <Expression> ; ->
int ID = IntLiteral ; ID = <Expression> + <Term> ; ->
int ID = IntLiteral ; ID = <Term> + <Term> ; ->
int ID = IntLiteral ; ID = <Term> * <Factor> + <Term> ; ->
int ID = IntLiteral ; ID = <Factor> * <Factor> + <Term> ; ->
int ID = IntLiteral ; ID = ID * <Factor> + <Term> ; ->
int ID = IntLiteral ; ID = ID * IntLiteral + <Term> ; ->
int ID = IntLiteral ; ID = ID * IntLiteral + <Factor> ; ->
int ID = IntLiteral ; ID = ID * IntLiteral + IntLiteral ;
```

**Cинтаксическое дерево:**
```tree
<Program>
└── <StatementList>
    ├── <StatementList>
    │   └── <Statement>
    │       └── <Declaration>
    │           ├── int
    │           ├── ID
    │           ├── =
    │           ├── <Expression>
    │           │   └── <Term>
    │           │       └── <Factor>
    │           │           └── IntLiteral
    │           └── ;
    └── <Statement>
        └── <Assignment>
            ├── ID
            ├── =
            ├── <Expression>
            │   ├── <Expression>
            │   │   └── <Term>
            │   │       ├── <Term>
            │   │       │   └── <Factor>
            │   │       │       └── ID
            │   │       ├── *
            │   │       └── <Factor>
            │   │           └── IntLiteral
            │   ├── +
            │   └── <Term>
            │       └── <Factor>
            │           └── IntLiteral
            └── ;
```

![5328239842653047882](https://github.com/user-attachments/assets/8aff5297-5797-40e1-b168-675086c63374)

## Задание 4

### Таблица SLR(1)

**Набор правил:**
```ebnf
0. S' -> .Program
1. Program -> .StatementList
2. StatementList -> .Statement
3. StatementList -> .StatementList Statement
4. Statement -> .Declaration
5. Statement -> .Assignment
6. Declaration -> .int ID = Expression ;
7. Assignment -> .ID = Expression ;
8. Expression -> .Expression + Term
9. Expression -> .Expression - Term
10. Expression -> .Term
11. Term -> .Term * Factor
12. Term -> .Term / Factor
13. Term -> .Factor
14. Factor -> .IntLiteral
15. Factor -> .ID
16. Factor -> .( Expression )
17. Factor -> .- Factor
```


|Нетерминал   |FIRST                     |FOLLOW                   |
|:-----------:|:------------------------:|:-----------------------:|
|S'           |{int, ID}                 |{$}                      |
|Program      |{int, ID}                 |{$}                      |
|StatementList|{int, ID}                 |{$,int,ID}               | 
|Statement    |{int, ID}                 |{$,int,ID}               |
|Declaration  |{int}                     |{$,int,ID}               | 
|Assignment   |{ID}                      |{$,int,ID}               |
|Expression   |{IntLiteral, ID, "(", "-"}|{";","+","-",")"}        |
|Term         |{IntLiteral, ID, "(", "-"}|{";","+","-","*","/",")"}|
|Factor       |{IntLiteral, ID, "(", "-"}|{";","+","-","*","/",")"}|

**Стартовое сотояние:**
```ebnf
0. S' -> .Program
1. Program -> .StatementList
2. StatementList -> .Statement
3. StatementList -> .StatementList Statement
4. Statement -> .Declaration
5. Statement -> .Assignment
6. Declaration -> .int ID = Expression ;
7. Assignment -> .ID = Expression ;
```

*Дублирующие состояния goto(n1, T1)=goto(n2, T1) для упрощения записаны в следующем виде: goto(n1/n2, T1)*
|STATE| GOTO                                   | STATE CONTENT                                                                                                 |
|:---:|:--------------------------------------:|:-------------------------------------------------------------------------------------------------------------:|
| I1  |goto(0, Program)                        |{S' -> Program.}                                                                                               |
| I2  |goto(0, StatementList)                  |{Program -> StatementList.;<br>StatementList -> StatementList.Statement}                                       |
| I3  |goto(0, Statement)                      |{StatementList -> Statement.}                                                                                  | 
| I4  |goto(0/2, Declaration)                  |{Statement -> Declaration.}                                                                                    |
| I5  |goto(0/2, Assignment)                   |{Statement -> Assignment.}                                                                                     |
| I6  |goto(0/2, int)                          |{Declaration -> int. ID = Expression ;}                                                                        |
| I7  |goto(0/2, ID)                           |{Assignment -> ID. = Expression ;}                                                                             |
| I8  |goto(2, Statement)                      |{StatementList -> StatementList Statement.}                                                                    |
| I9  |goto(6, ID)                             |{Declaration -> int ID. = Expression ;}                                                                        |
| I10 |goto(7, =)                              |{Assignment -> ID =. Expression ;}                                                                             |
| I11 |goto(9, =)                              |{Declaration -> int ID =. Expression ;}                                                                        |
| I12 |goto(10, Expression)                    |{Assignment -> ID = Expression.;<br>Expression -> Expression. + Term;<br>Expression -> Expression. - Term}     |
| I13 |goto(10/11/17, Term)                    |{Expression -> Term.;<br>Term -> Term. * Factor;<br>Term -> Term. / Factor}                                    |
| I14 |goto(10/11/17/21/22, Factor)            |{Term -> Factor.}                                                                                              |
| I15 |goto(10/11/17/21/22/23/24, IntLiteral)  |{Factor -> IntLiteral.}                                                                                        |
| I16 |goto(10/11/17/21/22/23/24, ID)          |{Factor -> ID.}                                                                                                |
| I17 |goto(10/11/18/23/24, "(")               |{Factor -> (. Expression )}                                                                                    |
| I18 |goto(10/11/17/21/22/23/24, -)           |{Factor -> -. Factor}                                                                                          |
| I19 |goto(11, Expression)                    |{Declaration -> int ID = Expression.;<br>Expression -> Expression. + Term;<br>Expression -> Expression. - Term}|
| I20 |goto(12, ";")                           |{Assignment -> ID = Expression ;.}                                                                             |
| I21 |goto(12, +)                             |{Expression -> Expression +. Term}                                                                             |
| I22 |goto(12, -)                             |{Expression -> Expression -. Term}                                                                             |
| I23 |goto(13, \*)                            |{Term -> Term *. Factor}                                                                                       |
| I24 |goto(13, /)                             |{Term -> Term /. Factor}                                                                                       |
| I25 |goto(17, Expression)                    |{Factor -> ( Expression.) ;<br>Expression -> Expression. + Term;<br>Expression -> Expression. - Term}          |
| I26 |goto(18, Factor)                        |{Factor -> - Factor.}                                                                                          |
| I27 |goto(19, ";")                           |{Declaration -> int ID = Expression ;.}                                                                        |
| I28 |goto(21, Term)                          |{Expression -> Expression + Term.;<br>Term -> Term. * Factor;<br>Term -> Term. / Factor}                       |
| I29 |goto(22, Term)                          |{Expression -> Expression - Term.;<br>Term -> Term. * Factor;<br>Term -> Term. / Factor}                       |
| I30 |goto(23, Factor)                        |{Term -> Term * Factor.}                                                                                       |
| I31 |goto(24, Factor)                        |{Term -> Term / Factor.}                                                                                       |
| I32 |goto(25, ")")                           |{Factor -> ( Expression ).}                                                                                    |

|State|int|ID |=  |;  |+  | - | *  | /  |IntLiteral| ( | ) |$   |S'  |Program|StatementList|Statement|Declaration|Assignment|Expression|Term|Factor|
|:---:|:-:|:-:|:-:|:-:|:-:|:-:|:--:|:--:|:--:|:---:|:---:|:---:|:---:|:---------:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0   |s6 |s7 |   |   |   |   |    |    |    |     |     |     |     | 1   | 2   | 3   | 4   | 5   |     |     |     |
| 1   |   |   |   |   |   |   |    |    |    |     |     | acc |     |     |     |     |     |     |     |     |     |
| 2   |s6 |s7 |   |   |   |   |    |    |    |     |     | r1  |     |     | 8   | 4   | 5   |     |     |     |     |
| 3   |r2 |r2 |   |   |   |   |    |    |    |     |     | r2  |     |     |     |     |     |     |     |     |     |
| 4   |r4 |r4 |   |   |   |   |    |    |    |     |     | r4  |     |     |     |     |     |     |     |     |     |
| 5   |r5 |r5 |   |   |   |   |    |    |    |     |     | r5  |     |     |     |     |     |     |     |     |     |
| 6   |   |s9 |   |   |   |   |    |    |    |     |     |     |     |     |     |     |     |     |     |     |     |
| 7   |   |   |s10|   |   |   |    |    |    |     |     |     |     |     |     |     |     |     |     |     |     |
| 8   |r3 |r3 |   |   |   |   |    |    |    |     |     | r3  |     |     |     |     |     |     |     |     |     |
| 9   |   |s11|   |   |   |   |    |    |    |     |     |     |     |     |     |     |     |     |     |     |     |
| 10  |   |s16|   |   |   |s18|    |    | s15| s17 |     |     |     |     |     |     |     |     | 12  | 13  | 14  |
| 11  |   |s16|   |   |   |s18|    |    | s15| s17 |     |     |     |     |     |     |     |     | 19  | 13  | 14  |
| 12  |   |   |   |s20|s21|s22|    |    |    |     |     |     |     |     |     |     |     |     |     |     |     |
| 13  |   |   |   |r10|r10|r10| s23| s24|    |     | r10 |     |     |     |     |     |     |     |     |     |     |
| 14  |   |   |   |r13|r13|r13| r13| r13|    |     | r13 |     |     |     |     |     |     |     |     |     |     |
| 15  |   |   |   |r14|r14|r14| r14| r14|    |     | r14 |     |     |     |     |     |     |     |     |     |     |
| 16  |   |   |   |r15|r15|r15| r15| r15|    |     | r15 |     |     |     |     |     |     |     |     |     |     |
| 17  |   |s16|   |   |   |s18|    |    | s15| s17 |     |     |     |     |     |     |     |     | 25  | 13  | 14  |
| 18  |   |s16|   |   |   |s18|    |    | s15| s17 |     |     |     |     |     |     |     |     |     |     | 26  |
| 19  |   |   |   |s27|s21|s22|    |    |    |     |     |     |     |     |     |     |     |     |     |     |     |
| 20  |r7 |r7 |   |   |   |   |    |    |    |     |     | r7  |     |     |     |     |     |     |     |     |     |
| 21  |   |s16|   |   |   |s18|    |    | s15| s17 |     |     |     |     |     |     |     |     |     | 28  | 14  |
| 22  |   |s16|   |   |   |s18|    |    | s15| s17 |     |     |     |     |     |     |     |     |     | 29  | 14  |
| 23  |   |s16|   |   |   |s18|    |    | s15| s17 |     |     |     |     |     |     |     |     |     |     | 30  |
| 24  |   |s16|   |   |   |s18|    |    | s15| s17 |     |     |     |     |     |     |     |     |     |     | 31  |
| 25  |   |   |   |   |s21|s22|    |    |    |     | s32 |     |     |     |     |     |     |     |     |     |     |
| 26  |   |   |   |r17|r17|r17| r17| r17|    |     | r17 |     |     |     |     |     |     |     |     |     |     |
| 27  |r6 |r6 |   |   |   |   |    |    |    |     |     | r6  |     |     |     |     |     |     |     |     |     |
| 28  |   |   |   |r8 |r8 |r8 | s23| s24|    |     | r8  |     |     |     |     |     |     |     |     |     |     |
| 29  |   |   |   |r9 |r9 |r9 | s23| s24|    |     | r9  |     |     |     |     |     |     |     |     |     |     |
| 30  |   |   |   |r11|r11|r11| r11| r11|    |     | r11 |     |     |     |     |     |     |     |     |     |     |
| 31  |   |   |   |r12|r12|r12| r12| r12|    |     | r12 |     |     |     |     |     |     |     |     |     |     |
| 32  |   |   |   |r16|r16|r16| r16| r16|    |     | r16 |     |     |     |     |     |     |     |     |     |     |


**Разбор предложения `int a = 4; b = (a + 3) * 2;`**

| Стек                                   | Вход                          | Действие                     |
|----------------------------------------|-------------------------------|------------------------------|
| I0                                     | int a = 4; b = (a + 3) * 2; $ | s6 (shift int)               |
| I0 int I6                              | a = 4; b = (a + 3) * 2; $     | s9 (shift ID)                |
| I0 int I6 ID I9                        | = 4; b = (a + 3) * 2; $       | s11 (shift =)                |
| I0 int I6 ID I9 = I11                  | 4; b = (a + 3) * 2; $         | s15 (shift IntLiteral)       |
| I0 int I6 ID I9 = I11 IntLiteral I15   | ; b = (a + 3) * 2; $          | r14 (Factor -> IntLiteral)   |
| I0 int I6 ID I9 = I11                  | ; b = (a + 3) * 2; $          | goto(11, Factor) = I14       |
| I0 int I6 ID I9 = I11 Factor I14       | ; b = (a + 3) * 2; $          | r13 (Term -> Factor)         |
| I0 int I6 ID I9 = I11                  | ; b = (a + 3) * 2; $          | goto(11, Term) = I13         |
| I0 int I6 ID I9 = I11 Term I13         | ; b = (a + 3) * 2; $          | r10 (Expression -> Term)     |
| I0 int I6 ID I9 = I11                  | ; b = (a + 3) * 2; $          | goto(11, Expression) = I19   |
| I0 int I6 ID I9 = I11 Expression I19   | ; b = (a + 3) * 2; $          | s27 (shift ;)                |
| I0 int I6 ID I9 = I11 Expression I19 ; I27 | b = (a + 3) * 2; $        | r6 (Declaration -> int ID = Expression ;) |
| I0                                     | b = (a + 3) * 2; $            | goto(0, Declaration) = I4    |
| I0 Declaration I4                      | b = (a + 3) * 2; $            | r4 (Statement -> Declaration)|
| I0                                     | b = (a + 3) * 2; $            | goto(0, Statement) = I3      |
| I0 Statement I3                        | b = (a + 3) * 2; $            | r2 (StatementList -> Statement) |
| I0                                     | b = (a + 3) * 2; $            | goto(0, StatementList) = I2  |
| I0 StatementList I2                    | b = (a + 3) * 2; $            | s7 (shift ID)                |
| I0 StatementList I2 ID I7              | = (a + 3) * 2; $              | s10 (shift =)                |
| I0 StatementList I2 ID I7 = I10        | (a + 3) * 2; $                | s17 (shift ()                |
| I0 StatementList I2 ID I7 = I10 ( I17  | a + 3) * 2; $                 | s16 (shift ID)               |
| I0 StatementList I2 ID I7 = I10 ( I17 ID I16 | + 3) * 2; $         | r15 (Factor -> ID)           |
| I0 StatementList I2 ID I7 = I10 ( I17  | + 3) * 2; $                   | goto(17, Factor) = I14       |
| I0 StatementList I2 ID I7 = I10 ( I17 Factor I14 | + 3) * 2; $          | r13 (Term -> Factor)         |
| I0 StatementList I2 ID I7 = I10 ( I17  | + 3) * 2; $                   | goto(17, Term) = I13         |
| I0 StatementList I2 ID I7 = I10 ( I17 Term I13 | + 3) * 2; $           | r10 (Expression -> Term)     |
| I0 StatementList I2 ID I7 = I10 ( I17  | + 3) * 2; $                   | goto(17, Expression) = I25   |
| I0 StatementList I2 ID I7 = I10 ( I17 Expression I25 | + 3) * 2; $   | s21 (shift +)                |
| I0 StatementList I2 ID I7 = I10 ( I17 Expression I25 + I21 | 3) * 2; $ | s15 (shift IntLiteral) |
| I0 StatementList I2 ID I7 = I10 ( I17 Expression I25 + I21 IntLiteral I15 | ) * 2; $ | r14 (Factor -> IntLiteral) |
| I0 StatementList I2 ID I7 = I10 ( I17 Expression I25 + I21 | ) * 2; $ | goto(21, Factor) = I14 |
| I0 StatementList I2 ID I7 = I10 ( I17 Expression I25 + I21 Factor I14 | ) * 2; $ | r13 (Term -> Factor) |
| I0 StatementList I2 ID I7 = I10 ( I17 Expression I25 + I21 | ) * 2; $ | goto(21, Term) = I28 |
| I0 StatementList I2 ID I7 = I10 ( I17 Expression I25 + I21 Term I28 | ) * 2; $ | r8 (Expression -> Expression + Term) |
| I0 StatementList I2 ID I7 = I10 ( I17 Expression I25 | ) * 2; $ | s32 (shift )) |
| I0 StatementList I2 ID I7 = I10 ( I17 Expression I25 ) I32 | * 2; $ | r16 (Factor -> ( Expression )) |
| I0 StatementList I2 ID I7 = I10        | * 2; $                        | goto(10, Factor) = I14       |
| I0 StatementList I2 ID I7 = I10 Factor I14 | * 2; $                 | r13 (Term -> Factor)         |
| I0 StatementList I2 ID I7 = I10        | * 2; $                        | goto(10, Term) = I13         |
| I0 StatementList I2 ID I7 = I10 Term I13 | * 2; $                 | s23 (shift *)                |
| I0 StatementList I2 ID I7 = I10 Term I13 * I23 | 2; $           | s15 (shift IntLiteral)       |
| I0 StatementList I2 ID I7 = I10 Term I13 * I23 IntLiteral I15 | ; $ | r14 (Factor -> IntLiteral) |
| I0 StatementList I2 ID I7 = I10 Term I13 * I23 | ; $           | goto(23, Factor) = I30       |
| I0 StatementList I2 ID I7 = I10 Term I13 * I23 Factor I30 | ; $ | r11 (Term -> Term * Factor) |
| I0 StatementList I2 ID I7 = I10        | ; $                           | goto(10, Term) = I13         |
| I0 StatementList I2 ID I7 = I10 Term I13 | ; $                 | r10 (Expression -> Term)     |
| I0 StatementList I2 ID I7 = I10        | ; $                           | goto(10, Expression) = I12   |
| I0 StatementList I2 ID I7 = I10 Expression I12 | ; $                 | s20 (shift ;)                |
| I0 StatementList I2 ID I7 = I10 Expression I12 ; I20 | $             | r7 (Assignment -> ID = Expression ;) |
| I0 StatementList I2                    | $                             | goto(2, Assignment) = I5     |
| I0 StatementList I2 Assignment I5      | $                             | r5 (Statement -> Assignment) |
| I0 StatementList I2                    | $                             | goto(2, Statement) = I8      |
| I0 StatementList I2 Statement I8       | $                             | r3 (StatementList -> StatementList Statement) |
| I0 StatementList I2                    | $                             | goto(2, StatementList) = I2  |
| I0 StatementList I2                    | $                             | r1 (Program -> StatementList)|
| I0                                     | $                             | goto(0, Program) = I1        |
| I0 Program I1                          | $                             | acc                    |

**optional: дерево состояний в черновом варианте (здесь стартовое состояние I0 записано в полном виде)**

```ebnf
Для упрощения введём следующие обозначения:
- Program - P
- StatementList - L
- Statement - S
- Declaration - D
- Assignment - A
- Expression - E
- Term - T
- Factor - F
- int - i
- ID - "ID"
- IntLiteral - 2
```

![StateTree (на всякий случай)](https://github.com/user-attachments/assets/e2b02798-e4ae-4a1f-8abf-fcd82b797f22)
![StateTreeContinue](https://github.com/user-attachments/assets/7ea61be1-3b4b-4b10-86f6-f24f05debc47)
