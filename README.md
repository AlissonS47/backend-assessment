Backend Assessment

Olá! 🖖🏽

Nossa intenção é, através deste (breve) desafio, avaliar a habilidade técnica percebida ao empregar e desenvolver uma solução para o problema aqui descrito.

## Domínio Problema

Uma instituição financeira contratou os serviços da T10 buscando maior **agilidade dos dados** através da metrificação de processos que, até então, não eram _observados_ (apropriadamente). Um dos processos é a solicitação do produto débito automático de empresas parceiras.
A operação é realizada manualmente e vai ser automatizada por este serviço, que vai permitir que outros serviços consumam, de forma livre, de seus eventos operacionais.

# Escopo

## Casos de Uso

1. Autenticação e acesso a plataforma

Um usuário autenticado,

2. solicita uma ativação de débito automático
3. cancela uma solicitação de ativação
4. aprova uma solicitação de ativação
5. rejeita uma solicitação de ativação
6. visualiza uma solicitação


Diagrama do [modelo de eventos](img/model.jpg).

Observações **importantes** sobre o modelo:

  - É uma representação do domínio _exclusivamente_.

  - Não é mandatório ser modelado usando CQRS nem event-driven.

  - Não é mandatório implementar o EmailServer

## Requisitos

Especifica o contexto em que a aplicação será operacionalizada

### Não funcionais

1. 30 empresas parceiras
1. 5000 usuários simultâneos
1. 100 reqs/s 

### Funcionais

#### Tecnologias

- implementação: `golang | elixir | python`
- armazenamento: `postgres | mongodb`
- **não-mandatório** broker: `kafka | rabbitmq`

#### Protocolos

- pontos de entrada: `http`
- autenticação: `simple jwt`

#### Padrões

Bonus points:

- arquitetural: `cqrs & hexagonal`
- design: `ddd & solid`
- message bus as stream

### 3rd parties

O uso de bibliotecas externas é **livre**.

### Deployment

A forma como a aplicação será disponibilizada é **livre**. Fica a critério do candidato, por exemplo, usar algum PaaS a fim de reduzir a complexidade bem como utilizar receitas prontas através de ferramentas de automatização e.g. `ansible+dockercompose`.

No entanto, é esperado bom senso na documentação caso sejam usadas soluções @ `localhost`.

# Entrega

A _Release_ 0.1 🚀 consiste na implementação de um servidor web que implementa os casos de uso listados acima respeitando os requisitos funcionais e não funcionais. Fica a critério do desenvolvedor como os testes serão escritos, os scripts de _data migration_, os _schemas_ de entrada e saída da api e todas as outras definições que não foram listadas neste documento.

## Avaliação

Critérios ordenados por ordem de peso decrescente:

1. Correção (_correctness_) da solução

   - a fim de solucionar o [domínio-problema](#domínio-problema)
   - a fim de cumprir os [casos de uso](#casos-de-uso)
   - ao implementar os [requisitos](#requisitos) especificados

1. Testes
1. Organização, documentação e clareza na estruturação do projeto
1. Estilo, legibilidade e simplicidade no código
1. Escolhas e uso de 3rd parties
1. Padrões de segurança

#### Bonus points 🏆

1. Teste de stress
1. Boas práticas na modelagem e armazenamento de dados

## Eliminatórios

1. Copiar ou "se inspirar" em código alheio é _veementemente_ vetado ✋

## Submissão

Ao finalizar a implementação, o diretório da solução pode ser submetido de duas formas:

1. através de um _fork_ e um _pull request_ neste repositório ou
1. por email, compactado, para `it@t10.digital` com o assunto `Backend Assessment`

Feito 🤘



# Documentação

### Rotas:
- users/registration/ 
  - Rota para criação de usuários, recebe como parâmentros username, email e password
  
- users/login/
  - Rota para login de usuários, recebe como parâmetros username e password e retorna dois tokens JWT, "access" e "refresh"
  
- users/login/refresh/ 
  - Rota para atualizar o token JWT expirado, recebe como parâmentro o token refresh, e retorna um novo token access
  
- requests/ 
  - Se utilizado o método GET por um usuário normal, retorna todas as solicitações deste usuário. Se utilizado por um super usuário,
    retorna as solicitações de todos os usuários
  
- requests/ 
  - Se utilizado o método POST, registra uma request, recebendo como parâmetro "message"
  
- requests/{id}/ 
  - Se utilizado o método GET por um super usuário, retorna a solicitação correspondente ao id
  
- requests/{id}/ 
  - Se utilizado o método PATCH por um super usuário, faz uma atualização parcial da solicitação correspondente ao id, sendo possível
    atualizar somente o "status" da solicitação
    
- requests/{id}/ 
  - Se utilizado o método DELETE pelo dono da solicitação, cancela a solicitação correspondente ao id

### Detalhes:
- Autenticação
  - Com exceção das rotas de registro e login de usuário, todas as outras requerem autenticação via token JWT

- Login
  - Ao fazer login, o usuário recebe dois tokens JWT, "refresh" e "access". O token access é utilizado para realizar a autenticação nas 
    rotas, já o token refresh é utilizado para atualizar o token access expirado
  ```
          {
              "refresh": "...",
              "access": "..."
          }
  ```

- Buscas
  - Na rota requests/ é possível fazer uma busca via query string, o parâmetro utilizado é "checked" e com ele é possível buscar as 
    solicitações que já foram ou não checadas. A busca fica na forma *requests/?checked=true*

## Nota Final
A API está disponível neste endereço: https://backend-assessment47.herokuapp.com/ <br/>
Todos os testes manuais foram feitos com o auxílio do software Postman <br/>
Super usuário para testes:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;username: super<br/>
&nbsp;&nbsp;&nbsp;&nbsp;password: super123<br/>
Desde já, agradeço pela oportunidade, fico a disposição :v::smile:


