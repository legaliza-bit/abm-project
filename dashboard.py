from model import EconomyModel
import numpy as np

import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

theme = 'minty'

bg_color = 'rgb(252, 248, 227)'

suppress_callback_exceptions = True


def blank_fig(**update_layput_params):
    fig = go.Figure(go.Scatter(x=[0], y=[0]))
    fig.update_layout(**update_layput_params)
    return fig


table_header = [
    html.Thead(html.Tr([html.Th("Description"), html.Th("Symbol"), html.Th("Value")]))
]

row1 = html.Tr([html.Td("Exponential MA Parameter"), html.Td(dcc.Markdown("$\\omega$",mathjax=True)), html.Td("0.2")])
row2 = html.Tr([html.Td("Lending rate mark-up"), html.Td(dcc.Markdown("$\\mu_{loan}$",mathjax=True)), html.Td("0.5")])
row3 = html.Tr([html.Td("Deposit mark-down"), html.Td(dcc.Markdown("$\\mu_{dep}$",mathjax=True)), html.Td("0.1")])
row4 = html.Tr([html.Td("Loan-to-value ratio"), html.Td(dcc.Markdown("$ltv$",mathjax=True)), html.Td("0.5")])
row5 = html.Tr([html.Td("Price adjustment"), html.Td(dcc.Markdown("$\\nu_p$",mathjax=True)), html.Td("0.1")])
row6 = html.Tr([html.Td("Excess supply sensitivity"), html.Td(dcc.Markdown("$\\eta_-$",mathjax=True)), html.Td("0.2")])
row7 = html.Tr([html.Td("Excess demand sensitivity"), html.Td(dcc.Markdown("$\\eta_+$",mathjax=True)), html.Td(dcc.Markdown("$\\rho (t) \\eta_-$",mathjax=True))])
row8 = html.Tr([html.Td("Wage rigidity"), html.Td(dcc.Markdown("$\\gamma$",mathjax=True)), html.Td("0.6")])
row9 = html.Tr([html.Td("Household sensitivity parameter"), html.Td(dcc.Markdown("$\\alpha$",mathjax=True)), html.Td("0.05")])
row10 = html.Tr([html.Td("EV of idiosyncratic consumption"), html.Td(dcc.Markdown("$\\mu_k$",mathjax=True)), html.Td("20")])
row11 = html.Tr([html.Td("St.dev. of idiosyncratic consumption"), html.Td(dcc.Markdown("$\\sigma_k$",mathjax=True)), html.Td("10")])
row12 = html.Tr([html.Td("EV in case of investment"), html.Td(dcc.Markdown("$\\mu_1$",mathjax=True)), html.Td("0.012")])
row13 = html.Tr([html.Td("EV in case of no investment"), html.Td(dcc.Markdown("$\\mu_2$",mathjax=True)), html.Td("0.01")])
row14 = html.Tr([html.Td("St.dev. of investment outcome"), html.Td(dcc.Markdown("$\\sigma$",mathjax=True)), html.Td("0.0115")])


table_body = [html.Tbody([row1, row2, row3, row4, row5, row6, row7,
                          row8, row9, row10, row11, row12, row13, row14])]

app = dash.Dash(external_stylesheets=[dbc.themes.MINTY])

model = EconomyModel()


app.layout = html.Div([
        html.Div([
                html.Div([
                    html.H1(['An Agent-Based Model of Household Inequality'],
                            style={'color': 'white'}),
                    html.P([
                        '''This is an economy model with heterogeneous agents
                        and monetary policy.''', html.Br(),
                        '''The model aims to explore and illustrate the ways in
                        which the rate policy of a central bank affects
                        household wealth and inequality.
                        '''
                    ]),
                ], style={
                    'flex': '2',
                    'color': 'white'
                }),

                html.Img(src=r'assets/bongo-cat-transparent.png',
                         alt='image',
                         style={'width': '12%'}),
            ],
                style={
                    'backgroundColor': 'rgba(243,150,154,255)',
                    # 'rgb(252, 248, 227)',
                    'padding': '10px 15px',
                    'width': '100%',
                    'top': '0px',
                    'display': 'flex',
                }),

        html.Div([
            dbc.Tabs(
                [
                    dbc.Tab(label="Simulation", tab_id="Simulation"),
                    dbc.Tab(label="Theory", tab_id="Theory"),
                ],
                id="tabs",
                active_tab="Simulation",
            ),
            html.Div(id="content"),
            ]),
        ])


