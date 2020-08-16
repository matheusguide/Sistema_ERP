import matplotlib.pyplot as plt
import pymysql.cursors

conexao = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='erp',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor

)

autentico = False


def logarCadastrar():
    usuarioExistente = 0
    autenticado = False
    usuarioMaster = False

    if decisao == 1:
        nome = input('Digite seu nome: ')
        senha = input('Digite sua senha: ')

        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                if linha['nivel'] == 1:
                    usuarioMaster = False
                elif linha['nivel'] == 2:
                    usuarioMaster = True
                autenticado = True
                break
            else:
                autenticado = False
        if not autenticado:
            print('E-mail ou senha incorretos.')

    elif decisao == 2:
        print('Faça seu cadastro: ')
        nome = input('Digite um nome: ')
        senha = input('Digite uma senha: ')

        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                usuarioExistente = 1
        if usuarioExistente == 1:
            print('O usuário já está cadastrado. Tente um nome ou senha diferente.')
        elif usuarioExistente == 0:
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('insert into cadastros(nome,senha,nivel) values(%s,%s,%s)', (nome, senha, 1))
                    conexao.commit()
                print('Usuário cadastrado com sucesso!')
            except:
                print('Erro ao inserir os dados na database')

    return autenticado, usuarioMaster


def cadastrarProdutos():
    nome = input('Digite o nome do produto: ')
    ingredientes = input('Digite os ingredientes do produto: ')
    grupo = input('Digite o grupo pertencente a este produto: ')
    preco = float(input('Digite o preço deste produto: '))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('insert into produtos(nome, ingredientes, grupo, preco) values (%s,%s,%s,%s)',
                           (nome, ingredientes, grupo, preco))
            conexao.commit()
            print('Produto cadastrado com sucesso!')
    except Exception as e:
        print(e)


def listarProdutos():
    produtos = []

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from produtos')
            produtosCadastrados = cursor.fetchall()

    except Exception as k:
        print(k)

    for i in produtosCadastrados:
        produtos.append(i)

    if len(produtos) != 0:
        pass
        for i in range(0, len(produtos)):
            print(produtos[i])

    else:
        print('Nenhum produto cadastrado.')


def excluirProdutos():
    idDeletar = int(input('Digite o id referente ao produto a ser deletado: '))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('delete from produtos where id = {}'.format(idDeletar))
    except:
        print('Erro ao excluir o produto.')


def listarPedidos():
    pedidos = []
    decision = 0

    while decision != 2:
        pedidos.clear()

        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from pedidos')
                listaPedidos = cursor.fetchall()
        except:
            print('erro no banco de dados')

        for i in listaPedidos:
            pedidos.append(i)

        if len(pedidos) != 0:
            for i in range(0, len(pedidos)):
                print(pedidos[i])
        else:
            print('nenhum pedido foi feito')

        decision = int(input('digite 1 para dar um produto como entregue e 2 para voltar'))

        if decision == 1:
            idDeletar = int(input('digite o id do pedido entregue'))

            try:
                with conexao.cursor() as cursor:
                    cursor.execute('delete from pedidos where id = {}'.format(idDeletar))
                    print('produto dado como entregue')
            except:
                print('erro ao dar o pedido como entregue')


