# 📂 API Response Saver Automation (S3 Bucket) 🤖

Este projeto automatiza a coleta de dados de uma API em intervalos regulares e armazena a resposta em arquivos JSON localmente, além de enviá-los para um bucket S3 na AWS. Ele é útil para coletar e armazenar dados de APIs de forma automatizada, com agendamento flexível. 📊☁️

## 🛠️ Funcionalidades

- **🌐 Requisição HTTP**: Faz uma requisição GET para uma URL configurada.
- **💾 Salvamento de Dados**: Salva a resposta da API em um arquivo JSON com carimbo de data/hora no formato `ano-mês-dia-hora-minuto.json`.
- **⏰ Agendamento Flexível**: Executa a coleta de dados em intervalos configuráveis, definidos via variável de ambiente.
- **📤 Envio para S3**: Envia os arquivos JSON gerados para um bucket S3 na AWS.

## 📋 Pré-requisitos

- 🐍 Python 3.x
- 📚 Bibliotecas Python: `requests`, `boto3`, `schedule`, `python-dotenv`
- 🌐 Conta na AWS (para configurar o S3)
- 🌍 Acesso à API que deseja consultar

## ⚙️ Configuração

1. **Instale as dependências**:
   Primeiro, crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Para Linux/Mac
   venv\Scripts\activate  # Para Windows
   ```
   Em seguida, instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. **Crie um arquivo `.env`** na raiz do projeto com as seguintes variáveis de ambiente:
   ```plaintext
   REQUEST_URL=<URL_da_API>
   SCHEDULE_INTERVAL_HOURS=<intervalo_em_horas>  # Exemplo: "4"
   MAX_RETRIES=<número_de_retentativas>  # Exemplo: "144"
   AWS_ACCESS_KEY_ID=<sua_chave_de_acesso_AWS>
   AWS_SECRET_ACCESS_KEY=<sua_chave_secreta_AWS>
   S3_BUCKET_NAME=<nome_do_seu_bucket_S3>
   ```

   - `REQUEST_URL`: URL da API que será consultada.
   - `SCHEDULE_INTERVAL_HOURS`: Intervalo em horas entre as execuções do script.
   - `MAX_RETRIES`: Número máximo de tentativas em caso de falha na requisição.
   - `AWS_ACCESS_KEY_ID`: Chave de acesso da sua conta AWS.
   - `AWS_SECRET_ACCESS_KEY`: Chave secreta da sua conta AWS.
   - `S3_BUCKET_NAME`: Nome do bucket S3 onde os arquivos JSON serão enviados.

3. **Execute o script**:
   ```bash
   python seu_script.py
   ```

## 🚀 Como Funciona

1. O script valida as variáveis de ambiente e carrega as configurações.
2. A cada intervalo configurado (`SCHEDULE_INTERVAL_HOURS`), ele:
   - 🌐 Faz uma requisição GET para a URL configurada.
   - 💾 Salva a resposta em um arquivo JSON com o nome no formato `response_YYYY-MM-DD_HH-MM.json`.
   - 📤 Envia o arquivo gerado para o bucket S3 na AWS.

## 📄 Exemplo de Saída

- **Arquivo JSON**:
  ```json
  {
      "config": {
          "status": "scheduled"
      }
  }
  ```

- **S3**:
  - O arquivo será armazenado no bucket S3 com o nome `response_YYYY-MM-DD_HH-MM.json`.
  - **Exemplo de chave no S3**: `response_2025-02-04_12-30.json`

## 🎨 Personalização

- **☁️ Configuração do S3**: Caso queira usar outra solução de armazenamento (como Google Cloud Storage ou outro serviço), basta modificar o método de envio para o S3.
- **📄 Formato do JSON**: Ajuste o tratamento da resposta da API no método `fetch_and_save` conforme necessário.
- **🔄 Intervalo de Execução**: O intervalo de execução pode ser facilmente ajustado modificando a variável `SCHEDULE_INTERVAL_HOURS` no arquivo `.env`.

## ⚠️ Observações

- **🔒 Segurança**: Não compartilhe o arquivo `.env` ou credenciais da AWS publicamente.
- **📜 Logs**: O script imprime logs no console para facilitar a depuração. 
- **🚀 Acessibilidade**: Certifique-se de que a URL da API e as credenciais AWS são válidas.

## 📜 Licença

Este projeto é open-source. Sinta-se à vontade para utilizá-lo e modificá-lo conforme suas necessidades. 🎉