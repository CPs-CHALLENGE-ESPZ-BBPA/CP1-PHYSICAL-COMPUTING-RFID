import cv2
import time
import mediapipe as mp
import numpy as np
import serial
import sqlite3
import datetime
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class SmartGymApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        # --- UI Setup ---
        self.main_frame = ttk.Frame(window, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Painel Visual - Status
        self.status_var = tk.StringVar()
        self.status_var.set("Status: Aguardando Login")
        self.status_label = ttk.Label(self.main_frame, textvariable=self.status_var, font=("Helvetica", 16, "bold"), foreground="blue")
        self.status_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Painel Visual - Boas Vindas
        self.welcome_var = tk.StringVar()
        self.welcome_var.set("Aproxime o cartão RFID ou aperte 'S' (Convidado)")
        self.welcome_label = ttk.Label(self.main_frame, textvariable=self.welcome_var, font=("Helvetica", 14))
        self.welcome_label.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Painel Visual - Contador de Exercícios
        self.reps_var = tk.StringVar()
        self.reps_var.set("Repetições: 0 / 0")
        self.reps_label = ttk.Label(self.main_frame, textvariable=self.reps_var, font=("Helvetica", 14, "bold"), foreground="green")
        self.reps_label.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Canvas de Vídeo + Gráfico
        self.video_canvas = tk.Canvas(self.main_frame, width=640, height=480+200)
        self.video_canvas.grid(row=3, column=0, columnspan=2, pady=10)
        
        # --- Configurações Iniciais ---
        self.arduino_conectado = False
        try:
            # Lembre-se de conferir a porta COM no Gerenciador de Dispositivos / ls /dev/tty*
            self.ser = serial.Serial('COM5', 9600, timeout=0.1) # Tenta a porta original
            self.arduino_conectado = True
            print("Arduino ON - Sistema de Identificacao Pronto na porta COM5!")
        except Exception as e:
            try:
                self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.1) # Tenta porta Linux
                self.arduino_conectado = True
                print("Arduino ON - Sistema de Identificacao Pronto na porta /dev/ttyUSB0!")
            except:
                print("Arduino OFF - Apenas modo Convidado disponivel (Tecla 'S')")
            
        # Atalhos
        self.window.bind('s', self.login_convidado)
        self.window.bind('q', lambda e: self.window.destroy())
        
        # MediaPipe Setup
        model_path = 'pose_landmarker_full.task'
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO
        )
        self.detector = vision.PoseLandmarker.create_from_options(options)
        
        # Gráfico Setup
        self.fig = plt.figure(figsize=(6.4, 2.0), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('black')
        self.fig.set_facecolor('black')
        self.canvas = FigureCanvas(self.fig)
        
        # Variáveis de Estado
        self.estado_app = "AGUARDANDO_ID"
        self.perfil_ativo = None
        self.contador_reps = 0
        self.estagio_exercicio = ""
        self.historico_angulo = []
        
        # Video Capture
        self.cap = cv2.VideoCapture(0)
        
        # Loop do Tkinter
        self.delay = 15
        self.update()

    def conectar_db(self):
        # Ensure 'smart_gym.db' is in the exact same directory as the script.
        return sqlite3.connect('smart_gym.db')

    def validar_rfid(self, uid):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            
            # Fetching id, nome, exercicio, and repeticoes from the 'alunos' table
            cursor.execute("SELECT id, nome, exercicio, repeticoes FROM alunos WHERE uid = ?", (uid,))
            aluno = cursor.fetchone()
            
            if aluno:
                # Registro automático do horário de acesso no campo 'ultimo_acesso'
                agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("UPDATE alunos SET ultimo_acesso = ? WHERE id = ?", (agora, aluno[0]))
                conn.commit()
                conn.close()
                
                # aluno[1] = nome, aluno[2] = exercicio, aluno[3] = repeticoes (objetivo)
                return {"nome": aluno[1], "exercicio": aluno[2], "objetivo": aluno[3]}
            else:
                conn.close()
                return None
        except Exception as e:
            print(f"Erro no banco de dados: {e}")
            return None

    def login_convidado(self, event=None):
        if self.estado_app == "AGUARDANDO_ID":
            print("Iniciando como Aluno Convidado.")
            self.perfil_ativo = {"nome": "Convidado", "exercicio": "Rosca Direta", "objetivo": 3}
            self.iniciar_treino()

    def iniciar_treino(self):
        self.historico_angulo = []
        self.contador_reps = 0
        self.estado_app = "TREINO_EM_CURSO"
        
        # Atualiza Painel Visual Tkinter
        self.status_var.set("Status: Pronta para Uso / Treino Ativo")
        self.status_label.config(foreground="green")
        self.welcome_var.set(f"Bem-vindo(a), {self.perfil_ativo['nome']}! Exercício: {self.perfil_ativo['exercicio']}")
        self.reps_var.set(f"Repetições: {self.contador_reps} / {self.perfil_ativo['objetivo']}")

    def calcular_angulo(self, a, b, c):
        a, b, c = np.array(a), np.array(b), np.array(c)
        radianos = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angulo = np.abs(radianos * 180.0 / np.pi)
        if angulo > 180.0: angulo = 360 - angulo
        return angulo

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            
            # --- SISTEMA DE ENTRADA HÍBRIDO ---
            if self.estado_app == "AGUARDANDO_ID":
                # 1. Checa RFID (Arduino)
                if self.arduino_conectado and self.ser.in_waiting > 0:
                    id_lido = self.ser.readline().decode('utf-8').strip()
                    
                    # NOVA VALIDAÇÃO: Garante que a string recebida tem tamanho de um UID (ex: 7A:24:88:19)
                    # Isso evita que linhas em branco ou ruídos causem consultas vazias no banco de dados.
                    if len(id_lido) >= 11:
                        aluno = self.validar_rfid(id_lido)
                        if aluno:
                            print(f"Aluno Identificado: {aluno['nome']}")
                            self.perfil_ativo = aluno
                            self.iniciar_treino()
                        else:
                            print(f"ID {id_lido} nao cadastrado no banco de dados.")
                
            elif self.estado_app == "TREINO_EM_CURSO":
                # IA e Processamento MediaPipe
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
                resultado = self.detector.detect_for_video(mp_image, int(time.time() * 1000))
                
                if resultado.pose_landmarks:
                    marcos = resultado.pose_landmarks[0]
                    # Ombro(11), Cotovelo(13), Pulso(15)
                    ombro = [int(marcos[11].x * w), int(marcos[11].y * h)]
                    cotovelo = [int(marcos[13].x * w), int(marcos[13].y * h)]
                    pulso = [int(marcos[15].x * w), int(marcos[15].y * h)]
                    
                    angulo = self.calcular_angulo(ombro, cotovelo, pulso)
                    texto_angulo = f"{int(angulo)} graus"
                    
                    cv2.putText(frame, texto_angulo,
                                (cotovelo[0] + 30, cotovelo[1]),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                (255, 255, 255), 2)
                                
                    self.historico_angulo.append(angulo)
                    if len(self.historico_angulo) > 50: self.historico_angulo.pop(0)
                    
                    # Desenho do esqueleto
                    cv2.line(frame, tuple(ombro), tuple(cotovelo), (255, 255, 255), 2)
                    cv2.line(frame, tuple(cotovelo), tuple(pulso), (255, 255, 255), 2)
                    for p in [ombro, cotovelo, pulso]: cv2.circle(frame, tuple(p), 8, (0, 0, 255), -1)
                    
                    # Contagem de Repetições
                    if angulo > 50: self.estagio_exercicio = "descida"
                    if angulo < 35 and self.estagio_exercicio == "descida":
                        self.estagio_exercicio = "subida"
                        self.contador_reps += 1
                        
                        # Atualiza UI do Contador
                        self.reps_var.set(f"Repetições: {self.contador_reps} / {self.perfil_ativo['objetivo']}")
                    
                    # Verifica conclusão
                    if self.contador_reps >= self.perfil_ativo['objetivo']:
                        self.estado_app = "TREINO_CONCLUIDO"
                        self.status_var.set("Status: Treino Concluído!")
                        self.status_label.config(foreground="blue")
                        self.window.after(3000, self.resetar_para_espera) # Retorna após 3 seg

            # Renderização do Gráfico no Frame
            if self.estado_app in ["TREINO_EM_CURSO", "TREINO_CONCLUIDO"]:
                self.ax.clear()
                self.ax.plot(self.historico_angulo, color='#00FFFF', linewidth=2)
                self.ax.set_ylim(0, 180)
                self.ax.set_title("ANGULO EM TEMPO REAL", color='white', fontsize=10)
                self.canvas.draw()
                grafico_img = cv2.cvtColor(np.asarray(self.canvas.buffer_rgba()), cv2.COLOR_RGBA2BGR)
                grafico_img = cv2.resize(grafico_img, (w, 200))
                frame = np.vstack((frame, grafico_img))
            else:
                # Preenche com área preta no modo espera para manter as dimensões do Canvas consistentes
                black_area = np.zeros((200, w, 3), dtype=np.uint8)
                frame = np.vstack((frame, black_area))
            
            # Converte o Frame BGR do OpenCV para o formato compatível com o Tkinter
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_canvas.imgtk = imgtk
            self.video_canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            
        # Agenda o próximo frame
        self.window.after(self.delay, self.update)

    def resetar_para_espera(self):
        self.estado_app = "AGUARDANDO_ID"
        self.status_var.set("Status: Aguardando Login")
        self.status_label.config(foreground="blue")
        self.welcome_var.set("Aproxime o cartão RFID ou aperte 'S' (Convidado)")
        self.reps_var.set("Repetições: 0 / 0")
        self.perfil_ativo = None

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()
        if self.arduino_conectado:
            self.ser.close()

if __name__ == '__main__':
    root = tk.Tk()
    app = SmartGymApp(root, "Smart Gym - Treino Digital com Tkinter e SQLite")
    root.mainloop()