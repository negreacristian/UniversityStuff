#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <windows.h>


void RED(){

      printf("\033[1;35m");
}
void YELLOW(){
    printf("\033[1;33m");
}
void GREEN(){
    printf("\033[0;32m");
}
void BLUE(){
    printf("\033[0;34m");
}
void reset() {
    printf("\033[0m");
}




void antet(){

    printf("#===================================#\n");
    printf("|           Cristi.Music            |\n");
    printf("#===================================#\n");
    printf("|              MENIU                |\n");
    printf("#===================================#\n");
    printf("|       1 - Creare Playlist         |\n");
    printf("|       2 - Vizualizare Playlisturi |\n");
    printf("|       3 - Stergere Playlist       |\n");
    printf("|       0 - EXIT!                   |\n");
    printf("#===================================#\n");

}
void antet2(){
    printf("#===================================#\n");
    printf("|        1 - Adaugare Melodie       |\n");
    printf("|        2 - Stergere Melodie       |\n");
    printf("|        0 - Exit                   |\n");
    printf("#===================================#\n");

}
void antet1(){

    printf("#===================================#\n");
    printf("#       1 - Selecteaza playlist     #\n");
    printf("#       0 - EXIT!                   #\n");
    printf("#===================================#\n");

}
void antet3(){


    printf("#===================================#\n");
    printf("#         Selecteaza playlist       #\n");
    printf("#===================================#\n");

}




int numar_playlist;
char nume_playlist[20][10];
int numar_melodii_playlist[20];
char nume_melodii_playlist[20][15][11];
double rating_melodii[20][20][20];

void citire_playlist()
{
    int i,j;
    FILE * fp2 = fopen("playlisturi.txt", "r");
    fscanf(fp2, "%d", &numar_playlist);


    for(i = 0; i < numar_playlist; i++)
    {
        fscanf(fp2, "%s", nume_playlist[i]);
        fscanf(fp2, "%d", &numar_melodii_playlist[i]);
        for(j = 0; j < numar_melodii_playlist[i]; j++){
            fscanf(fp2, "%s ", nume_melodii_playlist[i][j]);
            fscanf(fp2,"%lf",&rating_melodii[i][j]);

        }

    }
    fclose(fp2);
}


void salvare(){
     FILE * filePointer;
     filePointer = fopen("playlisturi.txt", "w");
    int i,j;
     if ( filePointer == NULL )
    {
        printf( "Playlistul nu poate fi creat." ) ;
    }
    else{
            fprintf(filePointer,"%d\n",numar_playlist);

            for(i = 0; i <numar_playlist; i++)
    {
        fprintf(filePointer, "%s\n", nume_playlist[i]);
        fprintf(filePointer, "%d\n", numar_melodii_playlist[i]);

        for(j=0; j<numar_melodii_playlist[i]; j++){


        fprintf(filePointer,"%s ",nume_melodii_playlist[i][j]);
        fprintf(filePointer,"%.2lf\n",*rating_melodii[i][j]);



        }

        }


}
 fclose(filePointer) ;
}


void adaugare() {
     system("cls");
     printf("#===================================#\n");
     printf("#           Adaugare Playlist       #\n");
     printf("#===================================#\n");


     int i,j;


     numar_playlist=numar_playlist+1;
     printf("#       Introduceti nume playlist:   ");


     scanf("%s",&nume_playlist[numar_playlist-1]);
     getchar();
     numar_melodii_playlist[numar_playlist]=0;

    system("cls");

     printf("#===================================#\n");
     printf("#       Playlistul a fost adaugat   #\n");
     printf("#===================================#\n");



    }

void stergere1(){



    system("cls");
     printf("#===================================#\n");
     printf("#           Stergere Melodie        #\n");
     printf("#===================================#\n");

     int i,j,jo;
     char nume[20];


     jo=numar_melodii_playlist[numar_playlist-1];

     i=numar_playlist-1;


        printf("#    Playlistul %s\n",nume_playlist[i]);
        printf("#--------------------------------------\n");
        for(j=0;j<numar_melodii_playlist[i];j++){

            printf("#        %d.%s  %.2lf\n",j+1,nume_melodii_playlist[i][j],*rating_melodii[i][j]);

        }


    printf("#-------Introduceti numar melodie:   ");

     getchar();

     printf("#-------Introduceti nume melodie:   ");

     getchar();
     scanf("%s",&nume_melodii_playlist[i][j]);







     printf("#-------Introduceti rating melodie:   ");

     scanf("%lf",&rating_melodii[i][j]);


     getchar();
     numar_melodii_playlist[numar_playlist-1]=numar_melodii_playlist[numar_playlist-1]-1;

     system("cls");
     printf("#===================================#\n");
     printf("#       Melodia a fost stearsa      #\n");
     printf("#===================================#\n");






}

