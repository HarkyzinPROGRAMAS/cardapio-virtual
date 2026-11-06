# ☕ Café do Garotinho — Cardápio Virtual

Sistema de cardápio virtual desenvolvido para facilitar o atendimento e o gerenciamento de pedidos de uma cafeteria. O projeto permite que clientes acessem o cardápio por meio de QR Codes, realizem pedidos e acompanhem o funcionamento do atendimento, enquanto a equipe gerencia produtos, pedidos e pagamentos.

## 📌 Sobre o projeto

O Café do Garotinho foi desenvolvido como projeto acadêmico do curso de Ciência da Computação, com o objetivo de aplicar conceitos de desenvolvimento Backend, integração com banco de dados, organização em camadas e comunicação entre Frontend e Backend.

A aplicação oferece um cardápio digital organizado por categorias e um painel administrativo para que os funcionários possam acompanhar e atualizar os pedidos recebidos.

## 🚀 Funcionalidades

### Cardápio virtual
- Acesso ao cardápio por meio de QR Codes das mesas.
- Exibição dos produtos disponíveis.
- Organização dos produtos por categorias.
- Identificação automática do número da mesa pelo QR Code.
- Visualização de preços e informações dos produtos.

### Gerenciamento de produtos
- Cadastro de produtos.
- Definição de nome, preço, disponibilidade e categoria.
- Consulta dos produtos cadastrados.
- Controle de acesso ao cadastro de produtos para administradores.

### Gerenciamento de pedidos
- Criação de pedidos pelos clientes.
- Identificação do cliente e número da mesa.
- Inclusão de vários produtos em um mesmo pedido.
- Cálculo automático do valor total pelo Backend.
- Consulta e filtragem de pedidos por status.
- Atualização do andamento dos pedidos.
- Atualização automática do painel a cada 30 segundos.

### Controle de status

Os pedidos seguem um fluxo definido de atualização:

- **Pendente:** pedido recebido.
- **Em preparo:** pedido em preparação.
- **Pronto:** pedido pronto para entrega.
- **Finalizado:** pedido concluído.
- **Cancelado:** pedido cancelado.

O sistema impede transições inválidas entre os status.

### Pagamentos
- Registro de pagamentos por Pix, Dinheiro ou Cartão.
- Registro do valor e da data do pagamento.
- Impedimento de pagamentos duplicados.
- Exibição da situação do pagamento no painel.

**Observação:** o sistema registra os pagamentos realizados pela equipe. Não possui integração automática com instituições financeiras ou processamento de pagamentos online.

### Arquivamento de pedidos
- Permite retirar pedidos finalizados do painel.
- Exige que o pedido esteja com status Finalizado.
- Exige que o pagamento esteja registrado.
- Mantém os pedidos arquivados armazenados no banco de dados.
- Oculta pedidos arquivados da listagem normal do painel.

### Autenticação e controle de acesso
- Login e logout de usuários.
- Senhas armazenadas com hash.
- Perfis de acesso ADMIN e FUNCIONARIO.
- Proteção das funcionalidades administrativas.
- Gerenciamento de usuários por administradores.
- Verificação de usuários ativos.

## 🛠️ Tecnologias utilizadas

### Backend
- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- SQLAlchemy
- PostgreSQL
- Python-Dotenv

### Frontend
- HTML5
- CSS3
- JavaScript
- Fetch API
- Async/Await

### Outras bibliotecas
- QRCode
- Pillow
- Werkzeug

## 🏗️ Arquitetura do projeto

O projeto utiliza uma arquitetura organizada em três camadas principais:

- **Controller:** recebe as requisições, chama os serviços e devolve as respostas.
- **Service:** concentra as validações e regras de negócio.
- **Repository:** responsável pelas operações de acesso e manipulação dos dados no banco.

Essa organização facilita a manutenção e separa as responsabilidades de cada parte da aplicação.

## 🔐 Segurança

O projeto utiliza alguns mecanismos para proteger os dados e controlar o acesso:

- Senhas armazenadas utilizando hash.
- Chave secreta configurada por variável de ambiente.
- Arquivo `.env` excluído do versionamento.
- Controle de acesso baseado em perfis.
- Validações no Backend para impedir operações inválidas.
- Verificação de disponibilidade dos produtos antes da criação dos pedidos.

## 👥 Desenvolvedores

Projeto desenvolvido por:

- Renan
- Eriosvaldo

## 🎓 Contexto acadêmico

Projeto desenvolvido como atividade acadêmica do curso de Ciência da Computação, com a finalidade de colocar em prática conhecimentos de programação, desenvolvimento web, banco de dados, arquitetura de software e engenharia de software.

---

**Café do Garotinho — Seu pedido, nosso cuidado! ☕**