def gerarEstatistica():
    nomeProdutos = []
    nomeProdutos.clear()

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from produtos')
            produtos = cursor.fetchall()
    except:
        print('erro ao fazer consulta no banco de dados')

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from estatisticaVendido')
            vendido = cursor.fetchall()
    except:
        print('erro ao fazer a consulta no banco de dados')

    estado = int(input('digite 0 para sair, 1 para pesquisar por nome e 2 para pesquisar por grupo '))

    if estado == 1:
        decisao3 = int(input('digite 1 para pesquisar por dinheiro e 2 por quantidade unitaria '))
        if decisao3 == 1:

            for i in produtos:
                nomeProdutos.append(i['nome'])

            valores = []
            valores.clear()

            for h in range(0, len(nomeProdutos)):
                somaValor = -1
                for i in vendido:
                    if i['nome'] == nomeProdutos[h]:
                        somaValor += i['preco']
                if somaValor == -1:
                    valores.append(0)
                elif somaValor > 0:
                    valores.append(somaValor + 1)

            plt.plot(nomeProdutos, valores)
            plt.ylabel('quantidade vendida em reais')
            plt.xlabel('produtos')
            plt.show()
        if decisao3 == 2:
            grupoUnico = []
            grupoUnico.clear()

            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from produtos')
                    grupo = cursor.fetchall()
            except:
                print('Erro ao acessar consulta.')

            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from estatisticavendido')
                    vendidoGrupo = cursor.fetchall()
            except:
                print('Erro na consulta.')

            for i in grupo:
                grupoUnico.append(i['nome'])

            print(grupoUnico)

            grupoUnico = sorted(set(grupoUnico)) #varrer toda a lista e ver se tem elementos repetidos
            qntFinal = []
            qntFinal.clear()

            for h in range(0, len(grupoUnico)):
                qntUnitaria = 0
                for i in vendidoGrupo:
                    if grupoUnico[h] == i['nome']:
                        qntUnitaria += 1
                qntFinal.append(qntUnitaria)

            plt.plot(grupoUnico, qntFinal)
            plt.ylabel('quantidade unitária vendida')
            plt.xlabel('produtos')
            plt.show()

    if estado == 2:
        decisao3 = int(input('digite 1 para pesquisar por dinheiro e 2 por quantidade unitaria '))
        if decisao3 == 1:

            for i in produtos:
                nomeProdutos.append(i['grupo'])

            valores = []
            valores.clear()

            for h in range(0, len(nomeProdutos)):
                somaValor = -1
                for i in vendido:
                    if i['grupo'] == nomeProdutos[h]:
                        somaValor += i['preco']
                if somaValor == -1:
                    valores.append(0)
                elif somaValor > 0:
                    valores.append(somaValor + 1)

            plt.plot(nomeProdutos, valores)
            plt.ylabel('quantidade vendida em reais')
            plt.xlabel('produtos')
            plt.show()
        if decisao3 == 2:
            grupoUnico = []
            grupoUnico.clear()

            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from produtos')
                    grupo = cursor.fetchall()
            except:
                print('Erro ao acessar consulta.')

            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from estatisticavendido')
                    vendidoGrupo = cursor.fetchall()
            except:
                print('Erro na consulta.')

            for i in grupo:
                grupoUnico.append(i['grupo'])

            print(grupoUnico)

            grupoUnico = sorted(set(grupoUnico))  # varrer toda a lista e ver se tem elementos repetidos
            qntFinal = []
            qntFinal.clear()

            for h in range(0, len(grupoUnico)):
                qntUnitaria = 0
                for i in vendidoGrupo:
                    if grupoUnico[h] == i['grupo']:
                        qntUnitaria += 1
                qntFinal.append(qntUnitaria)

            plt.plot(grupoUnico, qntFinal)
            plt.ylabel('quantidade unitária vendida')
            plt.xlabel('produtos')
            plt.show()

while not autentico:
    decisao = int(input('Digite 1 para logar ou 2 para cadastrar: '))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from cadastros')
            resultado = cursor.fetchall()

    except:
        print('Erro ao conectar no banco de dados...')

    autentico, usuarioSupremo = logarCadastrar()

if autentico:
    print('Autenticado.')
    decisaoUsuario = 1

    while decisaoUsuario != 0 and usuarioSupremo == True:
        decisaoUsuario = int(input(
            'Digite 0 para sair, 1 para cadastrar produtos, 2 para listar produtos, 3 para listar pedidos e 4 para visualizar as estatísticas : '))
        if decisaoUsuario == 1:
            cadastrarProdutos()
        elif decisaoUsuario == 2:
            listarProdutos()

            delete = int(input('Digite 1 para excluir um produto, 2 para sair: '))

            if delete == 1:
                excluirProdutos()
        elif decisaoUsuario == 3:
            listarPedidos()

        elif decisaoUsuario == 4:
            gerarEstatistica()