void adaugare1() {


     system("cls");
     printf("#===================================#\n");
     printf("#           Adaugare Melodie        #\n");
     printf("#===================================#\n");


     int i,j;
     char nume[20];


     j=numar_melodii_playlist[numar_playlist-1];

     i=numar_playlist-1;

     printf("#-------Introduceti nume melodie:   ");

     getchar();
     scanf("%s",&nume_melodii_playlist[i][j]);







     printf("#-------Introduceti rating melodie:   ");

     scanf("%lf",&rating_melodii[i][j]);


     getchar();
     numar_melodii_playlist[numar_playlist-1]=numar_melodii_playlist[numar_playlist-1]+1;

     system("cls");
     printf("#===================================#\n");
     printf("#       Melodia a fost adaugata     #\n");
     printf("#===================================#\n");


    }

void vizualizare() {


    system("cls");
    printf("#===================================#\n");
    printf("|         Afisare Playlisturi       |\n");
    printf("#===================================#\n");
    int i,j;
    double rating[20];
    double rat;
    double contor;
    double aux;
    char afis[20][15];
    char nume[20];


            for(i = 0; i <numar_playlist; i++)
    {
        rat=0;
        contor=0;
        strcpy(afis[i],nume_playlist[i]);
        for(j=0; j<numar_melodii_playlist[i]; j++){

            rat=rat+*rating_melodii[i][j];
            contor++;

        }
        rating[i]=rat/contor;
        }



        for(i=0;i<numar_playlist-1;i++){
                for(j=i;j<numar_playlist;j++){


                    if(rating[i]>rating[j]){
                            aux=rating[i];
                            rating[i]=rating[j];
                            rating[j]=aux;
                            strcpy(nume,afis[i]);
                            strcpy(afis[i],afis[j]);
                            strcpy(afis[j],nume);





                    }
                }




        }
        for(i=numar_playlist-1;i>=0;i--){
        printf( "%s ", afis[i]);
        printf( "%.2lf\n", rating[i]);
}
    printf("+-----------------------------------+\n");

    printf("Apasa orice tasta pentru a continua\n");
    getch();


}


void viz(){
        system("cls");
        antet3();
        int ops;
        int i,j;
        for(i=0;i<numar_playlist;i++){

            printf("+              %d.%s\n",i+1,nume_playlist[i]);




        }
        printf("+Introdu numarul aferent playlistului dorit:");
        scanf("%d",&ops);
        getchar();

        system("cls");

    for(i=0;i<numar_playlist;i++){
        if(ops-1==i){
        printf("#    Playlistul %s\n",nume_playlist[i]);
        printf("#--------------------------------------\n",nume_playlist[i]);
        for(j=0;j<numar_melodii_playlist[i];j++){

            printf("#        %d.%s  %.2lf\n",j+1,nume_melodii_playlist[i][j],*rating_melodii[i][j]);

        }
        }
        }
        printf("Apasa orice tasta pentru a continua\n");
        getch();
        meniu3();





}


void viz1(){
    system("cls");
        antet3();
        int ops;
        int i,j;
        for(i=0;i<numar_playlist;i++){

            printf("+              %d.%s\n",i+1,nume_playlist[i]);




        }
        printf("+Introdu numarul aferent playlistului dorit:");
        scanf("%d",&ops);
        getchar();




}


void meniu3(){
     antet1();
     int ops;


     printf("#-------------Introduceti optiunea: ");
    scanf("%d",&ops);
    system("cls");
   if(ops==1){
         viz();





        }
    else{
        printf("EXIT!\n");
        }

}


void meniu2(){
    int opt;
    antet2();
    printf("#-------Introduceti optiunea: ");
    scanf("%d",&opt);


    switch(opt){

case 1:
    adaugare1();

    salvare();
    meniu2();
    break;
case 2:

    break;
default:
    printf("EXIT!\n");



    }

    system("cls");


}

void meniu(int op){


    switch(op)
    {
    case 1:
        adaugare();
        salvare();
        meniu2();
        break;
    case 2:
        vizualizare();
        meniu3();

        break;
    case 3:
        viz1();
        system("cls");
        break;
    default:

        printf("EXIT!\n");


    }
}

int main()
{

    int optiune;


    citire_playlist();




     do{

        antet();

        printf("#Introduceti optiunea:");

        scanf("%d",&optiune);

        meniu(optiune);

    } while(optiune>0 && optiune<=3);

    return 0;
}
