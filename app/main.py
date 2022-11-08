from flask import Flask
from flask_restx import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

FUNCIONARIOS = [{'cpf': 1, 'nome': 'Ana', 'horas-trabalhadas': 8.0, 'valor': 45.78},
{'cpf': 2, 'nome': 'Bruna', 'horas-trabalhadas': 2.0, 'valor': 60.00},
{'cpf': 3, 'nome': 'Carlos', 'horas-trabalhadas': 10.0, 'valor': 38.99},
{'cpf': 4, 'nome': 'Diogo', 'horas-trabalhadas': 4.0, 'valor': 45.78},
{'cpf': 5, 'nome': 'Esther', 'horas-trabalhadas': 5.0, 'valor': 45.78}]

def aborta_se_o_funcionario_nao_existe(cpf):

    encontrei = False
    for funcionario in FUNCIONARIOS:
        if funcionario['cpf'] == int(cpf):
            encontrei = True
    if encontrei == False:
        abort(404, mensagem="O produto com cpf = {} não existe".format(cpf)) #404:Not Found


# Parse dos dados enviados na requisição no formato JSON:
parser = reqparse.RequestParser()
parser.add_argument('cpf', type=int, help='identificador do funcionario')
parser.add_argument('nome', type=str, help='nome do funcionario')
parser.add_argument('horas-trabalhadas', type=float, help='horas trabalhadas')
parser.add_argument('valor', type=float, help='valor da hora')
# Produto:
# 1) Apresenta um único produto.
# 2) Remove um único produto.
# 3) Atualiza (substitui) um produto.


class Funcionario(Resource):
    def get(self, cpf):
        aborta_se_o_funcionario_nao_existe(cpf)
        return FUNCIONARIOS[int(cpf)]
    def delete(self, cpf):
        aborta_se_o_funcionario_nao_existe(cpf)
        del FUNCIONARIOS[int(cpf)]
        return '', 204, #204: No Content
    def put(self, cpf):
        aborta_se_o_funcionario_nao_existe(cpf)
        args = parser.parse_args()
        for funcionario in FUNCIONARIOS:
            if funcionario['cpf'] == int(cpf):
                funcionario['cpf'] = args['cpf']
                funcionario['nome'] = args['nome']
                funcionario['horas-trabalhadas'] = args['horas-trabalhadas']
                funcionario['valor'] = args['valor']
                break
        return funcionario, 200, #200: OK
class Pagamento(Resource):
    def get(self, cpf):
        aborta_se_o_funcionario_nao_existe(cpf)
        return FUNCIONARIOS[int(cpf)]

# ListaProduto:
# 1) Apresenta a lista de produtos.
# 2) Insere um novo produto.
class ListaFuncionario(Resource):
    def get(self):
        return FUNCIONARIOS

    def post(self):
        args = parser.parse_args()
        cpf = -1
        for funcionario in FUNCIONARIOS:
            if int(funcionario['cpf']) > cpf:
                cpf = int(funcionario['cpf'])
        cpf = cpf + 1
        funcionario = {'cpf': cpf, 'nome': args['nome'], 'horas-trabalhadas':args['horas-trabalhadas'], 'valor': args['valor']}
        FUNCIONARIOS.append(funcionario)
        return funcionario, 201, #201: Created
##
## Roteamento de recursos:
##
api.add_resource(Funcionario, '/funcionarios/<cpf>')
api.add_resource(ListaFuncionario, '/funcionarios')

if __name__ == '__main__':
    app.run(debug=True)