from flask import Flask, render_template, request, redirect, url_for, make_response
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from waitress import serve
import sqlite3
from datetime import datetime

app = Flask(__name__)

caminho_csv = "./convidados_2.csv"

# Lista para armazenar os convidados
convidados = []

# Abrir o arquivo CSV e ler os dados
with open(caminho_csv, newline='', encoding='utf-8') as arquivo_csv:
    leitor_csv = csv.DictReader(arquivo_csv, delimiter=';')
    for linha in leitor_csv:
        # Converter os dados para o formato desejado
        convidado = {
            "id": int(linha["Ord"]),
            "nome": linha["Nome"],
            "tipo": linha["tipo"],
            "confirmado": False  # Por padrão, nenhum convidado está confirmado
        }
        # Adicionar o convidado à lista de convidados
        convidados.append(convidado)

print("rodando em: http://localhost:8080")

# Rota principal para exibir o menu de seleção de convidados
@app.route("/", methods=["GET", "POST"])
def menu_convidados():
    if request.method == "POST":
        convidado_id = int(request.form["convidado"])

        for convidado in convidados:
            if convidado["id"] == convidado_id:
                convidado["confirmado"] = True
        return render_template("confirmacao.html", convidados=convidados)
    return render_template("menu.html", convidados=convidados)

    #fazer uma requisição pro banco de dados retornar todos os eventos da tabela eventos
@app.route("/evento_novo", methods=["GET", "POST"])
def evento_novo():
    if request.method == "POST":
        evento_nome = request.form["nome"]
        evento_data = request.form["data"]

        # Connect to the SQLite database
        conn = sqlite3.connect("convidados.db")
        cursor = conn.cursor()

        # Insert the new event into the "eventos" table
        try:
            cursor.execute("INSERT INTO eventos (nome, data) VALUES (?, ?)", (evento_nome, evento_data))
            # Commit changes to the database
            conn.commit()
            print("Event inserted successfully!")
        except sqlite3.Error as e:
            print("Error inserting event:", e)
        finally:
            # Close the database connection
            conn.close()
        return redirect(url_for("listar_eventos"))
    return render_template("evento_novo.html")

@app.route("/eventos", methods=["GET"])
def listar_eventos():

    conn = sqlite3.connect("convidados.db")
    cursor = conn.cursor()

    try:
        # Query the database for all events
        cursor.execute("SELECT * FROM eventos")
        eventos = cursor.fetchall()
        #eventos_formatted = [(evento[0], evento[1], datetime.strptime(evento[2], "%Y-%m-%d").strftime("%d/%m/%Y")) for evento in eventos]
        print("Eventos:", eventos)
    except sqlite3.Error as e:
        print("Error querying events:", e)

    # Close the database connection
    conn.close()

    return render_template("listar_eventos.html", eventos=eventos) 

@app.route("/detalhes/<int:evento_id>", methods=["GET"])
def detalhes_evento(evento_id):

    conn = sqlite3.connect("convidados.db")
    cursor = conn.cursor()

    try:
        # Query the database for the event with the specified ID
        cursor.execute("SELECT * FROM eventos WHERE id = ?", (evento_id,))
        evento = cursor.fetchone()
        print("Evento:", evento)
    except sqlite3.Error as e:
        print("Error querying event:", e)

    # Close the database connection
    conn.close()

    return render_template("detalhes_evento.html", evento=evento)

def menu_convidados():
    if request.method == "POST":
        convidado_id = int(request.form["convidado"])

        for convidado in convidados:
            if convidado["id"] == convidado_id:
                convidado["confirmado"] = True
        return render_template("confirmacao.html", convidados=convidados)
    return render_template("detalhes_evento.html", convidados=convidados)

