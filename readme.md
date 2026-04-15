# Email sender (HTML + Jinja2)

## Motivação

Este projeto surgiu de uma necessidade real no contexto da empresa em que trabalho em regime **CLT**. Estávamos a preparar a entrada de **vários distribuidores** num processo de **homologação** e era preciso **contactar cada um por e-mail**, com o mesmo tipo de comunicação (onboarding, prazos, próximos passos), mas **sem misturar destinatários** entre parceiros.

Além dos contatos próprios de cada distribuidor, os **supervisores da indústria** (fabricante cujos produtos o distribuidor comercializa) **precisavam estar em cópia (Cc)** para acompanharem o processo. O ponto crítico: **cada distribuidor está ligado a um supervisor diferente** - não havia uma lista única de Cc para todos. Era indispensável **diferenciar por distribuidor**: destinatários principais (`to`) e cópias (`cc`) específicos, enquanto o corpo do e-mail podia partilhar a mesma estrutura, apenas personalizando o nome do parceiro e o que mais fosse relevante.

Daí a abordagem com **JSON por distribuidor** + **template HTML com Jinja2**: um envio em lote, mas com listas de e-mail e texto sob medida para cada caso.

---

Script em Python que envia e-mails em HTML personalizados por distribuidor, usando um template [Jinja2](https://jinja.palletsprojects.com/) e anexo inline de imagem (logo). O exemplo usa **Gmail** via SMTP com SSL.

## Requisitos

- [Python 3.10+](https://www.python.org/downloads/) (recomendado 3.11 ou superior)
- Conta Gmail com **palavra-passe de aplicação** (se tiveres autenticação em dois passos ativa) ou credenciais SMTP válidas para `smtp.gmail.com`

## Instalação

1. **Clona ou descarrega** o repositório e entra na pasta do projeto.
2. **Cria um ambiente virtual** (opcional mas recomendado):
  ```bash
   python -m venv .venv
  ```
3. **Ativa o ambiente virtual**
  - Windows (PowerShell):
  - Windows (cmd):
    ```cmd
    .venv\Scripts\activate.bat
    ```
  - macOS / Linux:
    ```bash
    source .venv/bin/activate
    ```
4. **Instala as dependências**
  ```bash
   pip install -r requirements.txt
  ```
5. **Configura variáveis de ambiente**
  Cria um ficheiro `.env` na raiz do projeto (este ficheiro está no `.gitignore` e **não** deve ser commitado):
   Para Gmail com 2FA: [Google Account → Segurança → Palavras-passe das aplicações](https://myaccount.google.com/apppasswords).
6. **Imagem do e-mail**
  Garante que existe o ficheiro `assets/logo-example.png` (é referenciado no template e anexado ao e-mail com `Content-ID` para aparecer no HTML).

## Dados dos destinatários

Edita `data/distributors.json`. Cada objeto representa um envio (um e-mail com os mesmos destinatários em `to` e cópias em `cc`):

```json
[
  {
    "distributor_name": "Nome do parceiro",
    "to": ["destinatario@exemplo.com"],
    "cc": ["copia@exemplo.com"]
  }
]
```

- `**distributor_name**`: usado no assunto e no corpo do template.
- `**to**`: lista de e-mails principais (obrigatório ter pelo menos um para o Gmail aceitar o envio).
- `**cc**`: lista de cópias (pode ser `[]`).

Campos adicionais que coloques no JSON ficam disponíveis no template Jinja2 como `{{ nome_do_campo }}`.

## Utilização

Com o ambiente virtual ativo e o `.env` preenchido:

```bash
python main.py
```

O script:

1. Lê `SMTP_FROM` e `SMTP_PASSWORD` do `.env`.
2. Carrega `data/distributors.json`.
3. Abre ligação **SMTP_SSL** a `smtp.gmail.com:465`, faz login e, para cada entrada do JSON, renderiza `templates/email_template.html` e envia o e-mail.

No terminal deves ver uma linha de confirmação por distribuidor, por exemplo: `✅ Nome — enviado para N contatos`.

## Personalizar o template

- Ficheiro principal: `templates/email_template.html`.
- Variáveis do logo: o `sender.py` injeta `logo_example_cid` para usar no HTML com `cid:{{ logo_example_cid }}`.
- Lógica de envio e MIME: `sender.py`.

## Notas de segurança

- **Nunca** commits o `.env` nem palavras-passe reais.
- Para repositório público, usa apenas exemplos em `distributors.json` (e-mails fictícios) ou mantém dados reais fora do Git.

## Estrutura do projeto

```
├── main.py                 # Entrada: SMTP, loop pelos distribuidores
├── sender.py               # Montagem do MIME (HTML + imagem inline)
├── requirements.txt
├── .env                    # Criar localmente (não versionar)
├── data/
│   └── distributors.json   # Lista de envios
├── templates/
│   └── email_template.html
└── assets/
    └── logo-example.png
```

