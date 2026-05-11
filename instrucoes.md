# Instruções para Apresentação ao Vivo - Smart Gym

Este guia rápido foi criado para ajudar na demonstração do projeto Smart Gym durante a apresentação do CP2.

## Pré-requisitos
1. **Arduino conectado:** Certifique-se de que o Arduino está conectado e rodando o código `Aula_6_RFID.ino`.
2. **Ambiente Python:** Verifique se as dependências do Python estão instaladas (`cv2`, `mediapipe`, `serial`, `sqlite3`, etc.).
3. **Câmera:** Confirme se a webcam do computador/notebook está habilitada.
4. **Tags RFID:** Tenha em mãos as tags RFID que serão utilizadas na demonstração.

## Roteiro da Demonstração

### Passo 1: Preparação Inicial
1. Certifique-se de que o banco de dados inicial já foi criado. Se houver dúvidas, execute o `setup_db.py` uma vez antes da apresentação.
2. Inicie o sistema principal executando:
   ```bash
   python Aula_6.py
   ```
3. A interface gráfica (Tkinter) deve abrir mostrando a câmera e o status "Aguardando Login".

### Passo 2: Demonstração de um Aluno Cadastrado
1. Aproxime uma tag RFID que **já está cadastrada** no banco de dados (ex: a tag simulada do Lucas ou Maria) do leitor RFID conectado ao Arduino.
2. A tela do Tkinter deve atualizar automaticamente:
   - O status mudará para "Pronta para Uso / Treino Ativo" (verde).
   - A mensagem de boas-vindas exibirá o nome e o exercício do aluno.
3. Demonstre a captura dos movimentos pela câmera, mostrando o gráfico em tempo real e o contador de repetições funcionando.

### Passo 3: Demonstração do Modo Convidado
1. Aguarde o sistema voltar para o status "Aguardando Login" (ou feche e abra novamente).
2. Sem aproximar nenhuma tag, pressione a tecla **`S`** no teclado.
3. A interface mudará para o modo "Convidado", permitindo o treino sem identificação prévia.

### Passo 4: Registro "Ao Vivo" de uma Nova Tag (O Diferencial!)
*Este passo é ideal para engajar os avaliadores, cadastrando uma tag deles ou uma tag nova na hora.*

1. Com o sistema principal rodando (ou com o Monitor Serial do Arduino aberto), aproxime uma **nova tag RFID** que ainda não está cadastrada.
2. Anote ou copie o **UID** dessa nova tag (ele aparecerá no terminal do Python ou no Monitor Serial do Arduino).
3. Sem precisar fechar o sistema principal, execute o script em lote:
   - Dê um clique duplo em **`register_live.bat`** (no Windows).
4. O prompt de comando abrirá. Preencha os dados:
   - **UID:** (Insira o UID copiado, ex: `1A 2B 3C 4D`)
   - **Nome:** (Insira o nome do avaliador ou um nome fictício)
   - **Exercício:** (Ex: Rosca Direta)
   - **Repetições:** (Ex: 5)
5. O terminal exibirá `[SUCESSO]`. Pode pressionar Enter para fechar o terminal.
6. Agora, volte para a interface do Tkinter e **aproxime a mesma nova tag novamente**.
7. *Magia!* O sistema agora reconhecerá a tag imediatamente, buscando no banco de dados atualizado, e iniciará o treino personalizado para a pessoa recém-cadastrada.

## Dicas Adicionais
- O script `register_live.bat` também atualiza tags existentes. Se você digitar o UID de um aluno que já existe e mudar o nome ou as repetições, o banco será atualizado.
- O campo de `ultimo_acesso` no banco de dados é atualizado automaticamente a cada login bem-sucedido, cumprindo perfeitamente os requisitos do CP2.
