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

- [ ] Página de criação de posts (`create_post.html`)

  - [ ] Criar um novo post, fornecendo um título e conteúdo.

- [ ] Página de visualização de Post (`post.html`)

  - [ ] Exibir o título, conteúdo e os comentários.

- [ ] Área de comentários (opcional)

  - [ ] Adicione a funcionalidade de comentários em cada post. Cada comentário deve ter um autor e conteúdo.

- [ ] Página inicial (`index.html`)

  - [ ] Esta página deverá exibir uma lista de posts, com paginação usando QueryString.
  - [ ] Uma barra de pesquisa para filtrar os posts.
