from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

produtos_lista = []

class Produto:

    def __init__(self, codigo, descricao, preco):
        self.codigo = codigo
        self.descricao = descricao
        self.preco = preco

class ProdutoDAO:

    def adicionar(self, produto):
        produtos_lista.append(produto)

    def listar(self):
        return produtos_lista
    
    def apagar(self, codigo):

     for produto in produtos_lista:

        if produto.codigo == codigo:
            produtos_lista.remove(produto)
            return True

     return False
    
    def alterar(self, codigo, descricao, preco):

     for produto in produtos_lista:

        if produto.codigo == codigo:

            produto.descricao = descricao
            produto.preco = preco

            return True

     return False

    
@app.route("/api/produtos")
def listar_produtos():

    dao = ProdutoDAO()

    lista = []

    for produto in dao.listar():
        lista.append({
            "codigo": produto.codigo,
            "descricao": produto.descricao,
            "preco": produto.preco
        })

    return jsonify(lista)

@app.route("/api/produtos", methods=["POST"])
def adicionar_produto():

    dados = request.json

    produto = Produto(
        dados["codigo"],
        dados["descricao"],
        dados["preco"]
    )

    dao = ProdutoDAO()
    dao.adicionar(produto)

    return jsonify({"mensagem": "Produto cadastrado"})

@app.route("/api/produtos/<int:codigo>", methods=["DELETE"])
def apagar_produto(codigo):

    dao = ProdutoDAO()

    if dao.apagar(codigo):
        return jsonify({"mensagem": "Produto apagado"})

    return jsonify({"erro": "Produto não encontrado"})

@app.route("/api/produtos/<int:codigo>", methods=["PUT"])
def alterar_produto(codigo):

    dados = request.json

    dao = ProdutoDAO()

    if dao.alterar(
        codigo,
        dados["descricao"],
        dados["preco"]
    ):
        return jsonify({"mensagem": "Produto alterado"})

    return jsonify({"erro": "Produto não encontrado"})

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/usuarios")
def usuarios():
    return render_template("usuarios.html")

@app.route("/produtos")
def produtos():
    return render_template("produtos.html")


app.run(debug=True)