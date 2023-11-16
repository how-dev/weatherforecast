# Weather Forecast

## Considerações:

✨Para pular para o tópico de rodar o projeto localmente, clique
[aqui](#rodando-o-projeto-localmente).

Este é um projeto que, por mais simples que seja, inspirado em
arquitetura limpa, ddd e arquitetura hexagonal. A grande ideia é
que você seja capaz de rodar qualquer parte do código em qualquer
interface que você queira: seja num terminal, webserver, etc.

Os princípios dizem para separar as camadas em repositórios
separados, mas devido a simplicidade do projeto, eu preferi
separar em módulos. Quando não há a separação em repositórios,
o isolamento das camadas não fica tão evidente, mas ainda assim
é possível ver que as camadas estão bem separadas.

### Basic

O módulo basic não faz parte de nenhuma camada, ele é um módulo
que contém classes básicas para montar entidades e adaptadores.
Ele é um módulo que pode ser usado em qualquer camada, e os
adaptadores são usamos pelas entidades por meio de injeção
de dependência.

O basic foi construido em cima de uma premissa: Entidades se
persistem, mas não conhecem a forma como são persistidas. Por
isso, as entidades não devem conhecer os adaptadores, mas os
adaptadores devem conhecer as entidades.

### Domain (camada mais interna)

O módulo domain é o módulo que contém as entidades. Nesse sistema
possuímos apenas uma entidade, que é a entidade de previsão do
tempo. Essa entidade é persistida por meio de um adaptador, que
não é conhecido pela entidade. Se eu construisse um adaptador para
MySQL, por exemplo, eu poderia persistir a entidade de previsão.

### mongodb_adapter

O módulo mongodb_adapter é o módulo que contém o adapter para
o MongoDB. Também seria um repositório totalmente a parte que
poderia ser acessado de qualquer outro projeto.

### Adapters

O módulo adapters é o módulo que contém os adaptadores para
interfaces. Nesse caso, temos apenas um adaptador para a
previsão do tempo.

### Backend (camada mais externa)

O módulo backend é o módulo que contém os casos de uso (interactors).
Os interactors são responsáveis por orquestrar as entidades e os
adaptadores. Eles são responsáveis por fazer a comunicação entre
as camadas. No nosso caso, também tenho um client para consumir
a api do OpenWeather, que seria uma espécie de um adapter, mas
focado em uma interface externa.

## Rodando o projeto localmente

1. Para rodar o projeto localmente, primeiro certifique-se de
ter mongodb instalado e rodando na porta 27017.

2. Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```dotenv
DB_HOST=mongodb://localhost:27017/
DB_NAME=weatherresearch
OPEN_WEATHER_APP_ID=...
OPEN_WEATHER_API_URL=https://api.openweathermap.org/data/3.0/onecall
```

3. Rode o comando `make install` para instalar as dependências.

4. Rode o comando `make run` para rodar o projeto.
> Esse comando subirá o projeto utilizando o framework flask na porta 5000.
> 💡Para validar que o sistema não está dependendo de framework para rodar, se quiser,
> basta rodar o arquivo `pure.py` com o comando `python pure.py`, que nele eu
> não utilizo o flask e nenhum outro framework modinha =) Ah, se quiser rodar um 
> interactor no console, ou rodar um adapter no console também, fique a vontade.

5. Na raiz do projeto, eu deixei um arquivo chamado `howard_request_collection.json`, que
é um arquivo de importação para o Insomnia. Caso você queira testar a api, basta
importar esse arquivo no Insomnia e testar as rotas.

### Úteis, caso queira rodar algo no console

#### Criar
```python
from backend.services.getters import get_open_weather_service
from adapters.getters import get_weather_forecast_adapter
from backend.interactors.create_weather_forecast_interactor import CreateWeatherForecastInteractor
adapter = get_weather_forecast_adapter()
service = get_open_weather_service()
interactor = CreateWeatherForecastInteractor(adapter, service)
response = interactor.run()
```

#### Listar
```python
from adapters.getters import get_weather_forecast_adapter
from backend.interactors.list_weather_forecast_interactor import ListWeatherForecastInteractor

adapter = get_weather_forecast_adapter()
interactor = ListWeatherForecastInteractor(adapter)
response = interactor.run()
```

#### Buscar
```python
from adapters.getters import get_weather_forecast_adapter
from backend.interactors.detail_weather_forecast_interactor import DetailWeatherForecastInteractor

adapter = get_weather_forecast_adapter()
entity_id = 'algum_id'
interactor = DetailWeatherForecastInteractor(adapter, entity_id)
response = interactor.run()
```

#### Deletar

```python
from adapters.getters import get_weather_forecast_adapter
from backend.interactors.delete_weather_forecast_interactor import DeleteWeatherForecastInteractor

adapter = get_weather_forecast_adapter()
entity_id = 'algum_id'
interactor = DeleteWeatherForecastInteractor(adapter, entity_id)
interactor.run()
```

