#!/bin/bash
set -e

# Aguarda até que o MongoDB esteja pronto para aceitar conexões
# Isso é importante para evitar que o script tente se conectar antes que o DB esteja totalmente iniciado
# Usa o mongosh para verificar o status
echo "Waiting for MongoDB to start..."
until mongosh --host localhost --eval 'quit(db.runCommand({ ping: 1 }).ok ? 0 : 2)' &>/dev/null; do
  printf '.'
  sleep 1
done
echo "MongoDB started."

# Exporta a senha do secret para a variável de ambiente MONGO_APP_PASSWORD
export MONGO_APP_PASSWORD=$(cat /run/secrets/mongo_app_pass)

# Executa comandos MongoDB para criar o banco de dados e um usuário
mongosh --host localhost <<EOF
  db = db.getSiblingDB('chatbot_db'); // Mudar para o banco de dados 'chatbot_db' (cria se não existir)

  // Criar uma coleção de exemplo (opcional)
  db.createCollection('conversations');

  // Criar um usuário para a sua aplicação com permissões de leitura e escrita no 'chatbot_db'
  // A senha será lida do secret montado em /run/secrets/mongo_app_pass
  db.createUser(
    {
      user: "chatbot_user",
      pwd: "$MONGO_APP_PASSWORD", // Lê a senha da variável de ambiente MONGO_APP_PASSWORD
      roles: [ { role: "readWrite", db: "chatbot_db" } ]
    }
  );
  print("Database 'chatbot_db' and user 'chatbot_user' created successfully.");
EOF