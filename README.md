# **Зависимость экономического неравенства среди домохозяйств от политики Центрального банка** <br/> Агентная модель

## Запуск симуляции

1. Склонировать репозиторий
 
```
git clone https://github.com/legaliza-bit/abm-project
```

2. Установить зависимости

```
pip install -r requirements.txt
```

3. Запустить симуляцию

```
python dashboard.py
```

<br/>

## Описание модели

![flowchart](https://github.com/legaliza-bit/abm-project/blob/main/assets/flowchart.png)

### **Центральный банк**
Центральный банк устанавливает ключевую ставку каждый период согласно модифицированному правилу Тейлора:

$$
\rho (t) = \rho_0 + \phi_{\pi} [\pi^{ema} (t) - \pi^*]
$$

* $\rho_0$ - **Baseline interest rate** - базовая ставка, устанавливаемая ЦБ: минимальная разрешенная ставка по кредитам для коммерческих банков
* $\phi_{\pi}$ - **Intensity of Central Bank policy** - "интенсивность" политики ЦБ (насколько сильно ЦБ таргетирует инфляцию)
* $\pi^*$ - **Central Bank target rate** - целевой уровень инфляции, устанавливаемый ЦБ
* $\pi^{ema} (t)$ - экспоненциальное скользящее среднее инфляции в текущий период:

<br/>

### **Коммерческий банк**

Агрегированный репрезентативный банк. Выдает кредиты и принимает депозиты. Меняет свои ставки в зависимости 
от ключевой ставки ЦБ по следующим правилам:

$$
r_{loan} (t) = (1 + \mu_{loan}) \times \rho (t)
$$

$$
r_{dep} (t) = (1 + \mu_{dep}) \times \rho (t)
$$

* $\mu_{loan}$ - **Lending rate mark-up**
* $\mu_{dep}$ - **Deposit mark-down**

<br/>

### **Фирма**
Агрегированная репрезентативная фирма.

1. Производит абстрактный гомогенный товар по правилу:

$$
Y(t) \leq D(t) \rightarrow Y(t+1) = Y(t) + min[\eta_+ (D(t)-Y(t)), u(t)]
$$

$$
Y(t) > D(t) \rightarrow Y (t+1) = Y(t) + \eta_-(D(t)-Y(t))
$$

* $\eta_-$ - **Excess supply sensitivity**
* $\eta_+ = \rho(t) \times \eta^-$ - **Excess demand sensitivity**

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
* $N_{hire/fire}$ - количество работников, которое фирма хочет нанять/уволить в периоде t

<br/>

### **Домохозяйства**

Гетерогенные домохозяйства. Их количество N - регулируемый параметр модели. Каждое домохозяйство

1. Планирует потребление 

$$
ptc = \sigma[(1+\alpha)(\hat{\pi}(t)- r_{dep} (t))]
$$

$$
Z_i(t)=ptc \times \hat{W_i}(t) + k_i(t)
$$

* $\alpha$ - чувствительность к инфляциии и изменению ставок на депозиты
* $ptc$ - склонность к потреблению из дохода
* $Z_i (t)$ - желаемый уровень потребления
* $\hat{W_i}(t)$ - ожидаемая заработная плата в периоде t, формируется наивным способом: $\hat{W_i}(t) = W_i(t-1)$
* $k_i(t)$ - случайная величина $~N(\mu_k,\sigma_k)$


2. Получает заработную плату от фирмы: 

$$
W_i(t)=W(t)*A_i(t) 
$$

3. Совершает операции на кредитном рынке:

- Сберегает, если $Z_i(t)+I_i \leq B_i(t)$: $Cred_i(t) = (Z_i(t)+I_i-B_i(t)) \times (1+r_{dep})$

- Берет в долг, если $Z_i(t)+I_i > B_i(t)$:

    - Нет ограничений ликвидности, если $Z_i(t)+I_i-B_i(t) \leq ltv \times B_i(t)$: $Cred_i(t) = (Z_i(t)+I_i-B_i(t)) \times (1+r_{loan})$

    - Есть ограничения ликвидности, если $Z_i(t)+I_i-B_i(t) > ltv \times B_i(t)$: домохозяйство решает не инвестировать, $I_i$=0
        - Если $Z_i(t)-B_i(t) \leq ltv \times B_i(t)$, то $Cred_i(t) = (Z_i(t)-B_i(t)) \times (1+r_{loan})$

        - Иначе, д/х все еще ограничено, тогда: $Cred_i(t) = ltv \times B_i(t) \times (1+r_{loan})$

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


<br/>

### **Переменные модели**

Инфляция:

$$
\pi(t)=\frac{p(t)-p(t-1)}{p(t-1)}
$$

Инфляционные ожидания

$$
\hat{\pi}(t)=\tau \pi^* + (1-\tau) \pi^{ema}(t)
$$

* $\tau$ - **Trust of agents to central bank** - уровень доверия агентов к ЦБ

Сглаженная инфляция:
$$\pi^{ema} = \omega \pi(t) + (1-\omega) \pi^{ema}(t-1)$$
* $\omega$ - **Exponential MA Parameter** - параметр "сглаживания" инфляции

Агрегированный спрос:

$$
D(t)=\Sigma_{i=1}^N C_i(t)
$$

Безработица:

$$
u(t)=u(t-1)+\frac{N_{fire}-N_{hire}}{N}
$$


## Источники:
1. [Jean-Philippe Bouchaud, Stanislao Gualdi, Marco Tarzia, and Francesco Zamponi (2017). Optimal inflation target: insights from an agent-based model. Economics Discussion Papers, No 2017-64, Kiel Institute for the World Economy.](https://arxiv.org/abs/1709.05117)
2. [Stanislao Gualdi, Marco Tarzia, Francesco Zamponi, Jean-Philippe Bouchaud, Tipping points in macroeconomic agent-based models, Journal of Economic Dynamics and Control, Volume 50, 2015,Pages 29-61](https://arxiv.org/abs/1307.5319)
3. [Palagi, Elisa and Napoletano, Mauro and Roventini, Andrea and Gaffard, Jean-Luc, An agent-based model of trickle-up growth and income inequality (June 23, 2021)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3873764)