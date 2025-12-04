def broj_U_Excel_Stupac(n):
    result = ""
    while n > 0:
        n -= 1
        result = chr(n % 26 + ord('A')) + result
        n //= 26
    return result

def excSlovo_u_broj(tks):
    brj = 0
    for tk in tks:
        vrijednost = ord(tk.upper()) - ord('A') + 1
        brj = brj * 26 + vrijednost
    return brj

print("zelis li slova u brojeve(1) ili brojeve u slova (2)")
pitanje=int(input())

if pitanje == 1:
    while True:
        print("za izlaz upisi 0")
        unos = input("daj slova :::")
        if(unos=="0"):
            break
        print(excSlovo_u_broj(unos))

elif pitanje == 2:
    while True:
        Ulaz = input("daj pozitivan broj ('q' ugasi): ")
        if Ulaz.lower() == 'q':
            break
        if Ulaz.isdigit() and int(Ulaz) > 0:
            print(broj_U_Excel_Stupac(int(Ulaz)))
        else:
            print("daj prek nule broj")
else:
    print("debil")