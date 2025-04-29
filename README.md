# Regex to DFA

## Descriere

Acest proiect Python convertește expresii regulate în DFA (automat finit determinist), parcurgând următoarele etape:

1. **Transformarea expresiei regulate** într-o formă postfixată.
2. **Construirea unui NFA** folosind algoritmul lui Thompson.
3. **Conversia NFA-ului în DFA** prin algoritmul de determinizare (subset construction).
4. **Simularea DFA-ului** pentru a valida dacă anumite cuvinte aparțin limbajului descris de expresia regulată.
5. **Testarea automată** a rezultatelor folosind un fișier JSON de intrare.

---

## Formatul fișierului `input.json`

Fișierul JSON trebuie să conțină o listă de teste, fiecare test având forma:

```json
[
  {
    "regex": "a(b|c)*",
    "test_strings": [
      {"input": "ab", "expected": true},
      {"input": "accc", "expected": true},
      {"input": "a", "expected": true},
      {"input": "b", "expected": false}
    ]
  }
]
```

---

## Funcționalități principale

- `postfix(regex)` – transformă expresia regulată într-o formă postfixată, adăugând concatenări implicite (`.`).
- `postfix_nfa(postfix)` – construiește un NFA folosind algoritmul lui Thompson.
- `nfa_dfa(tranzitii, stare_initiala, stare_finala)` – transformă un NFA într-un DFA prin subset construction.
- `validare_cuvant_DFA(...)` – simulează execuția unui cuvânt prin DFA și verifică dacă este acceptat.

---

## Exemplu de output

```text
Cuvant introdus ab: rezultat obtinut True, expected: True
Cuvant introdus b: rezultat obtinut False, expected: False
...
```

---

Proiect realizat ca parte a cursului **Limbaje Formale și Automate**.