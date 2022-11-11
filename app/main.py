from flask import Flask
from flask_restx import reqparse, abort, Api, Resource, fields

app = Flask(__name__)
api = Api(app,
        version='1.0',
        title='API da folha de pagamento de uma Empresa',
        description='Permite gerenciar os registros dos funcionarios de uma empresa',
        doc='/doc')

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
        abort(404, mensagem="O funcionario com cpf = {} não existe".format(cpf)) #404:Not Found

# Parse dos dados enviados na requisição no formato JSON:
parser = reqparse.RequestParser()
parser.add_argument('cpf', type=int, help='identificador do funcionario')
parser.add_argument('nome', type=str, help='nome do funcionario')
parser.add_argument('horas-trabalhadas', type=float, help='horas trabalhadas')
parser.add_argument('valor', type=float, help='valor da hora')


campos_obrigatorios_para_atualizacao = api.model('Atualizaçao de Funcionario', {
    'cpf': fields.Integer(required=True, description='cpf do funcionario'),
    'nome': fields.String(required=True, description='nome do funcionario'),
    'horas-trabalhadas': fields.Integer(required=True, description='quantidade de horas trabalhadas'),
    'valor': fields.Float(required=True, description='valor da hora'),
})

campos_obrigatorios_para_atualizacao_parcial = api.model('Atualizaçao de Funcionario', {
    'valor': fields.Float(required=True, description='valor da hora')
})

campos_obrigatorios_para_insercao = api.model('Inserção de Funcionario', {
    'cpf': fields.Integer(required=True, description='cpf do funcionario'),
    'nome': fields.String(required=True, description='nome do funcionario'),
    'horas-trabalhadas': fields.Integer(required=True, description='quantidade de horas trabalhadas'),
    'valor': fields.Float(required=True, description='valor da hora'),
})



# Produto:
# 1) Apresenta um único produto.
# 2) Remove um único produto.
# 3) Atualiza (substitui) um produto.


@api.route('/funcionarios/<cpf>')
@api.doc(params={'cpf': 'cpf do funcionario'})
class Funcionario(Resource):
    @api.doc(responses={200: 'funcionario retornado'})
    def get(self, cpf):
        aborta_se_o_funcionario_nao_existe(cpf)
        return FUNCIONARIOS[int(cpf)]

    @api.doc(responses={204: 'funcionario removido'}) #204: No Content
    def delete(self, cpf):
        aborta_se_o_funcionario_nao_existe(cpf)
        del FUNCIONARIOS[int(cpf)]
        return '', 204


    @api.doc(responses={200: 'funcionario substituído'}) #200: OK
    @api.expect(campos_obrigatorios_para_atualizacao)
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
            return funcionario

    @api.doc(responses={200: 'produto substituído'})  # 200: OK
    @api.expect(campos_obrigatorios_para_atualizacao_parcial)
    def patch(self, cpf):
        aborta_se_o_funcionario_nao_existe(cpf)
        args = parser.parse_args()
        for funcionario in FUNCIONARIOS:
            if funcionario['cpf'] == int(cpf):
                funcionario['valor'] = args['valor']
                break
        return funcionario  # 200: OK

# ListaProduto:
# 1) Apresenta a lista de produtos.
# 2) Insere um novo produto.

@api.route('/funcionarios') 
class ListaFuncionario(Resource):
    @api.doc(responses={200: 'produtos retornados'})
    def get(self):
        return FUNCIONARIOS

    @api.doc(responses={201: 'funcionario inserido'}) #201: Created
    @api.expect(campos_obrigatorios_para_insercao)
    def post(self):
        args = parser.parse_args()
        cpf = -1
        for funcionario in FUNCIONARIOS:
            if int(funcionario['cpf']) > cpf:
                id = int(funcionario['cpf'])
        cpf = cpf + 1
        produto = {'cpf': cpf, 'nome': args['nome'], 'horas-trabalhadas': args['horas-trabalhadas'], 'valor': args['valor']}
        FUNCIONARIOS.append(produto)
        return funcionario, 201

@api.route('/quantidades')
class QuantidadeTotal(Resource):
    def get(self):
        total = 0 
        for funcionario in FUNCIONARIOS:
            total = total + funcionario['horas-trabalhadas']*funcionario['valor']
        return total

@api.route('/horas/<cpf>')
class ValorFuncionario(Resource):
    def get(self, cpf):
        for funcionario in FUNCIONARIOS:
            if funcionario['cpf'] == int(cpf):
                return funcionario['horas-trabalhadas']

@api.route('/folha')
class Estoque(Resource):
    def get(self):
        for funcionario in FUNCIONARIOS:
            menor = funcionario['horas-trabalhadas']*funcionario['valor']
            maior = funcionario['horas-trabalhadas']*funcionario['valor']
            if funcionario['horas-trabalhadas']*funcionario['valor'] < menor:
                menor = funcionario['horas-trabalhadas']*funcionario['valor']
            if funcionario['horas-trabalhadas']*funcionario['valor'] < maior:
                maior = funcionario['horas-trabalhadas']*funcionario['valor']
        dados_estoque = {
            "Maior valor" : maior,
            "Menor valor" : menor
        }
        return dados_estoque

@api.route('/total/folha')
class ValorTotalEstoque(Resource):
    def get(self):
        total = 0
        for funcionario in FUNCIONARIOS:
            total = total + funcionario["quantidade"]*funcionario["preco"]
        return total

if __name__ == '__main__':
    app.run(debug=True)