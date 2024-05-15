#include <stdio.h>
#include <stdlib.h>

typedef struct nume
{
    char nume[100];

}nume;



typedef struct arce
{
    char head[100];
    char tail[100];
    char alfabet[100];

}arc;



int x, numar_stari,numar_arce,numar_alfabet,numar_stari_initiale,numar_stari_finale;
arc arce[100];
nume stari[100];
nume alfabet[100];
nume stare_initiala[100];
nume stare_finala[100];
nume curent;

int Initial(char nume[])
{

for(int i=0;i<numar_stari_initiale;i++)
    {
    if(strcmp(nume,stare_initiala[i].nume)==0)
            {
                return 1;
            }

    }
    return 0;
}
int Final(char nume[])
{
for(int i=0;i<numar_stari_finale;i++)
    {
    if(strcmp(nume,stare_finala[i].nume)==0)
            {
                return 1;
            }

    }
    return 0;
}

void Input(){

        int i;
        char head[100],tail[100],alfabet[100],aux[100], *p;
        FILE *fisier;
        fisier=fopen("input.txt","r");
        // stari initiale

        fgets(aux,255,fisier);
        i=0;
        p=strtok(aux," , ");
        while (p!=NULL){

                strcpy(stare_initiala[i].nume,p);
                i++;
                p= strtok(NULL,",");


        }

        p= strtok(stare_initiala[i-1].nume,"\n");
        strcpy(stare_initiala[i-1].nume,p);

        numar_stari_initiale=i;

        // stari finale

        fscanf(fisier,"%s\0", aux);
        i=0;
        p=strtok(aux," , ");
        while(p != NULL){

            strcpy(stare_finala[i].nume,p);
            i++;
            p=strtok(NULL,",");

        }

        numar_stari_finale=i;

        // arcele automatului

        i=-1;
        while(!feof(fisier)){

            i++;
            fscanf(fisier,"%s %s %s",arce[i].head,arce[i].tail,arce[i].alfabet);

        }


        numar_arce=i;
        fclose(fisier);

}


void AfisareArce(){
    for(int i=0;i<numar_arce;i++)
        {
        printf("--------------------\n");
        printf("    (%s)->(%s)=(%s)  \n",arce[i].head,arce[i].tail,arce[i].alfabet);

    }


}


void Automat()
{

    int si=0, ai=0, b, j;

    //adaugare stari
    strcpy(stari[0].nume, arce[0].head);
    numar_stari=1;
    si=1;

    for(int i=0; i<numar_arce; i++)
    {
        b=0;
        for(j=0; j<numar_stari; j++)
        {


            if(strcmp(arce[i].head,stari[j].nume)==0 )
            {
                b=1;
            }



        }

        if(b==0)
        {

            strcpy(stari[si].nume, arce[i].head);
            si++;
            numar_stari++;


        }

        b=0;
        for(j=0; j< numar_stari; j++)
        {
            if(strcmp(arce[i].tail, stari[j].nume)==0)
            {

                b=1;
            }
        }

        if(b==0)
        {
            strcpy(stari[si].nume, arce[i].tail);
            si++;
            numar_stari++;


        }


    }

    strcpy(alfabet[0].nume, arce[0].alfabet);
    numar_alfabet=1;
    ai=1;
    for(int i=0; i<numar_arce; i++)
    {
        b=0;
        for(j=0; j<numar_alfabet; j++)
        {
            if(strcmp(arce[i].alfabet,alfabet[j].nume)==0)
            {
                b=1;
            }
        }

        if(b==0)
        {
            strcpy(alfabet[ai].nume, arce[i].alfabet);
            ai++;
            numar_alfabet++;

        }


    }


}

void AfisareAutomat(){
    int j;
    Input();
    Automat();
    AfisareArce();
    printf("\n Numar de stari:  %d",numar_stari);

    for(j=0;j< numar_stari;j++)
    {
        if(Initial(stari[j].nume)== 1 && Final(stari[j].nume)== 1)
        {
        printf("\n ->(%s)<- ",stari[j].nume);
        }
        else
        {
            if(Initial(stari[j].nume)==1)
                {
               printf("\n ->(%s) ",stari[j].nume);
                }
            else
            {
            if(Final(stari[j].nume)==1)
                {
                printf("\n (%s)<- ",stari[j].nume);
                }
                else
                    {
                    printf("\n (%s) ",stari[j].nume);
                    }
            }
        }



    }

    printf("\n numar de litere: %d",numar_alfabet);
    for(j=0;j<numar_alfabet;j++)
        {

        printf("\n   %s    ", alfabet[j].nume);
        }



    }



int main()

{
    AfisareAutomat();
    printf("\n");


    char cuvant[100];
    int lungime;


    printf("Lungimea cuvantului de analizat: ");

    scanf("%d",&lungime);
    printf("\n");

    printf("Cuvantul de analizat: ");

    for(int i=0;i<=lungime;i++)
    {
        scanf("%c",&cuvant[i]);

    }
    printf("\n");

    int j=0;

    for (int i=0;i<=numar_arce;i++)
        {

        printf(arce[i].head);

         printf(arce[i].tail);
          printf(arce[i].alfabet);



    }
    while( j<numar_stari_initiale)
        {

            printf("%s ",curent.nume);
            printf("Posibilitati:");
            for (int i=0;i<=numar_arce;i++)
            {

                if(strcmp(stare_initiala[j],arce[i].head)==0)
                    {
                    for(int k=0;k<=lungime;k++)
                    {
                        if(strcmp(cuvant[k],arce[i].alfabet)==0)
                        printf("%s",arce[i].tail);
                    }
                    }
                    }




                j++;
            }











    return 0;
}