@app.route("/detalhes/<int:evento_id>/lista_presenca", methods=["GET", "POST"])
def lista_presenca(evento_id):

    conn = sqlite3.connect("convidados.db")
    cursor = conn.cursor()

    try:
        # Query the database for the event with the specified ID
        cursor.execute("SELECT * FROM eventos WHERE id = ?", (evento_id,))
        evento = cursor.fetchone()
        print("Evento:", evento)

        # Query the database for all guests invited to the event
        cursor.execute("SELECT * FROM convidados WHERE evento_id = ?", (evento_id,))
        convidados = cursor.fetchall()
        print("Convidados:", convidados)
    except sqlite3.Error as e:
        print("Error querying event and guests:", e)

    # Close the database connection
    conn.close()

    if request.method == "POST":
        convidado_id = int(request.form["convidado"])

        conn = sqlite3.connect("convidados.db")
        cursor = conn.cursor()

        try:
            # Update the guest's attendance status
            cursor.execute("UPDATE convidados SET confirmado = 1 WHERE id = ?", (convidado_id,))
            # Commit changes to the database
            conn.commit()
            print("Guest attendance confirmed successfully!")
        except sqlite3.Error as e:
            print("Error confirming guest attendance:", e)

        # Close the database connection
        conn.close()

        return redirect(url_for("lista_presenca", evento_id=evento_id))

    return render_template("lista_presenca.html", evento=evento)

@app.route("/eventos/delete/<int:evento_id>", methods=["GET"])
def deletar_evento(evento_id):

    conn = sqlite3.connect("convidados.db")
    cursor = conn.cursor()

    try:
        # Delete the event with the specified ID
        cursor.execute("DELETE FROM eventos WHERE id = ?", (evento_id,))
        # Commit changes to the database
        conn.commit()
        print("Event deleted successfully!")
    except sqlite3.Error as e:
        print("Error deleting event:", e)

    # Close the database connection
    conn.close()

    return redirect(url_for("listar_eventos"))

@app.route("/oficiais_generais", methods=["GET", "POST"])
def oficiais_generais():
    if request.method == "POST":
        convidado_id = int(request.form["convidado"])

        for convidado in convidados:
            if convidado["id"] == convidado_id:
                convidado["confirmado"] = True
        return render_template("confirmacao.html", convidados=convidados)
    return render_template("oficiais_generais.html", convidados=convidados)

@app.route("/comandantes_om", methods=["GET", "POST"])
def comandantes_om():
    if request.method == "POST":
        convidado_id = int(request.form["convidado"])

        for convidado in convidados:
            if convidado["id"] == convidado_id:
                convidado["confirmado"] = True
        return render_template("confirmacao.html", convidados=convidados)
    return render_template("comandantes_om.html", convidados=convidados)

@app.route("/convidados_militares", methods=["GET", "POST"])
def convidados_militares():
    if request.method == "POST":
        convidado_id = int(request.form["convidado"])

        for convidado in convidados:
            if convidado["id"] == convidado_id:
                convidado["confirmado"] = True
        return render_template("confirmacao.html", convidados=convidados)
    return render_template("convidados_militares.html", convidados=convidados)

@app.route("/civil", methods=["GET", "POST"])
def civil():
    if request.method == "POST":
        convidado_id = int(request.form["convidado"])

        for convidado in convidados:
            if convidado["id"] == convidado_id:
                convidado["confirmado"] = True
        return render_template("confirmacao.html", convidados=convidados)
    return render_template("civil.html", convidados=convidados)

# Rota para exibir os convidados com presença confirmada
@app.route("/presenca")
def presenca():
    convidados_confirmados = [convidado for convidado in convidados if convidado["confirmado"]]
    convidados_confirmados.sort(key=lambda x: x["id"])
    return render_template("presenca.html", convidados=convidados_confirmados)

@app.route("/add", methods=["GET", "POST"])
def adicionar_convidado():
    if request.method == "POST":
        nome = request.form["nome"].upper()
        # Gere um ID único para o novo convidado
        novo_id = len(convidados) + 1
        novo_convidado = {"id": novo_id, "nome": nome, "tipo":'OUTROS', "confirmado": True}
        # Adicione o novo convidado à lista de presença
        convidados.append(novo_convidado)
        return render_template("confirmacao.html", convidados=convidados)
    return render_template("add.html")

@app.route("/presenca/limpar", methods=["GET"])
def limpar_presenca():
    for convidado in convidados:
        convidado["confirmado"] = False
    return redirect(url_for("presenca"))

@app.route("/presenca/desconfirmar/<int:convidado_id>", methods=["GET"])
def deletar_convidado(convidado_id):
    for i, convidado in enumerate(convidados):
        if convidado["id"] == convidado_id:
            # alterar o valor de confirmado para False
            convidados[i]["confirmado"] = False
            print("Convidado desconfirmado:", convidado["nome"])
            break
    return redirect(url_for("presenca"))


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
