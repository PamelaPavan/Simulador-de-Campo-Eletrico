<h1 align="center">💡 Simulador de Campo Elétrico</h1>

<p align="justify">
Este projeto é uma aplicação web interativa desenvolvida com Python (Flask) e JavaScript. Ele permite visualizar e compreender de forma animada os conceitos de campo elétrico, linhas equipotenciais e potencial elétrico gerados por duas cargas puntiformes. A aplicação conta com a presença do Maxwell, um assistente virtual que narra o conteúdo apresentado para tornar a experiência mais inclusiva e didática.
</p>



### 🧠 Funcionalidades

- Geração automática de animações que mostram as linhas de campo e equipotenciais.

- Leitura em voz do conteúdo exibido (com opção de ativar/desativar som).

- Textos explicativos dinâmicos com navegação.

Como utilizar:
1. Insira os valores das cargas nos campos disponíveis e clique em simular
<img src="static/assets/img2.png">
📸 Demonstração
<img src="static/assets/image.png">
O mascote Maxwell fala com o usuário e exibe explicações baseadas nas cargas inseridas.

1. Instale as dependências necessárias

No terminal escreva:
```
pip install -r requirements.txt
```

2.  Execute o servidor

```
python app.py
```

3. Acesse a aplicação no navegador

Abra o navegador e acesse:

```
http://127.0.0.1:5000
```

📁 Estrutura do projeto

```

├── app.py                  # Servidor Flask
├── templates/
│   └── index.html          # Página principal
├── static/
│   ├── js/                 # Arquivos JS com lógica do Maxwell
│   ├── assets/             # Imagens do mascote Maxwell
│   └── simulacao.gif       # GIF gerado pela simulação
└── README.md               # Este arquivo
```

📦 Requisitos Python

    Python 3.8+

    Flask

    NumPy

    Matplotlib


### Autor

<p>Pâmela Aliny Cleto Pavan</p>

pamelaaliny@gmail.com