#include <Arduino.h>
#include <Mux.h>
#include <LiquidCrystal_I2C.h>


#define BOTAOSIM 3   //pino do botao de sim
#define BOTAONAO 2   //pino do botao de nao

#define SIG 4
#define S0 A0
#define S1 A1
#define S2 A2
#define S3 A3
#define ENABLE1 8
#define ENABLE2 9
#define ENABLE3 10
#define ENABLE4 11
using namespace admux;
#define a1 6

LiquidCrystal_I2C lcd(0x27, 16,2);


int address_mux4[2][8] = {{4,11,5,10,6,9,7,8},
                          {0,15,1,14,2,13,3,12}};

int address_mux3[2][8] = {{12,3,13,2,14,1,15,0},
                           {8,7,9,6,10,5,11,4}};

int address_mux2[2][8] = {{4,11,5,10,6,9,7,8},
                          {0,15,1,14,2,13,3,12}};

int address_mux1[2][8] = {{12,3,13,2,14,1,15,0},
                           {8,7,9,6,10,5,11,4}};


int enable1 = ENABLE1;
int enable2 = ENABLE2;
int enable3 = ENABLE3;
int enable4 = ENABLE4;

int botaosim = BOTAOSIM;
int botaonao = BOTAONAO;

byte tabuleiro[8][8];
byte tabuleiro_atual[8][8];
byte leitura_atual[8][8];
byte leitura_memoria[8][8];
byte tabuleiro_memoria[8][8];
byte tabuleiro_depois[8][8];
byte tabuleiro_captura[8][8];
char mov[]={'a','a','a','a'};
int moveu_coluna[]={0,0};
int moveu_linha[]={0,0};

Mux mux1(Pin(SIG, INPUT_PULLUP, PinType::Digital), Pinset(S0, S1, S2, S3));
Mux mux2(Pin(SIG, INPUT_PULLUP, PinType::Digital), Pinset(S0, S1, S2, S3));
Mux mux3(Pin(SIG, INPUT_PULLUP, PinType::Digital), Pinset(S0, S1, S2, S3));
Mux mux4(Pin(SIG, INPUT_PULLUP, PinType::Digital), Pinset(S0, S1, S2, S3));