@app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "Simulation":
        return html.Div([
            html.Div([
                html.Div([
                    html.H4('Adjustable parameters', className='text-dark-emphasis'),
                    html.Label("Number of agents"),
                    dbc.Input(id='number_of_agents',
                         value=1000,
                         placeholder='1000',
                         type='number'),

                    html.Label("Baseline interest rate"),
                    dbc.Input(id='baseline_interest_rate',
                        value=0,
                        placeholder='0',
                        type='number'),

                    html.Label("Intensity of Central Bank policy"),
                    dbc.Input(id='intensity_of_central_bank_policy',
                        value=0.8,
                        placeholder='0.8',
                        type='number'),

                    html.Label("Central Bank target rate"),
                    dbc.Input(id='central_bank_target_rate',
                        value=0.04,
                        placeholder='0.04',
                        type='number'),

                    html.Label("Trust of agents to central bank"),
                    dbc.Input(id='trust_of_agents_to_central_bank',
                        value=0.8,
                        placeholder='0.8',
                        type='number'),
                ], style={
                        'marginRight': '20px',
                        'flex': '1',
                        },
                    className='text-dark'),
                html.Div([
                    html.H4("Fixed parameters", className='text-dark-emphasis'),
                    dbc.Accordion([
                        dbc.AccordionItem([
                            dbc.Table(
                            # using the same table as in the above example
                                table_header + table_body,
                                id="table-color",
                            # color="info",
                                style={'border-radius': '10px'},
                                className='text-dark'
                            ),
                        ], title="View",)
                    ], start_collapsed=True)
                    ],
                    style={
                        'flex': '2',
                        'marginLeft': '20px',
                    },
                    className='text-dark'
                ),
            ],
                style={
                    'display': 'flex',
                    'marginTop': '20px',
                    }),

            html.Div([
                dbc.Button('Start', id='start-stop-button', n_clicks=0,
                     style={
                            'border-radius': '20px',
                            'display': 'inline-block',
                            'height': '100px',
                            'border-top-right-radius': '0px',
                            'border-bottom-right-radius': '0px',
                                },
                     color='primary',
                     className='col-md-3 offset-md-3'),
                dbc.Button('Reset', id='reset-button', n_clicks=0,
                     style={
                            'border-radius': '20px',
                            'display': 'inline-block',
                            'height': '100px',
                            'border-top-left-radius': '0px',
                            'border-bottom-left-radius': '0px',
                                },
                     color='danger',
                     className='col-md-3')],
                     className="row mx-auto",
                     style={
                        'marginTop': '40px',
                        'marginBottom': '40px',
                        }
            ),

            html.Div([
                    html.Label("Step per second", className='text-dark'),
                    dcc.Slider(1, 10, 1,
                            value=1,
                            id='sps-slider'),
                ],
                    className="d-grid gap-2 col-9 mx-auto",),

            html.Div([
                html.Div(
                    dcc.Graph(
                        id='gini-graph',
                        figure=blank_fig(
                            title='Gini',
                            xaxis_title='Step'
                            )
                        ),
                    style={'width': '48%', 'flex': '1'}
                ),

                html.Div(
                    dcc.Graph(id='cb-rate-graph',
                            figure=blank_fig(
                                title='CB Rate',
                                xaxis_title='Step')
                            ),
                    style={'width': '48%', 'flex': '1'}
                ),
            ],
                style={
                    'display': 'flex'
                    }),

            html.Div([
                html.Div(
                    dcc.Graph(
                        id='output-demand-graph',
                        figure=blank_fig(
                            title='Output and demand',
                            xaxis_title='Step'
                            )
                        ),
                    style={'width': '48%', 'flex': '1'}
                ),

                html.Div(
                    dcc.Graph(id='inf-graph',
                            figure=blank_fig(
                                title='Inflation',
                                xaxis_title='Step')
                            ),
                    style={'width': '48%', 'flex': '1'}
                ),
            ],
                style={
                    'display': 'flex'
                    }),
            html.Div([
                html.Div(
                    dcc.Graph(id='price-graph',
                            figure=blank_fig(
                                title='Price',
                                xaxis_title='Step')
                            ),
                    style={'width': '48%', 'flex': '1'}
                ),
                html.Div(
                    dcc.Graph(id='u-graph',
                            figure=blank_fig(
                                title='Unemployment',
                                xaxis_title='Step')
                            ),
                    style={'width': '48%', 'flex': '1'}
                ),
            ], 
                style={
                    'display': 'flex'
                    }),
            dcc.Interval(
                    id='interval-component',
                    interval=1000,  # in milliseconds
                    n_intervals=0,
                    disabled=True,
            ),
        ],
            style={
                'paddingLeft': '30px',
                'paddingRight': '30px'
                }),

    elif at == "Theory":
        return html.Div([
            dbc.Row([
                dbc.Col(),
                dbc.Col(
                    dbc.CardImg(src=r'assets/flowchart.png',), width='6'
                ),
                dbc.Col()
            ], align='center'),
            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(
                            html.H4("Центральный банк"
                            ), style={'background': "rgba(255,120,80,255)", "color": "white"}
                        ),
                        dbc.CardBody([
                            html.Div([
                                dcc.Markdown(
                                    r'''

                                    Центральный банк устанавливает ключевую ставку каждый период согласно модифицированному правилу Тейлора:

                                    $$
                                    \rho (t) = \rho_0 + \phi_{\pi} [\pi^{ema} (t) - \pi^*]
                                    $$

                                    * $\rho_0$ - **Baseline interest rate** - базовая ставка, устанавливаемая ЦБ: минимальная разрешенная ставка по кредитам для коммерческих банков
                                    * $\phi_{\pi}$ - **Intensity of Central Bank policy** - "интенсивность" политики ЦБ (насколько сильно ЦБ таргетирует инфляцию)
                                    * $\pi^*$ - **Central Bank target rate** - целевой уровень инфляции, устанавливаемый ЦБ
                                    * $\pi^{ema} (t)$ - экспоненциальное скользящее среднее инфляции в текущий период:
                                    ''', mathjax=True
                                ),
                            ]),
                        ], className="card-text")
                    ], style={'flex': '2'}, color='danger', outline=True),
                ),
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(
                            html.H4("Коммерческий банк"
                            ), style={'background': "rgba(120,194,173,255)", "color": "white"}
                        ),
                        dbc.CardBody([
                            html.Div([
                                dcc.Markdown(
                                    r'''

                                    Агрегированный репрезентативный банк. Выдает кредиты и принимает депозиты. 
                                    Меняет свои ставки в зависимости от ключевой ставки ЦБ по следующим правилам:

                                    $$
                                    r_{loan} (t) = (1 + \mu_{loan}) \times \rho (t)
                                    $$
                                    $$
                                    r_{dep} (t) = (1 + \mu_{dep}) \times \rho (t)
                                    $$

                                    * $\mu_{loan}$ - **Lending rate mark-up**
                                    * $\mu_{dep}$ - **Deposit mark-down**
                                    ''', mathjax=True
                                ),
                            ]),
                        ], className="card-text")
                    ], style={'flex': '2'}, color='primary', outline=True),
                ),
            ]),
            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(
                            html.H4("Фирма"
                            ), style={'background': "rgba(243,150,154,255)", "color": "white"}
                        ),
                        dbc.CardBody([
                            html.Div([
                                dcc.Markdown(
                                    r'''

                                    Агрегированная репрезентативная фирма.

                                    1. Производит абстрактный гомогенный товар по правилу:
                                    $$
                                    Y(t) \leq D(t) \rightarrow Y(t+1) = Y(t) + min[\eta +(D(t)-Y(t)), u(t)]
                                    $$
                                    $$
                                    Y(t) > D(t) \rightarrow Y (t+1) = Y(t) + \eta^-(D(t)-Y(t))
                                    $$

                                    * $\eta^-$ - **Excess supply sensitivity**
                                    * $\eta^+ = \rho(t) \times \eta^-$ - **Excess demand sensitivity**

                                    2. Устанавливает цену:
                                    $$
                                    Y (t) \leq D (t) \rightarrow p(t+1) = p(t) \times (1+\hat{\pi}(t))(1+\nu_p \xi_i(t))
                                    $$
                                    $$
                                    Y(t) > D(t) \rightarrow p(t+1) = p(t) \times (1+\hat{\pi}(t))(1-\nu_p \xi_i(t))
                                    $$

                                    * $\hat{\pi}(t)$ - ожидаемая инфляция
                                    * $\nu_p$ - параметр адаптации цен
                                    * $\xi_i(t)$ - случайная величина $~Unif[0;1]$

                                    3. Выплачивает заработную плату:
                                    $$
                                    Y(t) \leq D(t) \rightarrow W(t+1) = W(t) \times \gamma \xi_i(t)(1-\\eta_+) (1-u(t))(1+\gamma\hat{\pi}(t))
                                    $$
                                    $$
                                    Y (t) > D (t) \rightarrow W(t+1)=W(t)\times \gamma \xi_i(t)(1 - \\eta_-)u(t)(1+\gamma \hat{\pi} (t))
                                    $$
                                    * $W(t)$ - базовая ставка заработной платы, которая для каждого агента умножается на его продуктивность
                                    * $\gamma$ - **Wage rigidity** - параметр "липкости" заработной платы
                                    * $u(t)$ - безработица в периоде $t$

                                    4. Нанимает и увольняет работников:
                                    $$
                                    Y (t) \leq D (t) \rightarrow N_{hire} = \frac{D(t)-Y(t)}{Y(t)} \times (1-u(t))
                                    $$
                                    $$
                                    Y (t) > D (t) \rightarrow N_{fire}= \frac{D(t)-Y(t)}{Y(t)} \times (1-u(t))
                                    $$
                                    ''', mathjax=True
                                ),
                            ]),
                        ], className="card-text")
                    ], style={'flex': '2'}, color='secondary', outline=True),
                ),
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(
                            html.H4("Домохозяйства"
                            ), style={'background': "rgba(255,206,103,255)", "color": "white"}
                        ),
                        dbc.CardBody([
                            html.Div([
                                dcc.Markdown(
                                    r'''
                                    Гетерогенные домохозяйства. Их количество N - регулируемый параметр модели. Каждое домохозяйство

                                    1. Планирует потребление 

                                    $$
                                    ptc = \sigma[(1+\alpha)(\hat{\pi}(t)- r_{dep} (t))]
                                    $$
                                    $$
                                    Z_i(t)=ptc \times \hat{W_i}(t) + k_i(t)
                                    $$

                                    * $\alpha$ - чувствительность к инфляциии изменению ставок на депозиты
                                    * $ptc$ - склонность к потреблению из дохода
                                    * $Z_i (t)$ - желаемый уровень потребления
                                    * $\hat{W_i}(t)$ - ожидаемая заработная плата в периоде t, формируется наивным способом: $\hat{W_i}(t) = W_i(t-1)$
                                    * $k_i(t)$ - случайная величина $~N(\mu_k,\sigma_k)$


                                    2. Получает заработную плату от фирмы: 

                                    $$
                                    W_i(t)=W(t)*A_i(t) 
                                    $$

                                    3. Совершает операции на кредитном рынке:

                                    Сберегает, если $Z_i(t)+I_i \leq B_i(t)$:
                                    $$
                                    Cred_i(t) = (Z_i(t)+I_i-B_i(t)) \times (1+r_{dep})
                                    $$

                                    Берет в долг, если $Z_i(t)+I_i > B_i(t)$:

                                    Нет ограничений ликвидности, если $Z_i(t)+I_i-B_i(t) <= ltv \times B_i(t)$:
                                    $$
                                    Cred_i(t) = (Z_i(t)+I_i-B_i(t)) \times (1+r_{loan})
                                    $$

                                    Есть ограничения ликвидности, если $Z_i(t)+I_i-B_i(t) > ltv \times B_i(t)$:
                                    - Домохозяйство решает не инвестировать $I_i=0$
                                    - Если $Z_i(t)-B_i(t) <= ltv \times B_i(t)$, то
                                    $$
                                    Cred_i(t) = (Z_i(t)-B_i(t)) \times (1+r_{loan})
                                    $$
                                    - Иначе, д/х все еще ограничено, тогда:
                                    $$
                                    Cred_i(t) = ltv \times B_i(t) \times (1+r_{loan})
                                    $$

                                    4. Инвестирует в свою продуктивность:
                                    $$
                                    A_i(t+1) = A_i(t) * (1 + \xi_i (t))
                                    $$

                                    * $\xi_i (t)$ - случайная величина с распределением, параметры которого зависят от того, инвестировало ли домохозяйство фиксированную сумму в этом периоде - $N (\mu_1, \sigma_1)$ или $N (\mu_2, \sigma_2)$

                                    5. Потребляет:

                                    Если д/х сберегает или не имеет ограничений ликвидности, то оно может позволить себе желаемое потребление:
                                    $$
                                    C_i(t) = Z_i(t)
                                    $$

                                    Иначе:
                                    $$
                                    C_i(t) = ltv * B_i(t)
                                    $$
                                    ''', mathjax=True
                                ),
                            ]),
                        ], className="card-text")
                    ], style={'flex': '2'}, color='warning', outline=True),
                ),
            ], style={'marginTop': '20px'}),
            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(
                            html.H4("Переменные модели"
                            ), style={'background': "rgba(108,195,213,255)", "color": "white"}
                        ),
                        dbc.CardBody([
                            html.Div([
                                dcc.Markdown(
                                    r'''
                                    Инфляция:
                                    $$
                                    \pi(t)=\frac{p(t)-p(t-1)}{p(t-1)}
                                    $$

                                    Инфляционные ожидания
                                    $$
                                    \hat{\pi}(t)=\tau \pi^* + (1-\tau) \pi^{ema}(t)
                                    $$

                                    Сглаженная инфляция:
                                    $$
                                    \pi^{ema} = \omega \pi(t) + (1-\omega) \pi^{ema}(t-1)
                                    $$

                                    Агрегированный спрос:
                                    $$
                                    D(t)=\Sigma_{i=1}^N C_i(t)
                                    $$

                                    Безработица:
                                    $$
                                    u(t)=u(t-1)+\frac{N_{fire}-N_{hire}}{N}
                                    $$

                                    * $\tau$ - уровень доверия агентов к ЦБ
                                    * $\omega$ - параметр "сглаживания" инфляции
                                    ''', mathjax=True
                                ),
                            ]),
                        ], className="card-text")
                    ], style={'flex': '2'}, color='info', outline=True),
                ),
            ], style={'marginTop': '20px'})
        ], style={'marginLeft': '20px',
                  'marginRight': '20px'}, className='text-dark')
    return html.P("Something went wrong...")


