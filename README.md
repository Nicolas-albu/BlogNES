# **BlogNES**

> Neste exercício, o objetivo é criar um blog simples utilizando apenas conceitos básicos do Flask.

## **Restrições**

1. Utilize apenas os conceitos de redirecionamentos, configuração de sessões manualmente com cookies e flash messages.
2. Não utilize extensões do Flask para simplificar o desenvolvimento.
3. O banco de dados deve ser simulado utilizando dicionários.

## **Requisitos**

Implemente as seguintes funcionalidades:

- [x] Criação de uma endpoint API para carregar o conteúdo de todos os posts.

- [x] Sistema de login (`login.html`)

  - [x] Implemente um sistema de login para o admin.
  - [x] Caso o usuário não seja o admin, permita que ele acesse os blogs normalmente.

- [x] Perfil do usuário (`profile.html`)

  - [x] Exibir informações sobre o usuário (nome, foto de perfil, etc)
  - [x] Implemente um formulário para o usuário poder editar seu usuário.

- [x] Página de criação de posts (`create_post.html`)

  - [x] Criar um novo post, fornecendo um título e conteúdo.

- [x] Página de visualização de Post (`post.html`)

  - [x] Exibir o título, conteúdo e os comentários.

- [x] Área de comentários (Opcional)

  - [x] Adicione a funcionalidade de comentários em cada post. Cada comentário deve ter um autor e conteúdo.

- [x] Página inicial (`index.html`)

  - [x] Esta página deverá exibir uma lista de posts, com paginação usando QueryString.
  - [x] Uma barra de pesquisa para filtrar os posts.

## **Modificações**

- Modificar o endpoint `/api/allPosts` para `api/getPosts?page=<NUMERO_DA_PAGINA>`.
- Na rota `/` será apresentado a View `ìndex.html`. Esta View irá realizar o seguintes passos:
- A View terá uma variável contador `nextPage`.
- A View irá consultar o endpoint `api/getPosts` para obter os posts utilizando `nextPage` para definir a página atual.
- A View irá apresentar esses posts obtidos.
- Será apresentado um botão `id="btnNextPage"`, com a funcionalidade de paginação na View.
- A View irá consultar novamente a endpoint `api/getPosts`, para obter os posts utilizando `nextPage` (valor da próxima página).
- Este botão `id="btnNextPage"` irá remover todos os posts da página atual, e
- Irá para apresentar os posts na View.
