#include <Arduino.h>
#include <Mux.h>
#include <LiquidCrystal_I2C.h>

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
                          {4, 0}}

int address_mux3[8][2] = {{0, 4},
                          {15, 11},
                          {1, 5},
                          {14, 10},
                          {2, 6},
                          {13, 9},
                          {3, 7},
                          {12, 8}}

int address_mux2[8][2] = {{8, 12},
                          {7, 3},
                          {9, 13},
                          {6, 2},
                          {10, 14},
                          {5, 1},
                          {11, 15},
                          {4, 0}}

int address_mux1[8][2] = {{0, 4},
                          {15, 11},
                          {1, 5},
                          {14, 10},
                          {2, 6},
                          {13, 9},
                          {3, 7},
                          {12, 8}}

int enable1 = ENABLE1;
int enable2 = ENABLE2;
int enable3 = ENABLE3;
int enable4 = ENABLE4;

byte tabuleiro[8][8];
byte tabuleiro_atual[8][8];
byte tabuleiro_memoria[8][8];
byte tabuleiro_depois[8][8];
byte tabuleiro_captura[8][8];

Mux mux1(Pin(SIG, INPUT_PULLUP, PinType::Digital), Pinset(S0, S1, S2, S3));
Mux mux2(Pin(SIG, INPUT_PULLUP, PinType::Digital), Pinset(S0, S1, S2, S3));
Mux mux3(Pin(SIG, INPUT_PULLUP, PinType::Digital), Pinset(S0, S1, S2, S3));
Mux mux4(Pin(SIG, INPUT_PULLUP, PinType::Digital), Pinset(S0, S1, S2, S3));

void lertabuleiro_aposrobo()
{

  int coluna = 0;
  int linha = 0;
  digitalWrite(enable1, LOW);
  digitalWrite(enable2, HIGH);
  digitalWrite(enable3, HIGH);
  digiralWrite(enable4, HIGH);
  for (int i = 0; i < mux1.channelCount(); i++)
  {
    leitura_atual[linha][coluna] = mux1.read(address_mux1[linha][coluna]);

    if (linha == 7)
    {
      linha = 0;
      coluna++;
    }
    else
    {
      linha++;
    }
  }

  linha = 0;
  digitalWrite(enable1, HIGH);
  digitalWrite(enable2, LOW);
  for (int i = 0; i < mux2.channelCount(); i++)
  {
    leitura_atual[linha][coluna] = mux2.read(address_mux2[linha][coluna]);
    // Serial.print("Push button at channel "); Serial.print(i); Serial.print(" is "); Serial.println(data == LOW ? "pressed" : "not pressed");
    if (linha == 7)
    {
      linha = 0;
      coluna++;
    }
    else
    {
      linha++;
    }
  }
  linha = 0;
  digitalWrite(enable2, HIGH);
  digitalWrite(enable3, LOW);
  for (byte i = 0; i < mux3.channelCount(); i++)
  {
    leitura_atual[linha][coluna] = mux3.read(address_mux3[linha][coluna]);
    // Serial.print("Push button at channel "); Serial.print(i); Serial.print(" is "); Serial.println(data == LOW ? "pressed" : "not pressed");
    if (linha == 7)
    {
      linha = 0;
      coluna++;
    }
    else
    {
      linha++;
    }
  }
  linha = 0;
  digitalWrite(enable3, HIGH);
  digitalWrite(enable4, LOW);
  for (byte i = 0; i < mux4.channelCount(); i++)
  {
    leitura_atual[linha][coluna] = mux4.read(address_mux4[linha][coluna]);
    // Serial.print("Push button at channel "); Serial.print(i); Serial.print(" is "); Serial.println(data == LOW ? "pressed" : "not pressed");
    if (linha == 7)
    {
      linha = 0;
      coluna++;
    }
    else
    {
      linha++;
    }
  }
}

