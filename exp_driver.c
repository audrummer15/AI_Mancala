#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define NB_COLUMN_VALUES 3
#define NB_PEBBLE_VALUES 3
#define NB_PLY_VALUES 3
#define HEURISTIC_1 1
#define HEURISTIC_2 2
#define AND_OR 1
#define ALPHA_BETA 2

void error(char *str);

int main (int argc, char **argv){
  FILE *output;
  
  int   columnValues[NB_COLUMN_VALUES] = {2, 4, 5};

  int   pebbleValues[NB_PEBBLE_VALUES] = {1, 2, 3};

  int   plyValues[NB_PLY_VALUES] = {1, 3, 5};

  int columnCounter = 0, pebbleCounter = 0, plyCounter = 0;
  int p1Algorithm, p2Algorithm;
  int p1Heuristic, p2Heuristic;

  char python_command[512];

  srand(time(NULL));

  for(columnCounter = 0; columnCounter < NB_COLUMN_VALUES; columnCounter++ ) {
    int columnValue = columnValues[columnCounter]; // for readability

    for(pebbleCounter = 0; pebbleCounter < NB_PEBBLE_VALUES; pebbleCounter++ ) {
      int pebbleValue = pebbleValues[pebbleCounter];

      for(plyCounter = 0; plyCounter < NB_PLY_VALUES; plyCounter++ ) {
        int plyValue = plyValues[plyCounter];

        for(p1Algorithm = AND_OR; p1Algorithm <= ALPHA_BETA; p1Algorithm++ ) {

          for( p2Algorithm = AND_OR; p2Algorithm <= ALPHA_BETA; p2Algorithm++ ) {

            for( p1Heuristic = HEURISTIC_1; p1Heuristic <= HEURISTIC_2; p1Heuristic++ ) {

              for( p2Heuristic = HEURISTIC_1; p2Heuristic <= HEURISTIC_2; p2Heuristic++ ) {
                
                sprintf( python_command, "python pebbleAuto.py %d %d %d %d %d %d %d", columnValue, pebbleValue, plyValue, p1Algorithm, p2Algorithm, p1Heuristic, p2Heuristic );
                system(python_command);

                int winner = 0;
                FILE *input = fopen("auto_out.res", "r");

                fscanf(input, "%d", &winner);

                output = fopen("output.txt","a+");

                if (!output)
                    error("Error Opening output file 'output.txt'\n");

                fprintf(output, "%d %d %d %d %d %d %d - %d\n", columnValue, pebbleValue, plyValue, p1Algorithm, p2Algorithm, p1Heuristic, p2Heuristic, winner);
                fclose(output);
              }
            }
          }
        }
      }
    }
  }

  return 0;
}

void error(char *str){
  printf("%s",str);
  exit(1);
}