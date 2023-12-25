from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Устанавливаем внешние стили для приложения
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Загружаем данные из CSV-файла
df = pd.read_csv('main.csv')

# Получаем уникальные типы услуг
service_types = df['Тип услуги'].unique()

# Определяем структуру и стиль приложения
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    # Заголовок приложения
    html.H1('Продажи продуктового магазина', style={'text-align': 'center', 'color': '#2c3e50'}),

    # Первый блок: Круговая диаграмма и гистограмма с ползунком
    html.Div([
        # Левая часть блока
        html.Div([
            # Заголовок блока
            html.H4('Выберите тип услуги:', style={'color': '#2c3e50'}),
            # Выпадающий список для выбора типа услуги
            dcc.Dropdown(
                id='service-type',
                options=[{'label': service, 'value': service} for service in service_types],
                value='Техническое обслуживание',
                clearable=False,
                style={'width': '80%', 'margin': '0 auto'}
            ),
            # Круговая диаграмма
            dcc.Graph(id="piegraph"),
        ], className='six columns'),  # Половина ширины строки

        # Правая часть блока
        html.Div([
            # Заголовок блока
            html.H4('Распределение стоимости услуг:', style={'color': '#2c3e50'}),
            # Гистограмма с ползунком для распределения стоимости услуг
            dcc.Graph(id='graph-with-slider'),
            # Ползунок для выбора типа услуги
            dcc.Slider(
                id='year-slider',
                min=0,
                max=len(service_types) - 1,
                step=1,
                value=0,
                marks={str(i): str(service_types[i]) for i in range(0, len(service_types))},
            ),
        ], className='six columns'),  # Половина ширины строки

    ], className='row'),

    # Второй блок: График рассеивания с выбором марки автомобиля и типа оси x
    html.Div([
        # Единственная часть блока
        html.Div([
            # Заголовок блока
            html.H4('График рассеивания:', style={'color': '#2c3e50'}),
            # График рассеивания
            dcc.Graph(id='crossfilter-indicator-scatter'),
        ], className='twelve columns'),  # Полная ширина строки

    ], className='row', style={'margin-top': '50px'}),

    # График временного ряда (линейный график) для отображения динамики доходов и расходов
    dcc.Graph(
        id='time-series',
        figure=px.line(df, x='Дата', y='Общая стоимость (руб)', title='Динамика доходов и расходов')
    ),

], style={'max-width': '1200px', 'margin': '0 auto'})

# Callback-функции для обновления графиков при взаимодействии с пользователем

# Callback-функция для обновления графика с распределением стоимости услуг по маркам автомобилей
@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df[df['Тип услуги'] == service_types[selected_year]]

    # Создаем гистограмму
    fig = px.histogram(
        filtered_df,
        x="Общая стоимость (руб)",
        color="Название товара",
        marginal='box',
        nbins=20,
        labels={'Общая стоимость (руб)': 'Общая стоимость (руб)'}
    )

    # Настраиваем внешний вид графика
    fig.update_layout(
        title='Распределение стоимости услуг',
        xaxis_title='Общая стоимость (руб)',
        yaxis_title='Количество',
        transition_duration=500,
        showlegend=False
    )

    return fig

# Callback-функция для обновления круговой диаграммы с распределением общей стоимости по маркам автомобилей
@app.callback(
    Output("piegraph", "figure"),
    Input("service-type", "value"))
def generate_chart(service_type):
    jjj = df[df['Тип услуги'] == service_type]
    fig = px.pie(
        jjj,
        values='Общая стоимость (руб)',
        names='Название товара',
        hole=.3,
        title=f'Распределение общей стоимости для услуги: {service_type}'
    )
    return fig

# Callback-функция для обновления графика рассеивания
@app.callback(
    Output('crossfilter-indicator-scatter', 'figure'),
    Input('service-type', 'value'))
def update_graph(service_type):
    dff = df[df['Тип услуги'] == service_type]

    # Создаем график рассеивания
    fig = px.scatter(
        dff,
        x='Стоимость доставки (руб)',
        y='Стоимость продукта (руб)',
        color='Тип продукта',
        size='Общая стоимость (руб)',
        hover_name='Номер заказа'
    )

    # Настраиваем внешний вид графика
    fig.update_layout(
        title='График рассеивания стоимости услуг',
        xaxis_title='Стоимость доставки (руб)',
        yaxis_title='Стоимость продукта (руб)',
        transition_duration=500
    )

    return fig

# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)