void lertabuleiro_humano()
{

  for (int i = 0; i < 8; i++)
  {
    for (int j = 0; j < 8; j++)
    {
      tabuleiro_memoria[i][j] = tabuleiro_atual[i][j];
    }
  }

  int coluna = 0;
  int linha = 0;
  digitalWrite(enable1, LOW);
  digitalWrite(enable2, HIGH);
  digitalWrite(enable3, HIGH);
  digiralWrite(enable4, HIGH);
  for (int i = 0; i < mux1.channelCount(); i++)
  {
    leitura_atual[linha][coluna] = mux1.read(address_mux1[linha][coluna]);

    if (linha == 7)
    {
      linha = 0;
      coluna++;
    }
    else
    {
      linha++;
    }
  }

  linha = 0;
  digitalWrite(enable1, HIGH);
  digitalWrite(enable2, LOW);
  for (int i = 0; i < mux2.channelCount(); i++)
  {
    leitura_atual[linha][coluna] = mux2.read(address_mux2[linha][coluna]);
    // Serial.print("Push button at channel "); Serial.print(i); Serial.print(" is "); Serial.println(data == LOW ? "pressed" : "not pressed");
    if (linha == 7)
    {
      linha = 0;
      coluna++;
    }
    else
    {
      linha++;
    }
  }
  linha = 0;
  digitalWrite(enable2, HIGH);
  digitalWrite(enable3, LOW);
  for (int i = 0; i < mux3.channelCount(); i++)
  {
    leitura_atual[linha][coluna] = mux3.read(address_mux3[linha][coluna]);
    // Serial.print("Push button at channel "); Serial.print(i); Serial.print(" is "); Serial.println(data == LOW ? "pressed" : "not pressed");
    if (linha == 7)
    {
      linha = 0;
      coluna++;
    }
    else
    {
      linha++;
    }
  }
  linha = 0;
  digitalWrite(enable3, HIGH);
  digitalWrite(enable4, LOW);
  for (int i = 0; i < mux4.channelCount(); i++)
  {
    leitura_atual[linha][coluna] = mux4.read(address_mux4[linha][coluna]);
    // Serial.print("Push button at channel "); Serial.print(i); Serial.print(" is "); Serial.println(data == LOW ? "pressed" : "not pressed");
    if (linha == 7)
    {
      linha = 0;
      coluna++;
    }
    else
    {
      linha++;
    }
  }
}

void qualmovimento()
{

  for (byte i = 0; i < 8; i++)
  {
    for (byte j = 0; j < 8; j++)
    {
      if (leitura_atual[i][j] != leitura_memoria[i][j])
      {
        if (leitura_memoria[i][j] == 0)
        {
          moveu_coluna[0] = i;
          moveu_linha[0] = j;
        }
        if (leitura_memoria[i][j] == 1)
        {
          moveu_coluna[1] = i;
          moveu_linha[1] = j;
        }
      }
    }
  }
  //  Convert the reed sensors switches coordinates in characters
  char table1[] = {'8', '7', '6', '5', '4', '3', '2', '1'};
  char table2[] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'};

  mov[0] = table2[moveu_linha[0]];
  mov[1] = table1[moveu_coluna[0]];
  mov[2] = table2[moveu_linha[1]];
  mov[3] = table1[moveu_coluna[1]];

  // apos isso, mandar para o python a string
  // "mov[0]mov[1]mov[2]mov[3]"
}

LiquidCrystal_I2C lcd(03XF, 16, 2);

void lcdIniciaGame()
{
  lcd.clear();
  lcd.setCursor(0, 0);       // selecionando coluna 0 e linha 0
  lcd.print("Aperte SIM");   // print da mensagem
  lcd.setCursor(2, 1);       // selecionando coluna 2 e linha 1
  lcd.print("para iniciar"); // Print da mensagem
  delay(1000);               // atraso de 1 segundo
}

void lcdAskVaiComer()
{
  lcd.clear();
  lcd.setCursor(0, 0);         // selecionando coluna 0 e linha 0
  lcd.print("Voce ira comer"); // print da mensagem
  lcd.setCursor(2, 1);         // selecionando coluna 2 e linha 1
  lcd.print("uma peca?");      // Print da mensagem
  delay(200);                  // atraso de 1 segundo
}

void lcdShowRemovaPeca()
{
  lcd.clear();
  lcd.setCursor(0, 0);        // selecionando coluna 0 e linha 0
  lcd.print("Remova a peca"); // print da mensagem
  lcd.setCursor(2, 1);        // selecionando coluna 2 e linha 1
  lcd.print("a ser comida");  // Print da mensagem
  delay(200);                 // atraso de 1 segundo
}

void lcdShowMovaPeca()
{
  lcd.clear();
  lcd.setCursor(0, 0);          // selecionando coluna 0 e linha 0
  lcd.print("Mova a sua peca"); // print da mensagem
  lcd.setCursor(2, 1);          // selecionando coluna 2 e linha 1
  lcd.print("para a casa");     // Print da mensagem
  delay(200);                   // atraso de 1 segundo
}

void lcdShowFacaJogada()
{
  lcd.clear();
  lcd.setCursor(0, 0);     // selecionando coluna 0 e linha 0
  lcd.print("Faca a sua"); // print da mensagem
  lcd.setCursor(2, 3);     // selecionando coluna 2 e linha 1
  lcd.print("jogada");     // Print da mensagem
  delay(200);              // atraso de 1 segundo
}

void setup()
{
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  pinMode(enable1, OUTPUT);
  pinMode(enable2, OUTPUT);
  pinMode(enable3, OUTPUT);
  pinMode(enable4, OUTPUT);
}

void loop()
{
  byte data;

  int linha = 0;
  int coluna = 0;

  int x = 0;
  int y = 0;

  for (x = 0; x < 8; x++)
  {
    Serial.print("");
    for (y = 0; y < 8; y++)
    {
      Serial.print(tabuleiro_atual[x][y]);
    }
    Serial.print("\n");
  }
  delay(5000);
  Serial.println();
}
