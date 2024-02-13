Link para a collection do Postman = https://drive.google.com/file/d/1ZOeXc1k7sY_atcwqRmGdBCztKtPffAV7/view?usp=sharing


# Avisos
- Existem comandos para disparo dos testes através do Makefile: make test e make test_parallel
- Comando para gerar o requirements.txt: make requirements.
- Como virtual environment foi utilizado o poetry, para carregar as dependências em uma nova virtual environment, use o comando poetry install para instalar as dependências e depois poetry shell para iniciar a virtual env.


# Desafio
Esse desafio tem como objetivo avaliar as habilidades necessárias de um desenvolvedor back-end, 
visando atender os requisitos da stack da Keeps.
## O Desafio
O candidato deverá criar uma aplicação Server-Side que irá permitir gerir uma 'mini' solução de e-learning, 
que terá cursos, alunos e matrículas. Essa aplicação deverá ter as APIs expostas para que uma aplicação WEB
possa consumir os recursos.
O teste está dividido em fases de dificuldades. Não são obrigatórias todas as etapas e nem precisam ser executadas na sequência, o candidato será avaliado pelas quais foram concluídas, sendo que, quanto mais longe o candidato avançar no desafio, teremos mais condições de avaliar e melhor será sua pontuação.
- Nesse teste você poderá usar os frameworks **Django ou Flask.**
- Você pode usar qualquer banco de dados (Relacional como MySQL ou Postgres)

### 1) API Básica
A modelagem do projeto terá os seguintes modelos.
- Course (name, description, holder_image, duration, date_created, date_updated) [x]
- Student (name, nickname, phone, avatar, date_created, date_updated) [x]
- Enrollment (student, course, date_enroll, date_close, score, status) / * Status = (Aprovado, Reprovado, Andamento) [x]

#### A API deverá fornecer recursos para:
- Listar todos os cursos do catalogo
- Cadastrar e atualizar novos cursos
- Excluir cursos existentes
- Listar todos os alunos
- Cadastrar/Editar novos alunos
- Matricular um aluno em um curso
- Remover o aluno de um curso
Regras de négocios a ser implementadas:
- Um usuário pode desistir de um curso e informar uma justificativa
- Um usuário não pode estar matriculado em mais de uma curso ao mesmo tempo (matrícula em andamento - ativa)
- Um usuário não pode ser considerado aprovado se ele obter uma nota menor que 6 ao concluir uma matrícula
- Um curso pode notificar (pode ser um print) os usuários que estão matriculados que o curso irá ser expirado em X dias.
- Um curso pode notificar o usuário dono do curso que novas matrículas foram iniciadas ou concluídas

##### O que será avaliado
- Noções básicas de modelagem de dados (banco)
- Criação de endpoints e uso correto dos verbos HTTP
- Configuração básica do projeto, seja em Django ou Flask (usar da forma mais indicada para cada um dos frameworks)
- Separação das camadas (view, model, service, ...)
### 2) Filtros
Um recurso importante das APIs é a capacidade de prover filtros para que o front-end possa criar suas soluções otimizando recursos e dando flexibilidade para os usuários. Sendo assim, a API deverá ser possível:
- Filtrar quais matrículas foram reprovadas
- Filtrar todas as matrículas de um determinado aluno
- Filtrar todas as matrículas de um determinado curso
- Filtrar as matrículas que foram concluídas em um determinado período;
- Filtrar as matrículas que foram iniciadas em um determinado período;
- Filtrar alunos cadastrados em um determinado período;
##### O que será avaliado
- Recursos mais avançados de uma API
- Capacidade de pensar como o front poderia precisar da sua API

### 3) Criação de testes unitários e integração
  
Outro ponto importante no desenvolvimento de aplicações são os testes. Nesse item queremos avaliar se
o candidato tem conhecimento com ferramentas de testes e consegue ter uma compreensão ampla do contexto.
Como a aplicação é pequena, será mais difícil criar testes de serviços ou modelos. Fazer os testes das APIs,
simulando o request/response. dica de como fazer com Django:
https://realpython.com/test-driven-development-of-a-django-restful-api/
Em Flask também possuem modelos parecidos.
##### O que será avaliado
- Noções básicas de testes
- Testes descritivos (fácil entender o que o teste testa)
- Cobertura

*OBS: Escrever testes para todos os cases das regras de negócios mapeadas no item 1.
### 4) Criar testes de e2e com POSTMAN
Quando estamos desenvolvendo aplicações server-side precisamos testar nossas APIs como a mesma visão de um cliente. Uma forma mais simples de fazer isso, para não ter que desenvolver o front-end é usar uma ferramenta para que você possa simular as chamadas a essas APIs.
Para isso, utilizamos o Postman, mas você pode utilizar outro de seu conhecimento. Nesse item você deverá:
- Simular todas as chamadas das suas APIs;
- Criar um runner (Postman é possível) para rodar em sequência todas as APIs, simulando um fluxo de uso
--- exemplo: cadastrar um usuário, cadastrar um curso e matricular esse usuário nesse curso
- Em todas as etapas, colocar um test para verificar se tudo está ok.
Download e acesso:
 https://www.postman.com/
Tutorial para criar testes:
 https://medium.com/assertqualityassurance/automatizando-sua-api-com-postman-64a72185e1e6
##### O que será avaliado
- Conhecimento do POSTMAN;
- Se não conhecer o POSTMAN, capacidade de aprendizagem;
- Compreensão da API;
- Capacidade de entender quais são os fluxos de um sistema e testá-los;
### 5) Documentação
Além de uma boa documentação dentro do próprio código, é importante que tenha uma documentação consistente da APIs para que quem for consumir tenha todas as informações necessárias.
Normalmente utilizamos o Swagger (ou Redoc) para criar documentações que tragam todas as informações necessárias. Você deverá:
- Instalar o Swagger (ou similar)
- Configurar seu projeto
- Em muitos casos (Django + Swagger) a documentação é gerada automaticamente, mas é necessário complementar a descrição, dessa forma esperamos que a documentação esteja a mais clara possível.
##### O que será avaliado
- Conhecimento Swagger (ou outro);
- Escrita da Documentação (explicação clara, objetiva)
### 5) Task Async
Criar uma rotina, que ao adicionar uma nova matricula a um aluno, seja populada uma tabela com o nome enrollment_full_info com os dados:
student_name, course_name, course_description, course_duration, enrollment_id, enrollment_date, enrollment_status.
Basicamente você ira agregar os dados de 3 tabelas em uma mas utilizando uma tarefa assíncrona.
##### O que será avaliado
- Conceitos básicos de programação assíncrona e suas aplicações