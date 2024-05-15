from operator import index


class NFA:
   
    #initializam atributele clasei

    def __init__(self, cuvinte, tranzitii , date_intrare, stare_initiala, stari_finale, starefinala_cuvant):
        self.cuvinte=cuvinte
        self.tranzitii=tranzitii
        self.date_intrare=date_intrare
        self.stare_initiala=stare_initiala
        self.stari_finale=stari_finale
        self.starefinala_cuvant=starefinala_cuvant
  
    

    # afisam automatul 

    def print_afn(self):
       
        print("Date de intrare:", sorted(date_intrare))
       
        print("Tranzitiile :")
       
        for t in tranzitii:
            print(f"  {t[0]} --> {tranzitii[t]} --> {t[1]}")
      
        print("Prima stare:", stare_initiala)
       
        print("Stari finale acceptate:", stari_finale)
        
        print("Starile finale ale fiecarui cuvant: ")
        
        for i in starefinala_cuvant:
           print(f"  {starefinala_cuvant[i]} <--> {i} ")


# introduc 4 cuvinte de la tastatura

unu=input("Primul cuvant: ")
doi=input("Al doilea cuvant: ")
trei=input("Al treilea cuvant: ")
patru=input("Al patrulea cuvant: ")

cuvinte=[unu,doi,trei,patru]      

cuvant=cuvinte

# setam datele de intrare fiecare litera a cuvintelor
date_intrare = set("".join(cuvinte))



tranzitii = {}
stari_finale=[]

nr=0
t=0

#formeaza starea initiala

tranzitii[(t,t)]= "#"
starefinala_cuvant={}



       
for cuvinte in cuvinte:
    stari_finale.append(nr)

    if cuvinte:  # daca cuvantul exista
     
       tranzitii[(t, nr+1)] =cuvinte[0]  # adaugam prima legatura a cuvantului de la stare initiala
       nr=nr+1
       for i in range(len(cuvinte)-1):
         
           
           tranzitii[(nr, nr+1)] = cuvinte[i+1]
           nr=nr+1
           #cream toate legaturile intre stari

    else:  # daca cuvantul nu exista

       tranzitii[("#", "#")] = "#"  # adaugam o tranzitie de la lambda la lambda
            
stari_finale.append(nr)


#creem o legatura intre starea finala si cuvantul acesteia


cuvant.reverse()    
stari_finale.reverse()

for i in range(len(stari_finale)-1):
   starefinala_cuvant[cuvant[i]]=stari_finale[i]


#starea initiala de la care pleaca fiecare cuvant in automat
stare_initiala = t

# creez automatul finit dupa cuvinte

afn = NFA(cuvinte,tranzitii,date_intrare,stare_initiala,stari_finale,starefinala_cuvant)

#afisez automatul finit 

afn.print_afn()



        
# se introduce de la tastatura numele fisierului si se deschide acesta

file=input("Introduceti numele fisierului in care se v-a face cautarea:")

with open(f"{file}","r") as f:
   
    #creem un dictionar pentru a numara de cate ori apare fiecare cuvant
   
    nr={}

    for i in starefinala_cuvant:  
        nr[i]=0
    
    #creem o lista initiala in care cautam starile precedente 
    curent=[]
    curent.append(0)
    
    # parcurgem fisierul caracter cu caracter 

    for nr_linie, line in enumerate(f,1):
         for nr_coloana, c in enumerate(line,1):
             
             # creem o noua lista secundara in care punem starile succesoare 

             next=[]
             next.append(0)
             # cautam in lista initiala si adaugam in lista secundara starile succesoare 
             for j in curent:
                for i in tranzitii:
                    if c==tranzitii[i]:
                        if j==i[0]:
                             next.append(i[1])
             
             # pregatim lista initiala pentru o noua cautare 
             curent=next.copy()

             # afisam linia, coloana unde a fost gasit cuvantul inclusiv acesta
             for i in starefinala_cuvant:                
                  if starefinala_cuvant[i] in curent:
                       print("Linia:", nr_linie, "Coloana:", nr_coloana, "Cuvantul:", i)
                       # numaram de cate ori apare cuvantul in fisier
                       nr[i]=nr[i]+1
                       # eiiminam starea finala deja afisata
                       curent.remove(starefinala_cuvant[i])

# afisam de cate ori a aparut fiecare cuvant
for i in starefinala_cuvant:  
        print(f"{i} a aparut de {nr[i]} ori")
     
    