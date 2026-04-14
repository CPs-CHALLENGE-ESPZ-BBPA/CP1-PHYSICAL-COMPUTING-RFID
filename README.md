#  O Caso da Smart Gym: A Evolução do Treino Digital
 
Este projeto visa o desenvolvimento de um ecossistema de **Smart Stations** (Estações Inteligentes) projetado para replicar a atenção de um personal trainer presencial. O sistema garante que o aluno execute os exercícios com a técnica perfeita através do monitoramento de postura e desempenho em tempo real.
 
###  Funcionalidades
Com base nas exigências técnicas descritas no desafio oficial:
 
* **Identificação por RFID**: Sistema integrado entre Arduino UNO e Python para leitura de cartões RFID, reconhecimento do ID do aluno via porta serial e validação do acesso à estação de treino.
* **Captura Biométrica (Visão)**: Ativação automática da câmera após o login para extração das coordenadas (landmarks) das articulações do usuário em tempo real.
* **Monitoramento de Amplitude de Movimento (Postura)**: Verificação de execuções completas e controladas para evitar movimentos parciais ou desalinhados que possam gerar lesões.
* **Análise de Cadência e Fadiga (Comportamento)**: Monitoramento do ritmo de execução para identificar fadiga muscular e sugestão automática de tempos de descanso ideais (entre 60s e 90s).
* **Identificação e Contexto (Dados)**: Carregamento do perfil do atleta via RFID para garantir a personalização do treino e o acompanhamento preciso da evolução.
 
---
 
###  Equipe (Turma 3ESPZ)
* **Albert Katri** - RM556544
* **Bruno Leão** - RM555563
* **Bruno Biletsky** - RM554739
* **Paulo Akira** - RM556840
 
---
 
###  Componentes e Bibliotecas
 
#### 1. Hardware e Protocolos
* **Microcontrolador**: Arduino UNO.
* **Módulo de Identificação**: Leitor RFID-RC522.
* **Protocolo de Comunicação**: SPI (Serial Peripheral Interface).
* **Entrada de Vídeo**: Webcam para captura em tempo real.
 
#### 2. Bibliotecas Python Utilizadas
O projeto utiliza as seguintes dependências conforme importadas no código-fonte:
* `cv2` (OpenCV): Captura e processamento de frames de vídeo.
* `time`: Controle de cadência e cronometragem de intervalos.
* `mediapipe` (mp): Framework para rastreamento de pose e extração de landmarks.
* `numpy` (np): Operações matriciais e cálculos biomecânicos.
* `serial` (pySerial): Gestão da comunicação serial com o hardware.
* `matplotlib.pyplot` (plt): Geração de gráficos de desempenho.
* `FigureCanvasAgg` (FigureCanvas): Integração dos gráficos na interface de vídeo.
* `mediapipe.tasks.python`: Configuração de tarefas do MediaPipe.
* `mediapipe.tasks.python.vision`: APIs otimizadas para visão computacional.
 
**Arduino:**
* `MFRC522.h`: Biblioteca para interface com o módulo RFID via barramento SPI.
 
---
 
###  Acesso ao Projeto (Link e Imagem)

 * **Link do vídeo:** https://youtu.be/mSKdgU0WgsM
* **Link do Projeto (Wokwi):** https://wokwi.com/projects/461234007381623809
* **Imagem do Projeto:** 
<img width="757" height="478" alt="image" src="https://github.com/user-attachments/assets/b456a016-a585-49e9-9d86-d132829ae1ec" />

 
---
 
###  Diagrama de Conexões
O sistema integra o leitor RFID ao **Arduino UNO** utilizando a interface **SPI**. As conexões seguem o padrão de pinagem do UNO:
* **SDA (SS)**: Pino 10
* **SCK**: Pino 13
* **MOSI**: Pino 11
* **MISO**: Pino 12
* **RST**: Pino 9
* **3.3V**: 3.3V
* **GND**: GND
 
---
 
###  Instruções de Setup e Execução
 
1. **Configuração do Hardware**: Realize a montagem conforme o diagrama esquemático e conecte o Arduino UNO ao computador via USB.
2. **Firmware Arduino**: Carregue o código (.ino) para o UNO utilizando a IDE Arduino (certifique-se de que a biblioteca MFRC522 está instalada).
3. **Instalação das Dependências Python**:
   ```bash
   pip install opencv-python mediapipe numpy pyserial matplotlib