void qualmovimento()
{
  
  for (byte i = 0; i < 8; i++)
  {
    for (byte j = 0; j < 8; j++)
    {
      if (tabuleiro_atual[i][j] != tabuleiro_memoria[i][j])
      {
        if (tabuleiro_memoria[i][j] == 0)
        {
          moveu_coluna[0] = i;
          moveu_linha[0] = j;
        }
        if (tabuleiro_memoria[i][j] == 1)
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

void lertabuleiro_humano()
{
  for(int x = 0;x<8;x++){
    for(int y = 0;y<8;y++){
      tabuleiro_memoria[x][y] = tabuleiro_atual[x][y];
    }
  }
  
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

    if (coluna == 7)
    {
      coluna = 0;
      colunale = 0;
      linha++;
      linhale++;
    }
    else
    {
      coluna++;
      colunale++;
    }
  }

  coluna = 0;
  linhale = 0;
  colunale = 0;
  digitalWrite(enable4, HIGH);
  digitalWrite(enable3, LOW);
  for (int i = 0; i < 16; i++)
  {
    leitura_atual[linha][coluna] = mux3.read(address_mux3[linhale][colunale]);

    if (coluna == 7)
    {
      coluna = 0;
      colunale = 0;
      linha++;
      linhale++;
    }
    else
    {
      coluna++;
      colunale++;
    }
  }

  coluna = 0;
  linhale = 0;
  colunale = 0;
  digitalWrite(enable3, HIGH);
  digitalWrite(enable2, LOW);
  for (int i = 0; i < 16; i++)
  {
    leitura_atual[linha][coluna] = mux2.read(address_mux2[linhale][colunale]);

    if (coluna == 7)
    {
      coluna = 0;
      colunale = 0;
      linha++;
      linhale++;
    }
    else
    {
      coluna++;
      colunale++;
    }
  }

  coluna = 0;
  linhale = 0;
  colunale = 0;
  digitalWrite(enable2, HIGH);
  digitalWrite(enable1, LOW);
  for (int i = 0; i < 16; i++)
  {
    leitura_atual[linha][coluna] = mux1.read(address_mux1[linhale][colunale]);

    if (coluna == 7)
    {
      coluna = 0;
      colunale = 0;
      linha++;
      linhale++;
    }
    else
    {
      coluna++;
      colunale++;
    }
  }
  leitura_atual[7][7] = digitalRead(a1);
  for(int x = 0;x<8;x++){
    for(int y = 0;y<8;y++){
      tabuleiro_atual[x][y] = leitura_atual[x][y];
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

void lcdIniciaGame(){
  lcd.clear();
  lcd.setCursor(2, 0);            // selecionando coluna 0 e linha 0
  lcd.print("Aperte SIM");   // print da mensagem
  lcd.setCursor(2, 1);            // selecionando coluna 2 e linha 1
  lcd.print("para iniciar");       // Print da mensagem
  delay(1000);                    // atraso de 1 segundo
}

void lcdAskVaiComer(){
  lcd.clear();
  lcd.setCursor(1, 0);            // selecionando coluna 0 e linha 0
  lcd.print("Voce ira comer");   // print da mensagem
  lcd.setCursor(3, 1);            // selecionando coluna 2 e linha 1
  lcd.print("uma peca?");       // Print da mensagem
  delay(200);                    // atraso de 1 segundo  
}

void lcdShowRemovaPeca(){
  lcd.clear();
  lcd.setCursor(1, 0);            // selecionando coluna 0 e linha 0
  lcd.print("Remova a peca");   // print da mensagem
  lcd.setCursor(2, 1);            // selecionando coluna 2 e linha 1
  lcd.print("a ser comida");       // Print da mensagem
  delay(200);                    // atraso de 1 segundo  
}

void lcdShowMovaPeca(){
  lcd.clear();
  lcd.setCursor(0, 0);            // selecionando coluna 0 e linha 0
  lcd.print("Mova a sua peca");   // print da mensagem
  lcd.setCursor(2, 1);            // selecionando coluna 2 e linha 1
  lcd.print("para a casa");       // Print da mensagem
  delay(200);                    // atraso de 1 segundo  
}

void lcdShowFacaJogada(){
  lcd.clear();
  lcd.setCursor(2, 0);            // selecionando coluna 0 e linha 0
  lcd.print("Faca a sua");   // print da mensagem
  lcd.setCursor(4, 1);            // selecionando coluna 2 e linha 1
  lcd.print("jogada");       // Print da mensagem
  delay(200);                    // atraso de 1 segundo
}

bool botaoEsperaDois(int botaoSim,int botaoNao){
  int botaosimStatus = 0;
  int botaonaoStatus = 0;
  while(1){
    botaosimStatus = digitalRead(botaoSim);
    botaonaoStatus = digitalRead(botaoNao);
    if (botaosimStatus == LOW) {
      return true;
    }
    else if(botaonaoStatus == LOW){
      return false;
    }
  }
}

void botaoEsperaSim(int botaoSim){
  int botaosimStatus = 0;
  while(1){
    botaosimStatus = digitalRead(botaoSim);
    if (botaosimStatus == LOW) {
      return;
    }
  }
}


void setup() {
  Serial.begin(9600);
  pinMode(enable1, OUTPUT);
  pinMode(enable2, OUTPUT);
  pinMode(enable3, OUTPUT);
  pinMode(enable4, OUTPUT);
  pinMode(a1, INPUT_PULLUP);
  
  lcd.init();
  lcd.backlight();
  pinMode(botaosim,INPUT_PULLUP);
  pinMode(botaonao,INPUT_PULLUP);

}

void loop() {
  lcdIniciaGame();  //inicia o jogo
  botaoEsperaSim(botaosim); //espera confirmar pra inicio

  lcdAskVaiComer(); //pergunta se vai comer a peça

  //if para ver qual foi a resposta se vai comer ou nao
  //se for comer, executa o dentro do if, se nao executa o else
  if(botaoEsperaDois(botaosim,botaonao)){
      lcdShowRemovaPeca();  //pede para remover a peça
      botaoEsperaSim(botaosim); //espera usuario sinalizar que removeu
      lcdShowMovaPeca();        //mostra para ele mover a peça
      botaoEsperaSim(botaosim); //espera usuario sinalizar que moveu
      lertabuleiro_humano();    //lê o tabuleiro (função q tava funcionando)
      qualmovimento();          //identifica qual o movimento feito
      Serial.print(mov[0]);     //imprime no serial a string do movimento ex: b2c4
      Serial.print(mov[1]);
      Serial.print(mov[2]);
      Serial.print(mov[3]);
      Serial.println();
      
    }
    else{  //caso não va comer peça
      lcdShowFacaJogada();        //mostra para usuário fazer a jogada
      botaoEsperaSim(botaosim);   //espera usuario responder
      lertabuleiro_humano();      //le o tabuleiro 
      qualmovimento();            //identifica qual o movimento
      Serial.print(mov[0]);       //imprime no serial a string do movimento
      Serial.print(mov[1]);
      Serial.print(mov[2]);
      Serial.print(mov[3]);
      Serial.println();
      }

  //COMENTEI AS COISAS ABAIXO PARA CASO PRECISAMOS VOLTAR E ANALISAR ALGO, DEPOIS LIMPAMOS QUANDO ESTIVER TUDO OK
  //lertabuleiro_humano();
  
  //qualmovimento();
   //for(int x =0;x<8;x++){
    //for(int y = 0;y<8;y++){
      //Serial.print(leitura_atual[x][y]);
    //}
    //Serial.println();
  //}
  //Serial.print(mov[0]);
  //Serial.print(mov[1]);
  //Serial.print(mov[2]);
  //Serial.print(mov[3]);
  //Serial.println();
}
