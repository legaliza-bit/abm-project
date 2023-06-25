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
    # fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    # fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)

    return fig


table_header = [
    html.Thead(html.Tr([html.Th("Description"), html.Th("Symbol"), html.Th("Value")]))
]

row1 = html.Tr([html.Td("Exp MA Parameter"), html.Td(dcc.Markdown("$\\omega$",mathjax=True)), html.Td("0.5")])
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
# for i in range(50):
#     model.step()

# Определение внешнего вида приложения dash
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
                    ],
                    style={
                            'marginRight': '20px',
                            'flex': '1',
                        },
                    className='text-dark'),

                html.Div(
                    [
                        html.H4("Fixed parameters", className='text-dark-emphasis'),
                        dbc.Table(
                            # using the same table as in the above example
                            table_header + table_body,
                            id="table-color",
                            # color="info",
                            style={
                                'border-radius': '10px',
                            },
                            className='text-dark'
                        ),
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
            dbc.Row([dbc.Col(),
                dbc.Col(
                    dbc.CardImg(src=r'assets/flowchart.png',
                                # className='align-self-center'
                                ),
                                width='6',
            ), dbc.Col()], align='center'),
            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(html.H4("Центральный банк"),
                                        style={'background': "rgba(255,120,80,255)",
                                               "color": "white"}),
                        dbc.CardBody([
                            html.Div([
                                dcc.Markdown(
                                        '''
                                        Центральный банк устанавливает ключевую ставку
                                        каждый период согласно модифицированному правилу 
                                        Тейлора:
                                        '''
                                    ),
                                dbc.Container([
                                    dbc.Row([
                                        dcc.Markdown(
                                            '''$$\\rho (t) = \\rho_0 + \\phi_{\\pi} [\\pi^{ema} (t) - \\pi^*]$$''',
                                            mathjax=True
                                        ),
                                    ], align="center", className=["h-50", 'text-dark'],
                                        style={'font-size': '16px'}
                                    )],
                                        ),
                                html.P(
                                    dcc.Markdown(
                                            '''
                                            * $\\rho_0$ - **Baseline interest rate** - базовая ставка,
                                            устанавливаемая ЦБ: минимальная разрешенная ставка по
                                            кредитам для коммерческих банков
                                            * $\\phi_{\\pi}$ - **Intensity of Central Bank policy** -
                                            "интенсивность" политики ЦБ (насколько сильно ЦБ
                                            таргетирует инфляцию)
                                            * $\\pi^*$ - **Central Bank target rate** - целевой
                                            уровень инфляции, устанавливаемый ЦБ
                                            * $\\pi^{ema} (t)$ - экспоненциальное скользящее среднее
                                            инфляции в текущий период:
                                            ''',
                                            mathjax=True
                                        ),
                                ),
                            ], className="card-text")
                        ],),], style={
                            'flex': '2'
                        }, color='danger', outline=True),
                ),
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(html.H4("Коммерческий банк"),
                                        style={'background': "rgba(120,194,173,255)",
                                               "color": "white"}),
                        dbc.CardBody([
                            html.Div([
                                html.P(
                                    dcc.Markdown(
                                            '''
                                            Агрегированный репрезентативный банк. Выдает кредиты и
                                            принимает депозиты. Меняет свои ставки в зависимости 
                                            от ключевой ставки ЦБ по следующим правилам:
                                            '''
                                        ),
                                ),
                                dbc.Container([
                                    dbc.Row([
                                        dcc.Markdown(
                                            '''$$r_{loan} (t) = (1 + \\mu_{loan}) \\times \\rho (t)$$''',
                                            mathjax=True
                                        ),
                                    ], align="center", className=["h-50", 'text-dark'],
                                        style={'font-size': '16px'}
                                        )],
                                    ),
                                dbc.Container([
                                    dbc.Row([
                                        dcc.Markdown(
                                            '''$$r_{dep} (t) = (1 + \\mu_{dep}) \\times \\rho (t)$$''',
                                            mathjax=True
                                        ),
                                    ], align="center", className=["h-50", 'text-dark'],
                                        style={'font-size': '16px'}
                                        )],
                                    ),
                                html.P(
                                    dcc.Markdown(
                                            '''
                                            * $\\mu_{loan}$ - **Lending rate mark-up**
                                            * $\\mu_{dep}$ - **Deposit mark-down**
                                            ''',
                                            mathjax=True
                                        ),
                            )], className="card-text")
                        ],),], style={
                            'flex': '2'
                        }, color='primary', outline=True),),
                        ], style={'marginTop': '20px'}),
            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(html.H4("Фирма"),
                                        style={'background': "rgba(243,150,154,255)",
                                               "color": "white"}),
                        dbc.CardBody([
                            html.Div([
                                html.P([
                                    '''
                                    Агрегированная репрезентативная фирма.
                                    ''',
                                    html.Br(),
                                    '''
                                    1. Производит абстрактный гомогенный товар по правилу:
                                    '''
                                    ]
                                ),
                                dbc.Container([
                                    dbc.Row([
                                        dcc.Markdown(
                                            '''$$Y (t) \leq D (t) \\rightarrow Y (t+1) = Y(t) + min[\\eta^+(D(t)-Y(t)), u(t))]$$''',
                                            mathjax=True
                                        ),
                                    ], align="center", className=["h-50", 'text-dark'],
                                        style={'font-size': '16px'}
                                        )],
                                    ),
                                dbc.Container([
                                    dbc.Row([
                                        dcc.Markdown(
                                            '''$$Y (t) > D (t) \\rightarrow Y (t+1) = Y(t) + \\eta^-(D(t)-Y(t))$$''',
                                            mathjax=True
                                        ),
                                    ], align="center", className=["h-50", 'text-dark'],
                                        style={'font-size': '16px'}
                                        )],
                                    ),
                                html.P(
                                    dcc.Markdown(
                                            '''
                                            * $\\eta^-$ - **Excess supply sensitivity**
                                            * $\\eta^+ = \\rho(t) \\times \\eta^-$ - 
                                            **Excess demand sensitivity**
                                            ''',
                                            mathjax=True
                                        ),
                                ),
                                html.P([
                                    '''
                                    2. Устанавливает цену:
                                    '''
                                    ]
                                ),
                                dbc.Container([
                                    dbc.Row([
                                        dcc.Markdown(
                                            '''$$Y (t) \leq D (t) \\rightarrow 
                                            p(t+1) = p(t) \\times (1+\\hat{\\pi}(t))
                                            (1+\\nu_p \\xi_i(t)) 
                                            $$''',
                                            mathjax=True
                                        ),
                                    ], align="center", className=["h-50", 'text-dark'],
                                        style={'font-size': '16px'}
                                        )],
                                    ),
                                dbc.Container([
                                    dbc.Row([
                                        dcc.Markdown(
                                            '''$$Y (t) > D (t) \\rightarrow
                                            p(t+1) = p(t) \\times (1+\\hat{\\pi}(t))
                                            (1-\\nu_p \\xi_i(t))
                                            $$''',
                                            mathjax=True
                                        ),
                                    ], align="center", className=["h-50", 'text-dark'],
                                        style={'font-size': '16px'}
                                        )],
                                    ),
                                html.P(
                                    dcc.Markdown(
                                            '''
                                            * $\\hat{\\pi}(t)$ - ожидаемая инфляция
                                            * $\\nu_p$ - параметр адаптации цен
                                            * $\\xi_i(t)$ - случайная величина 
                                            $~Unif[0;1]$
                                            ''',
                                            mathjax=True
                                        ),
                                ),
                                html.P([
                                    '''
                                    3. Выплачивает заработную плату:
                                    '''
                                    ]
                                ),
                                dbc.Container([
                                    dbc.Row([
                                        dcc.Markdown(
                                            '''$$Y (t) \leq D (t) \\rightarrow
                                            W_i (t+1) = W_i(t) \\times \\gamma 
                                            \\xi_i(t)
                                            (1-\\eta_+) (1-u(t))
                                            (1+\\gamma\\hat{\\pi}(t))$$''',
                                            mathjax=True
                                        ),
                                    ], align="center", className=["h-50", 'text-dark'],
                                        style={'font-size': '16px'}
                                        )],
                                    ),
                                dbc.Container([
                                    dbc.Row([
                                        dcc.Markdown(
                                            '''$$Y (t) > D (t) \\rightarrow W_i(t+1)=W_i(t)
                                            \\times \\gamma \\xi_i(t) (1 - \\eta_-) u(t)
                                            (1+\\gamma \\hat{\\pi} (t))$$''',
                                            mathjax=True
                                        ),
                                    ], align="center", className=["h-50", 'text-dark'],
                                        style={'font-size': '16px'}
                                        )],
                                    ),
                                html.P(
                                    dcc.Markdown(
                                            '''
                                            * $\\gamma$ - **Wage rigidity** - 
                                            параметр "липкости" заработной платы
                                            * $u(t)$ - безработица в периоде $t$
                                            ''',
                                            mathjax=True
                                        ),
                                ),
                                html.P([
                                    '''
                                    4. Нанимает и увольняет работников:
                                    '''
                                    ]
                                ),
                                dbc.Container([
                                    dbc.Row([
                                        dcc.Markdown(
                                            '''$$Y (t) \leq D (t) \\rightarrow 
                                            N_{hire} = \\eta_+ (D(t)-Y(t))\\times u(t)$$''',
                                            mathjax=True
                                        ),
                                    ], align="center", className=["h-50", 'text-dark'],
                                        style={'font-size': '16px'}
                                        )],
                                    ),
                                dbc.Container([
                                    dbc.Row([
                                        dcc.Markdown(
                                            '''$$Y (t) > D (t) \\rightarrow 
                                            N_{fire}=\\eta_- (D(t)-Y(t))\\times (1-u(t))$$''',
                                            mathjax=True
                                        ),
                                    ], align="center", className=["h-50", 'text-dark'],
                                        style={'font-size': '16px'}
                                        )],
                                    ),
                                html.P(
                                    dcc.Markdown(
                                            '''
                                            ''',
                                            mathjax=True
                                        ),
                                ),
                            ])], className="card-text")
                                    ], color='secondary', outline=True),
                                    ),
                                    dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(html.H4("Домохозяйства"),
                                        style={'background': "rgba(255,206,103,255)",
                                               "color": "white"}),
                        dbc.CardBody([
                            html.Div([
                                html.P([
                                    '''
                                    Гетерогенные домохозяйства. Их количество 
                                    N - регулируемый параметр модели. Каждое домохозяйство
                                    ''',
                                    html.Br(),
                                    '''
                                    1. Планирует потребление:
                                    '''
                                    ]
                                ),
                                dbc.Container([
                                    dbc.Row([
                                        dcc.Markdown(
                                            '''$$ptc = \\sigma[(1+\\alpha)(\\hat{\\pi}(t)-
                                            r_{dep} (t))]$$''',
                                            mathjax=True
                                        ),
                                    ], align="center", className=["h-50", 'text-dark'],
                                        style={'font-size': '16px'}
                                        )],
                                    ),
                                dbc.Container([
                                    dbc.Row([
                                        dcc.Markdown(
                                            '''$$Z_i(t)= ptc \\times W_i(t) +
                                            k_i(t)$$''',
                                            mathjax=True
                                        ),
                                    ], align="center", className=["h-50", 'text-dark'],
                                        style={'font-size': '16px'}
                                        )],
                                    ),
                                html.P(
                                    dcc.Markdown(
                                            '''
                                            * $\\alpha$ - чувствительность к инфляции
                                            и изменению ставок на депозиты
                                            * $ptc$ - склонность к потреблению из дохода
                                            * $Z_i (t)$ - желаемый уровень потребления
                                            * $k_i(t)$ - случайная величина $~N(\\mu_k,\\sigma_k)$
                                            ''',
                                            mathjax=True
                                        ),
                                ),
                            
                                html.P([
                                    '''
                                    2. Получает заработную плату:
                                    '''
                                    ]
                                ),
                                # dbc.Container([
                                #     dbc.Row([
                                #         dcc.Markdown(
                                #             '''$$Y (t) \leq D (t) \\rightarrow Y (t+1) = Y(t) + min[\\eta^+(D(t)-Y(t)), u(t))]$$''',
                                #             mathjax=True
                                #         ),
                                #     ], align="center", className=["h-50", 'text-dark'],
                                #         style={'font-size': '16px'}
                                #         )],
                                #     ),
                                # dbc.Container([
                                #     dbc.Row([
                                #         dcc.Markdown(
                                #             '$$Y (t) > D (t) \\rightarrow Y (t+1) = Y(t) + \\eta^-(D(t)-Y(t))$$',
                                #             mathjax=True
                                #         ),
                                #     ], align="center", className=["h-50", 'text-dark'],
                                #         style={'font-size': '16px'}
                                #         )],
                                #     ),
                                # html.P(
                                #     dcc.Markdown(
                                #             '''
                                #             * $\\eta^+$ - **Lending rate mark-up** - 
                                #             гиперпараметр, 
                                #             * $\\eta^-$ - **Deposit mark-down** -
                                #             ''',
                                #             mathjax=True
                                #         ),
                                # ),
                                html.P([
                                    '''
                                    3. Инвестирует в свою продуктивность:
                                    '''
                                    ]
                                ),
                                dbc.Container([
                                    dbc.Row([
                                        dcc.Markdown(
                                            '''$$A_i(t+1) = A_i(t) * (1 + \\xi_i (t))$$''',
                                            mathjax=True
                                        ),
                                    ], align="center", className=["h-50", 'text-dark'],
                                        style={'font-size': '16px'}
                                        )],
                                    ),
                                html.P(
                                    dcc.Markdown(
                                            '''
                                            * $\\xi_i (t)$ - случайная величина с распределением,
                                            параметры которого зависят от того,
                                            инвестировало ли домохозяйство фиксированную
                                            сумму в этом периоде - 
                                            $N (\\mu_1, \\sigma_1)$ или $N (\\mu_2, \\sigma_2)$ 
                                            ''',
                                            mathjax=True
                                        ),
                                ),
                                html.P([
                                    '''
                                    4. Совершает операции на кредитном рынке:
                                    '''
                                    ]
                                ),
                                dbc.Container([
                                    dbc.Row([
                                        dcc.Markdown('',
                                            mathjax=True
                                        ),
                                    ], align="center", className=["h-50", 'text-dark'],
                                        style={'font-size': '16px'}
                                        )],
                                    ),
                                html.P(
                                    dcc.Markdown(
                                            '''
                                            ''',
                                            mathjax=True
                                        ),
                                ),
                            ])], className="card-text")
                                    ], color='warning', outline=True),
                                    )], style={
                                        'marginTop': '20px',
                                    },),
                                ], style={'marginLeft': '20px',
                                        'marginRight': '20px'},
                                        className='text-dark'),
    return html.P("Something went wrong...")


@app.callback(
    [Output('gini-graph', 'figure', allow_duplicate=True),
     Output('cb-rate-graph', 'figure', allow_duplicate=True),
     Output('output-demand-graph', 'figure', allow_duplicate=True),
     Output('inf-graph', 'figure', allow_duplicate=True),
     Output('price-graph', 'figure', allow_duplicate=True)],
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

    return gini_fig, cb_rate_fig, output_demand_fig, inf_fig, price_fig


@app.callback(
    [Output('gini-graph', 'figure'),
     Output('cb-rate-graph', 'figure'),
     Output('output-demand-graph', 'figure'),
     Output('inf-graph', 'figure'),
     Output('price-graph', 'figure'),
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
            blank_fig(title='Price', xaxis_title='Step')
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
    app.run_server(debug=True, host='localhost')
