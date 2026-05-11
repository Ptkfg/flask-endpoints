from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Lista para armazenar registros temporariamente
Registros = []

# Função para conectar ao banco
def get_db_connection():
    conn = sqlite3.connect("foco.db")
    conn.row_factory = sqlite3.Row
    return conn

def conectar_banco():
    conn = sqlite3.connect("foco_produtividade.db")
    return conn

# Cria a tabela 
def criar_tabela():
    conn = conectar_banco()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            duracao_minutos INTEGER NOT NULL,
            interrupcoes INTEGER NOT NULL,
            humor TEXT
        )
    """)
    conn.commit()
    conn.close()

criar_tabela()


@app.route("/Registro", methods=['POST'])
def registro_sessao():
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'Registro invalido'})
    
    Registros.append(dados)
    return jsonify({'mensagem': 'Registrado com sucesso', 'total_registros': len(Registros)})

@app.route("/diagnostico", methods=["GET"])
def diagnostico():
    if not Registros:
        return jsonify({"mensagem": "Nenhum registro encontrado."})
    
    duracoes = [r.get("duracao_minutos", 0) for r in Registros]
    interrupcoes = [r.get("interrupcoes", 0) for r in Registros]
    
    media_duracao = sum(duracoes) / len(duracoes)
    media_interrupcoes = sum(interrupcoes) / len(interrupcoes)
    
    insight = "Você está mantendo boas sessões de foco!" if media_duracao > 25 else "Tente aumentar o tempo médio de foco."
    
    return jsonify({
        "total_sessoes": len(Registros),
        "media_duracao_minutos": round(media_duracao, 2),
        "media_interrupcoes": round(media_interrupcoes, 2),
        "insight": insight
    })

if __name__ == "__main__":
    app.run(debug=True)