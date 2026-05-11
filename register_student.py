import sqlite3
import sys

def register(uid, nome, exercicio, repeticoes):
    conn = sqlite3.connect('smart_gym.db')
    cursor = conn.cursor()
    
    # Verifica se o UID já existe
    cursor.execute("SELECT id FROM alunos WHERE uid = ?", (uid,))
    result = cursor.fetchone()
    
    if result:
        cursor.execute('''
            UPDATE alunos 
            SET nome = ?, exercicio = ?, repeticoes = ?
            WHERE uid = ?
        ''', (nome, exercicio, repeticoes, uid))
        print(f"\n[SUCESSO] Cartao RFID '{uid}' atualizado para o aluno '{nome}'.")
    else:
        cursor.execute('''
            INSERT INTO alunos (uid, nome, exercicio, repeticoes)
            VALUES (?, ?, ?, ?)
        ''', (uid, nome, exercicio, repeticoes))
        print(f"\n[SUCESSO] Novo cartao RFID '{uid}' registrado para o aluno '{nome}'.")
        
    conn.commit()
    conn.close()

if __name__ == '__main__':
    if len(sys.argv) == 5:
        # Pega os argumentos e remove espaços extras
        uid_arg = sys.argv[1].strip().upper()
        nome_arg = sys.argv[2].strip()
        exercicio_arg = sys.argv[3].strip()
        try:
            reps_arg = int(sys.argv[4].strip())
            register(uid_arg, nome_arg, exercicio_arg, reps_arg)
        except ValueError:
            print("\n[ERRO] O numero de repeticoes deve ser um numero inteiro valido.")
    else:
        print("\n[ERRO] Argumentos invalidos.")
        print("Uso correto: python register_student.py <UID> <Nome> <Exercicio> <Repeticoes>")
