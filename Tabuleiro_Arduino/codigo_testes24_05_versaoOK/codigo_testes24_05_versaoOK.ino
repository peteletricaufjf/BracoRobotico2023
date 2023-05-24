#include <Arduino.h>
#include <Mux.h>

#define SIG 3
#define S0 A0
#define S1 A1
#define S2 A2
#define S3 A3
#define ENABLE3 6
#define ENABLE4 7
#define ENABLE1 8
#define ENABLE2 9
using namespace admux;


int address_mux4[8][2] = {{8, 12},
                          {7, 3},
                          {9, 13},
                          {6, 2},
                          {10, 14},
                          {5, 1},
                          {11, 15},
                          {4, 0}};

int address_mux3[8][2] = {{0, 4},
                          {15, 11},
                          {1, 5},
                          {14, 10},
                          {2, 6},
                          {13, 9},
                          {3, 7},
                          {12, 8}};

int address_mux2[8][2] = {{8, 12},
                          {7, 3},
                          {9, 13},
                          {6, 2},
                          {10, 14},
                          {5, 1},
                          {11, 15},
                          {4, 0}};

int address_mux1[8][2] = {{0, 4},
                          {15, 11},
                          {1, 5},
                          {14, 10},
                          {2, 6},
                          {13, 9},
                          {3, 7},
                          {12, 8}};

int enable1 = ENABLE1;
int enable2 = ENABLE2;
int enable3 = ENABLE3;
int enable4 = ENABLE4;

byte tabuleiro[8][8];
byte tabuleiro_atual[8][8];
byte leitura_atual[8][8];
byte leitura_memoria[8][8];
byte tabuleiro_memoria[8][8];
byte tabuleiro_depois[8][8];
byte tabuleiro_captura[8][8];

Mux mux1(Pin(SIG, INPUT_PULLUP, PinType::Digital), Pinset(S0, S1, S2, S3));
Mux mux2(Pin(SIG, INPUT_PULLUP, PinType::Digital), Pinset(S0, S1, S2, S3));
Mux mux3(Pin(SIG, INPUT_PULLUP, PinType::Digital), Pinset(S0, S1, S2, S3));
Mux mux4(Pin(SIG, INPUT_PULLUP, PinType::Digital), Pinset(S0, S1, S2, S3));


void lertabuleiro_humano()
{

  int coluna = 0;
  int linha = 0;
  int colunale;
  int linhale;
  digitalWrite(enable4, LOW);
  digitalWrite(enable2, HIGH);
  digitalWrite(enable3, HIGH);
  digitalWrite(enable1, HIGH);
  linhale = 0;
  colunale = 0;
  for (int i = 0; i < 16; i++)
  {
    leitura_atual[linha][coluna] = mux4.read(address_mux4[linhale][colunale]);

    if (linha == 7)
    {
      linha = 0;
      linhale = 0;
      coluna++;
      colunale++;
    }
    else
    {
      linha++;
      linhale++;
    }
  }

  linha = 0;
  linhale = 0;
  colunale = 0;
  digitalWrite(enable4, HIGH);
  digitalWrite(enable3, LOW);
  for (int i = 0; i < 16 ; i++)
  {
    leitura_atual[linha][coluna] = mux3.read(address_mux3[linhale][colunale]);
    // Serial.print("Push button at channel "); Serial.print(i); Serial.print(" is "); Serial.println(data == LOW ? "pressed" : "not pressed");
    if (linha == 7)
    {
      linha = 0;
      linhale =0;
      coluna++;
      colunale++;
    }
    else
    {
      linha++;
      linhale++;
    }
  }
  linha = 0;
  linhale = 0;
  colunale = 0;
  digitalWrite(enable3, HIGH);
  digitalWrite(enable2, LOW);
  for (int i = 0; i < 16; i++)
  {
    leitura_atual[linha][coluna] = mux2.read(address_mux2[linhale][colunale]);
    // Serial.print("Push button at channel "); Serial.print(i); Serial.print(" is "); Serial.println(data == LOW ? "pressed" : "not pressed");
    if (linha == 7)
    {
      linha = 0;
      linhale = 0;
      coluna++;
      colunale++;
    }
    else
    {
      linha++;
      linhale++;
    }
  }
  linha = 0;
  linhale = 0;
  colunale = 0;
  digitalWrite(enable2, HIGH);
  digitalWrite(enable1, LOW);
  for (int i = 0; i < 16; i++)
  {
    leitura_atual[linha][coluna] = mux1.read(address_mux1[linhale][colunale]);
    // Serial.print("Push button at channel "); Serial.print(i); Serial.print(" is "); Serial.println(data == LOW ? "pressed" : "not pressed");
    if (linha == 7)
    {
      linha = 0;
      linhale = 0;
      coluna++;
      colunale++;
    }
    else
    {
      linha++;
      linhale++;
    }
  }
  for (int i = 0; i < 8; i++)
  {
    for (int j = 0; j < 8; j++)
    {
      tabuleiro_atual[i][j] = leitura_atual[i][j];
    }
  }
}

void transporMatriz(byte matrix[8][8]) {
  for (int i = 0; i < 8; i++) {
    for (int j = i + 1; j < 8; j++) {
      // Swap elements (i, j) and (j, i)
      int temp = matrix[i][j];
      matrix[i][j] = matrix[j][i];
      matrix[j][i] = temp;
    }
  }
}


void setup() {
  Serial.begin(9600);
  pinMode(enable1, OUTPUT);
  pinMode(enable2, OUTPUT);
  pinMode(enable3, OUTPUT);
  pinMode(enable4, OUTPUT);

}

void loop() {

  int x = 0;
  int y = 0;

  lertabuleiro_humano();
  transporMatriz(leitura_atual);
  for (x = 0; x < 8; x++)
  {
    Serial.print("");
    for (y = 7 ; y > -1 ; y--)
    {
      Serial.print(leitura_atual[x][y]);
    }
    Serial.print("\n");
  }
  delay(2500);
  Serial.println();

}
