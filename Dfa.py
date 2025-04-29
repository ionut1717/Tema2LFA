import json
teste=json.load(open("input.json","r"))
def postfix(regex):
    precedenta = {'*': 3, '+': 3, '?': 3, '.': 2, '|': 1}
    simboluri = set(precedenta.keys())
    
    new_regex = ""
    for i in range(len(regex)):
        new_regex += regex[i]
        if i + 1 < len(regex):
            if (regex[i].isalnum() or regex[i] in ')*+?') and (regex[i+1].isalnum() or regex[i+1] == '('):
                new_regex += '.'
    output = []
    stiva = []
    for litera in new_regex:
        if litera.isalnum():
            output.append(litera)
        elif litera == '(':
            stiva.append(litera)
        elif litera == ')':
            while stiva and stiva[-1] != '(':
                output.append(stiva.pop())
            stiva.pop()
        elif litera in simboluri:
            while (stiva and stiva[-1] != '(' and precedenta[litera] <= precedenta[stiva[-1]]):
                output.append(stiva.pop())
            stiva.append(litera)
    while stiva:
        output.append(stiva.pop())
    return ''.join(output)

def postfix_nfa(postfix):
    tranzitii = {}
    numar_stare=0

    def stare():
        nonlocal numar_stare
        stare = numar_stare
        tranzitii[stare] = {}
        numar_stare += 1
        return stare

    stiva = []

    for simbol in postfix:
        if simbol.isalnum():
            start = stare()
            final = stare()
            tranzitii[start][simbol] = {final}
            stiva.append((start, final))

        elif simbol == '.':
            s1_start, s1_final = stiva.pop()
            s0_start, s0_final = stiva.pop()
            #setam tranzitiile cu {} daca nu exista, apoi le setam pe cele cu cheia 'λ' cu set gol daca nu exista, la care adaugam s1_start pentru a le concatena
            tranzitii.setdefault(s0_final, {}).setdefault('λ', set()).add(s1_start) 
            stiva.append((s0_start, s1_final))

        elif simbol == '|':
            s1_start, s1_final = stiva.pop()
            s0_start, s0_final = stiva.pop()
            start = stare()
            final = stare()
            tranzitii[start]['λ'] = {s0_start, s1_start}
            tranzitii.setdefault(s0_final, {}).setdefault('λ', set()).add(final)
            tranzitii.setdefault(s1_final, {}).setdefault('λ', set()).add(final)
            stiva.append((start, final))

        elif simbol == '*':
            s_start, s_final = stiva.pop()
            start = stare()
            final = stare()
            tranzitii[start]['λ'] = {s_start, final}
            tranzitii.setdefault(s_final, {}).setdefault('λ', set()).update({s_start, final})
            stiva.append((start, final))

        elif simbol == '+':
            s_start, s_final = stiva.pop()
            start = stare()
            final = stare()
            tranzitii[start]['λ'] = {s_start}
            tranzitii.setdefault(s_final, {}).setdefault('λ', set()).update({s_start, final})
            stiva.append((start, final))

        elif simbol == '?':
            s_start, s_final = stiva.pop()
            start = stare()
            final = stare()
            tranzitii[start]['λ'] = {s_start, final}
            tranzitii.setdefault(s_final, {}).setdefault('λ', set()).add(final)
            stiva.append((start, final))

    stare_initiala, stare_finala = stiva.pop()
    return tranzitii, stare_initiala, stare_finala

def nfa_dfa(nfa_tranzitii, stare_initiala_nfa, stare_finala_nfa):
    
    def nume_stare(stari):
        return '/'.join(str(s) for s in sorted(stari))
    
    def inchidere(stare, tranzitii):
        stare=stare.strip().split("/")
        inchidere = list(set([int(x) for x in stare if x]))
        for stare in inchidere:
            for next_state in tranzitii.get(stare, {}).get('λ', []):
                if next_state not in inchidere:
                    inchidere.append(next_state)
                    
        return inchidere
    
    def stari_accesibile(stare,simbol,tranzitii):
        stare=stare.strip().split("/")
        stari_initiale=set([int(x) for x in stare if x])
        stari_accesibile=set()
        for stare in stari_initiale:
            stari_accesibile.update(tranzitii.get(stare, {}).get(simbol, []))
        return stari_accesibile
    
    dfa_tranzitii = {}
    stari_finale_dfa = set() 
    stari_dfa=set()
    stare_initiala_nfa=str(stare_initiala_nfa)
    stare_initiala_dfa = nume_stare(inchidere(stare_initiala_nfa, nfa_tranzitii))
    stari_dfa.add(stare_initiala_dfa)
    stari_nevizitate = [stare_initiala_dfa]
    dfa_tranzitii[stare_initiala_dfa] = {}
    if str(stare_finala_nfa) in stare_initiala_dfa:
        stari_finale_dfa.add(stare_initiala_dfa)
    alfabet = set()
    for tranzitie in nfa_tranzitii.values():
        for litera in tranzitie:
            if litera != 'λ':
                alfabet.add(litera)
    while stari_nevizitate:
        stare_curenta = stari_nevizitate.pop()
        for litera in alfabet:
            stari_acc=stari_accesibile(stare_curenta,litera,nfa_tranzitii)
            stari_acc=nume_stare(stari_acc)
            stari_acc=(inchidere(stari_acc, nfa_tranzitii))
            stare_obtinuta=nume_stare(stari_acc)
            dfa_tranzitii.setdefault(stare_curenta, {}).setdefault(litera, set()).add(stare_obtinuta)
            if stare_obtinuta not in stari_dfa:
                stari_dfa.add(stare_obtinuta)
                stari_nevizitate.append(stare_obtinuta)
                if str(stare_finala_nfa) in stare_obtinuta:
                    stari_finale_dfa.add(stare_obtinuta)
    return dfa_tranzitii, stare_initiala_dfa, stari_finale_dfa, alfabet

#Functie luata din tema anterioara, modificata doar pentru a primi toate argumentele
def validare_cuvant_DFA(cuvant, start_state, Sigma, Transitions, Final_States):
    current_state = start_state
    for litera in cuvant:
        if litera not in Sigma:
            return False
        if litera not in Transitions.get(current_state, {}):
            return False
        current_state = list(Transitions[current_state][litera])[0]
    if current_state in Final_States:
        return True
    else:
        return False
i=1
for test in teste:
    regex=test['regex']
    regex=postfix(regex)
    tranzitii_nfa,stare_initiala_nfa,stare_finala_nfa=postfix_nfa(regex)
    tranzitii_dfa, stare_initiala_dfa, stari_finale_dfa, alfabet_dfa=nfa_dfa(tranzitii_nfa,stare_initiala_nfa,stare_finala_nfa)
    for caz in test['test_strings']:
        input=caz['input']
        expected=caz['expected']
        print(f"Cuvant introdus {input}: rezultat obtinut {validare_cuvant_DFA(input,stare_initiala_dfa,alfabet_dfa,tranzitii_dfa,stari_finale_dfa)},expected:{expected}")