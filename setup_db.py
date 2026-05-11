import sqlite3
import datetime

def setup_db():
    conn = sqlite3.connect('smart_gym.db')
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid TEXT UNIQUE NOT NULL,
        nome TEXT NOT NULL,
        exercicio TEXT NOT NULL,
        repeticoes INTEGER NOT NULL,
        ultimo_acesso DATETIME
    )
    ''')
    
    # Insert initial data
    alunos = [
        ("4A B9 3B 1B", "Lucas", "Rosca Direta", 5),
        ("B3 22 A1 0C", "Maria", "Rosca Direta", 8),
        ("BD:84:7A:59", "Ronaldo", "Triceps", 10),
        ("D6:EE:4C:1F", "Messi", "Triceps", 10),
    ]
    
    cursor.executemany('''
    INSERT OR IGNORE INTO alunos (uid, nome, exercicio, repeticoes)
    VALUES (?, ?, ?, ?)
    ''', alunos)
    
    conn.commit()
    conn.close()
    print("Database configurado com sucesso!")

if __name__ == '__main__':
    setup_db()