@app.callback(
    [Output('gini-graph', 'figure', allow_duplicate=True),
     Output('cb-rate-graph', 'figure', allow_duplicate=True),
     Output('output-demand-graph', 'figure', allow_duplicate=True),
     Output('inf-graph', 'figure', allow_duplicate=True),
     Output('price-graph', 'figure', allow_duplicate=True),
     Output('u-graph', 'figure', allow_duplicate=True)],
    [Input('interval-component', 'n_intervals')],
    prevent_initial_call=True,
)
def update_graphs_live(n_intervals):
    model.step()

    gini_fig = go.Figure()
    gini_fig.add_trace(go.Line(y=model.datacollector.model_vars['Gini']))
    gini_fig.update_layout(
        title='Gini',
        xaxis_title='Step'
        )

    cb_rate_fig = go.Figure()
    cb_rate_fig.add_trace(go.Line(y=model.datacollector.model_vars['CB Rate']))
    cb_rate_fig.update_layout(
        title='CB Rate',
        xaxis_title='Step'
        )

    output_demand_fig = go.Figure()
    output_demand_fig.add_trace(
        go.Line(y=model.datacollector.model_vars['Output'],
                name='Output')
        )
    output_demand_fig.add_trace(
        go.Line(y=model.datacollector.model_vars['Demand'],
                name='Demand')
        )
    output_demand_fig.update_layout(
        title='Output and demand',
        xaxis_title='Step'
        )
 
    inf_fig = go.Figure()
    inf_fig.add_trace(go.Line(y=model.datacollector.model_vars['Actual Inflation'],
                              name='Actual Inflation')
                      )
    inf_fig.add_trace(go.Line(y=model.datacollector.model_vars['Inflation EMA'],
                              name='Inflation EMA')
                      )
    inf_fig.add_trace(go.Line(y=model.datacollector.model_vars['Inflation Expectations'],
                              name='Inflation Expectations')
                      )
    inf_fig.update_layout(
        title='Inflation',
        xaxis_title='Step'
        )
    
    price_fig = go.Figure()
    price_fig.add_trace(go.Line(y=model.datacollector.model_vars['Price']))
    price_fig.update_layout(
        title='Price',
        xaxis_title='Step'
        )
    
    u_fig = go.Figure()
    u_fig.add_trace(go.Line(y=model.datacollector.model_vars['Unemployment']))
    u_fig.update_layout(
        title='Unemployment',
        xaxis_title='Step'
        )

    return gini_fig, cb_rate_fig, output_demand_fig, inf_fig, price_fig, u_fig


