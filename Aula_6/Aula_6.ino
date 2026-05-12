// Definição dos pinos dos botões
#define BTN_LUCAS 7
#define BTN_MARIA 6
#define BTN_RONALDO 8
#define BTN_MESSI 9

void setup() 
{
  // A velocidade deve ser 9600 para bater com o script Python
  Serial.begin(9600);
  
  // Configuração com Pull-up interno (Botão no pino e no GND)
  pinMode(BTN_LUCAS, INPUT_PULLUP);
  pinMode(BTN_MARIA, INPUT_PULLUP);
}

void loop() 
{
  // --- Lógica para o Perfil do Lucas ---
  if (digitalRead(BTN_LUCAS) == LOW) 
  {
    delay(50); // Debounce
    
    // Envia exatamente a chave que o Python espera no dicionário
    Serial.println("4A B9 3B 1B"); 
    
    // Aguarda soltar o botão para não inundar a Serial
    while(digitalRead(BTN_LUCAS) == LOW);
    delay(200);
  }

  // --- Lógica para o Perfil da Maria ---
  if (digitalRead(BTN_MARIA) == LOW) 
  {
    delay(50); // Debounce
    
    // Envia a chave correspondente à Maria no Python
    Serial.println("B3 22 A1 0C");
    
    // Aguarda soltar o botão
    while(digitalRead(BTN_MARIA) == LOW);
    delay(200);
  }

  // --- Lógica para o Perfil do RONALDO ---
  if (digitalRead(BTN_RONALDO) == LOW) 
  {
    delay(50); // Debounce
    
    // Envia a chave correspondente à Ronaldo no Python
    Serial.println("BD:84:7A:59");
    
    // Aguarda soltar o botão
    while(digitalRead(BTN_RONALDO) == LOW);
    delay(200);
  }

  // --- Lógica para o Perfil do MESSI ---
  if (digitalRead(BTN_MESSI) == LOW) 
  {
    delay(50); // Debounce
    
    // Envia a chave correspondente à Messi no Python
    Serial.println("D6:EE:4C:1F");
    
    // Aguarda soltar o botão
    while(digitalRead(BTN_MESSI) == LOW);
    delay(200);
  }
}
