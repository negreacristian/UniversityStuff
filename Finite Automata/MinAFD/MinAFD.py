class AFD(object):
    
    # initializare elemente AFD
    def __init__(self, stari, inputs, starea_finala, starea_initiala, tranzitiile):

        self.stari = stari
        self.Inputs = inputs
        self.Starea_finala = starea_finala
        self.Starea_initala = starea_initiala
        self.Tranzitiile = tranzitiile

    # returnam starea si simbolul de intrare curente
    def getTranzitie(self, stare, input):
        return self.Tranzitiile.get((stare, input))
    
    # cautam starile accesibile pentru a le sterge pe cele ne accesibile
    def getStariAccesibile(self):
        stare_accesibila = {self.Starea_initala}
        for input in self.Inputs:
            stare_posibila = self.getTranzitie(self.Starea_initala, input)
            if stare_posibila is not None:
                stare_accesibila.add(stare_posibila)
        size = 0
        while len(stare_accesibila) > size:
            size = len(stare_accesibila)
            stare_noua = set()
            for stare in stare_accesibila:
                for input in self.Inputs:
                    stare_posibila = self.getTranzitie(stare, input)
                    if stare_posibila is not None:
                        stare_noua.add(stare_posibila)
            stare_accesibila.update(stare_noua)

        return stare_accesibila

    # cautam starile inaccesibile si le stergem

    def stergeStariInaccesibile(self):

        stari_accesibile = self.getStariAccesibile()

        self.stari = set(stare for stare in self.stari if stare in stari_accesibile)
        self.Starea_finala = set(stare for stare in self.Starea_finala if stare in stari_accesibile)
        self.Tranzitiile = {k: v for k, v in self.Tranzitiile.items() if k[0] in stari_accesibile}


    def sortTuple(self, a, b):
        return (a, b) if a < b else (b, a)

    #cream matricea si marcam tranzitile
    def createMatrice(self):
        matrice = dict()
        toate_starile = sorted(self.stari)
        
        # marcam tranzitile ce au stare finala 
        for i in range(len(toate_starile) - 1):
            for j in range(i + 1, len(toate_starile)):
                matrice[self.sortTuple(toate_starile[i], toate_starile[j])] = \
                    ((toate_starile[i] in self.Starea_finala) ^ (toate_starile[j] in self.Starea_finala))
     
        # marcam tranzitile derivate ce sunt marcate deja
        for i in range(len(toate_starile) - 1):
            for j in range(i + 1, len(toate_starile)):

                for input in self.Inputs:
                    transition1 = self.getTranzitie(toate_starile[i], input)
                    transition2 = self.getTranzitie(toate_starile[j], input)

                    if (transition1 is not None) and (transition2 is not None):
                        if matrice.get(self.sortTuple(transition1, transition2)):
                            matrice[self.sortTuple(toate_starile[i], toate_starile[j])] = True

        return matrice

    # cautam starile ce nu au fost marcate
    def GasesteStareAsemanatoare(self, matrice):

        stare_asemanatoare = list()
        toate_starile = sorted(self.stari)

        for i in range(len(toate_starile) - 1):
            for j in range(i + 1, len(toate_starile)):
                if not matrice.get(self.sortTuple(toate_starile[i], toate_starile[j])):
                    stare_asemanatoare.append(self.sortTuple(toate_starile[i], toate_starile[j]))

        return stare_asemanatoare


    def minimize(self):

        AFD_minimizat = AFD(self.stari, self.Inputs, self.Starea_finala, self.Starea_initala, self.Tranzitiile)
        
        AFD_minimizat.stergeStariInaccesibile()
       
       # cream matricea de tranzitii si o completam de 2 ori
        matrice = AFD_minimizat.createMatrice()
        stare_asemanatoare = AFD_minimizat.GasesteStareAsemanatoare(matrice)
       
       # cautam in multimea de stari asemanatoare tranzitile nemarcate ce pot fi marcate 
        for i in stare_asemanatoare:
                for input in self.Inputs:
                    transition1 = self.getTranzitie(i[0], input) 
                    transition2 = self.getTranzitie(i[1], input)

                    if (transition1 is not None) and (transition2 is not None):
                        if matrice.get(self.sortTuple(transition1, transition2)):
                            matrice[self.sortTuple(i[0], i[1])] = True

        stare_asemanatoare = AFD_minimizat.GasesteStareAsemanatoare(matrice)
        # stergem tranzitile ce nu au fost marcate cu tot cu starile lor pentru fiecare simbol de intrare

        for stare in stare_asemanatoare:
            for input in AFD_minimizat.Inputs:

                try:
                    del AFD_minimizat.Tranzitiile[(stare[1], input)]
                except:
                    pass
                try:
                    AFD_minimizat.stari.remove(stare[1])
                except:
                    pass

                try:
                    AFD_minimizat.Starea_finala.remove(stare[1])
                except:
                    pass
                if stare[1] == AFD_minimizat.Starea_initala:
                    AFD_minimizat.Starea_initala = stare[0]

        for key in AFD_minimizat.Tranzitiile.keys():
            for stare in stare_asemanatoare:
                if AFD_minimizat.Tranzitiile.get(key) == stare[1]:
                    AFD_minimizat.Tranzitiile[key] = stare[0]

        return AFD_minimizat

    # functie printare AFD
    def printAFD(self):
      
        print("Starile Automatului: "+ ",".join(sorted(self.stari)))
        print("Simboluri de intrare: "+ ",".join(sorted(self.Inputs)))
        print("Starea initiala: "+ ",".join(sorted(self.Starea_finala)))
        print("Starea finala: "+self.Starea_initala)
        print("Tranzitile Automatului: ")
        for item in sorted(self.Tranzitiile.items()):
            print("         {},{}->{}".format(item[0][0], item[0][1], item[1]))






def main():
    # initializarea automatului

    toate_stariile={'a', 'b', 'c', 'e', 'f', 'g', 'h'}
    inputs={'0', '1'}
    Stare_finala= 'c'
    Stare_initiala= 'a'
    Tranzitiile = { ('a', '0'): 'b',
                    ('a', '1'): 'f',
                    ('b', '0'): 'g', 
                    ('b', '1'): 'c',
                    ('c', '0'): 'a',
                    ('c', '1'): 'c',
                    ('f', '1'): 'g',
                    ('f', '0'): 'c',
                    ('g', '0'): 'g',
                    ('g', '1'): 'e',
                    ('e', '1'): 'f',
                    ('e', '0'): 'h',
                    ('h', '0'): 'g',
                    ('h', '1'): 'c'}
    
    AFD_initial = AFD(toate_stariile, inputs, Stare_finala, Stare_initiala, Tranzitiile)
    AFD_initial.printAFD()
    
    # minimizarea AFD
    AFD_minimizat = AFD_initial.minimize()
    
    # printare AFD
    print("AFD --> AFD Minimizat")
    print("")
    AFD_minimizat.printAFD()


if __name__ == "__main__":
    main()