@app.callback(
    [Output('gini-graph', 'figure'),
     Output('cb-rate-graph', 'figure'),
     Output('output-demand-graph', 'figure'),
     Output('inf-graph', 'figure'),
     Output('price-graph', 'figure'),
     Output('u-graph', 'figure'),
     ],
    [Input('reset-button', 'n_clicks')],
    [State('number_of_agents', 'value'),
     State('baseline_interest_rate', 'value'),
     State('intensity_of_central_bank_policy', 'value'),
     State('central_bank_target_rate', 'value'),
     State('trust_of_agents_to_central_bank', 'value')
     ]
)
def callback_func_reset_interval(button_clicks, *args):
    global model
    model = EconomyModel(*args)
    return (blank_fig(title='Gini', xaxis_title='Step'),
            blank_fig(title='CB Rate', xaxis_title='Step'),
            blank_fig(title='Output and demand', xaxis_title='Step'),
            blank_fig(title='Inflation', xaxis_title='Step'),
            blank_fig(title='Price', xaxis_title='Step'),
            blank_fig(title='Unemployment', xaxis_title='Step')
            )


@app.callback(
    [Output('interval-component', 'disabled'),
     Output('start-stop-button', 'children'),
     Output('start-stop-button', 'color')],
    [Input('start-stop-button', 'n_clicks')],
    [State('interval-component', 'disabled')],
)
def callback_func_start_stop_interval(button_clicks, disabled_state):
    if button_clicks is not None and button_clicks > 0:
        return (not disabled_state,
                'Stop' if disabled_state else 'Start',
                'secondary' if disabled_state else 'primary')
    else:
        return disabled_state, 'Start', 'primary'


@app.callback(
    Output('interval-component', 'interval'),
    [Input('sps-slider', 'value')],
)
def interval_fps(value):
    return 1000 / value


seed = np.random.seed(0)

if __name__ == '__main__':
    app.run_server(debug=False, host='localhost')
