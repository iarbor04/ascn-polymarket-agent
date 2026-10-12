# Polymarket AI-аналитик: ресёрч (12.10.2026)

Цель: ИИ-сотрудник на ASCN, который анализирует рынки Polymarket и **не ставит сам**. Всё про API ниже проверено живыми запросами 12.10.2026.

## 1. Конкуренты

| Продукт | Что делает | Ключевые фичи | Цена | Аудитория |
|---|---|---|---|---|
| **Polymarket/agents** (github.com/polymarket/agents) | Открытый Python-фреймворк для автономных агентов-трейдеров | RAG по новостям, Gamma-клиент, Chroma, CLI, LLM-подсказки по сделкам; нужен приватный ключ кошелька | MIT, бесплатно | Разработчики |
| **Polysights** (app.polysights.xyz) | ИИ-аналитика рынков | ИИ-сводка «что было за 24 ч» (кто покупал/продавал), 30+ метрик, дашборды, поиск инсайдеров (новые кошельки), арбитраж; бета ~v0.4, есть токен | Фримиум, прайс не опубликован | Активные трейдеры |
| **Hashdive → Unusual Predictions** (Unusual Whales) | Скринер «умных денег» Polymarket + Kalshi | Smart Score трейдера от −100 до 100, отслеживание до 50 кошельков в Pro | Pro, цена не ясна | Копи-трейдеры |
| **Polymarket Analytics** (polymarketanalytics.com) | Самая глубокая аналитика трейдеров | PnL, позиции, win rate кошельков, лидерборд, Polymarket+Kalshi вместе, обновление ~5 мин | Бесплатно/фримиум | Исследователи, арбитражёры |
| **PredictFolio** (predictfolio.com) | Портфель и трейдеры | PnL своего портфеля, лидерборды, сравнение с топами | Бесплатно | Розница |
| **PolyTrack** (polytrackhq.app) | Поиск прибыльных трейдеров | Кластеры кошельков одного владельца, алерты <30 с, вотчлисты | Бесплатно | Копи-трейдеры |
| **Betmoar** | Веб-терминал + Discord-бот (де-факто «официальный» бот серверов) | Поиск, новые рынки, держатели, **трекинг UMA-споров** (голоса, обсуждения) | Без подписки и наценки | Активные трейдеры, Discord |
| **Oddpool** | Кросс-венью Kalshi ↔ Polymarket | Мониторинг расхождений цен на одинаковых рынках, арбитраж | Free + Pro $30/мес | Арбитражёры |
| **Kreo / KreoPoly**, **PolyCop**, **PolyBot**, PolyGun | Telegram-боты исполнения и копи-трейдинга | Копирование кошельков, снайпинг, Polymarket + Kalshi (Kreo) | ~0,5% с сделки (Kreo) | Розница в TG |
| **PolyxBot, PolyIntel, Polymarket Insider Bot, Wincy** | TG-алерты | Киты/инсайдеры, топ-держатели рынка, алерты каждые 10 мин | Фримиум | Розница |
| **PolyAlertHub** | Алерты по правилам | Порог цены, всплеск объёма, конкретный трейдер; TG/email/браузер | Фримиум | Частичная занятость |
| **Olas Polystrat** (Pearl) | Автономный агент, торгует за пользователя | Self-custody Safe, гео/полит. рынки с закрытием за 4–5 дней, награды OLAS; заявлено 4200+ сделок (самоотчёт) | Бесплатно + награды | Крипто-нативные |
| **Nansen Prediction Markets API** | Ончейн-данные Polymarket | Скринер рынков (снимок без истории), PnL-лидерборд, топ-держатели, OHLCV, стакан, сделки адреса | Подписка Nansen | Аналитики, разработчики |
| **Kairos, PolyClaw (Chainstack), polyrust, MCP-серверы Polymarket** | Терминалы и фреймворки | Торговля из терминала/IDE-агента | Разное | Разработчики |

Каталоги: launchpoly.com/tools (100+ инструментов), github.com/aarora4/Awesome-Prediction-Market-Tools, github.com/sssobolevski/polymarket-bots, PANews «170+ tools».

**Что встречается чаще всего (= чего явно хотят пользователи):**

| Фича | Где есть | Частота |
|---|---|---|
| Трекинг китов / топ-трейдеров, лидерборд, PnL кошелька | Analytics, PredictFolio, PolyTrack, Hashdive, Nansen, Polysights | очень высокая |
| Алерты (цена, объём, кит зашёл) в Telegram/Discord | PolyTrack, PolyAlertHub, PolyxBot, PolyIntel, Betmoar | очень высокая |
| Копи-трейдинг | Kreo, PolyCop, PolyBot, Analytics (Polycycle) | высокая (но это исполнение — нам нельзя) |
| Сравнение с Kalshi / арбитраж | Oddpool, Analytics, Hashdive, Polysights | высокая |
| ИИ-сводка рынка / «почему двинулось» | Polysights, PolyxBot | средняя, растёт |
| Детектор инсайдеров (свежие кошельки, крупный вход перед новостью) | Polysights, PolyIntel | средняя |
| Риск резолюции / UMA-споры | Betmoar | **редко — пробел** |
| Портфель и PnL пользователя | PredictFolio, Analytics | средняя |

Пробел для нас: никто не делает **связку «разбор правил резолюции + сравнение с внешними коэффициентами + доходность к дате + ликвидность» в виде понятного отчёта человеческим языком**, без требования подключать кошелёк и без исполнения.

Источники: [launchpoly](https://launchpoly.com/blog/best-polymarket-analytics-tools), [kairos](https://kairos.trade/compare/polysights-review), [polymart Hashdive](https://polymart.app/hashdive), [Betmoar review](https://polymart.app/blog/betmoar-review), [xclsv arb tools](https://xclsvmedia.com/best-prediction-market-arbitrage-tools-2026-ahasignals-arbbets-oddpool/), [Kreo](https://polymarketacademy.com/guides/kreo-vs-polycop), [coincodecap TG bots](https://coincodecap.com/10-best-polymarket-telegram-bots), [Polystrat](https://www.digitaltoday.co.kr/vn/view/63463/ai-upends-crypto-prediction-markets-single-trade-returns-376-percent), [Nansen PM API](https://docs.nansen.ai/api/prediction-market), [PANews](https://panewslab.com/en/articles/4053e837-eec0-4606-b72b-7ad03ba01a83).

## 2. Чего хотят пользователи (боли и задачи)

Спрос: «polymarket» ~450k/мес US, «polymarket bot» 590/мес при CPC $9,7 — коммерческий интент высокий, но «bot» в основном = копи-трейдинг/исполнение.

1. **Найти недооценённые рынки** — где цена расходится с Kalshi, букмекерами, опросами, базовой частотой.
2. **Следить за китами и топ-трейдерами** — кто зашёл, на сколько, их PnL и точность; отличать умные деньги от одного шумного кошелька.
3. **Инсайдеры** — после скандалов (ставка на уход Мадуро, мартовские правила 2026 против инсайда, спуфинга и wash-trading) все ищут «свежий кошелёк + крупный вход».
4. **Риск резолюции — главная боль доверия.** Неоднозначные слова («allow» в рынке про Fort Knox, $3,5M), «UMA-кит» в рынке про минералы Украины, иск по рынку Strategy/BTC из-за «уточнения» правил задним числом. По одной выборке 43% споров — из-за двусмысленных формулировок. Залог на предложение ответа $750, спор решают держатели UMA.
5. **Алерты** — движение цены, объём, близость даты закрытия, предложение/спор резолюции.
6. **PnL портфеля** — реальная доходность с учётом комиссий, наград и rebate.
7. **Ликвидность/спред** — тонкие рынки, проскальзывание, невозможность выйти; тонкие рынки ещё и дольше резолвятся.
8. **Комиссии (с 30.03.2026 Fee Structure V2)**: taker-комиссия `C × rate × p × (1−p)`; rate: Crypto 0,07, Sports/Economics/Culture/Weather/Other 0,05, Politics/Finance/Tech/Mentions 0,04, Geopolitics 0. Мейкеры не платят и получают rebate 15–25%.
9. **Награды**: liquidity rewards за лимитки у середины (поля `rewardsMinSize`, `rewardsMaxSpread`), holding rewards ~4% годовых на отдельных долгих рынках (`holdingRewardsEnabled`).
10. **Гео-ограничения / США**: CFTC выдал amended order в ноябре 2025 (через QCEX/QCX LLC, DCM+DCO); US-биржа работает с дек. 2025, iOS-приложение без вейтлиста с мая 2026, Android на раскатке, веба для США нет; доступ ~40+ штатов, часть штатов судится (Миннесота SF4760). Комиссии US-биржи отдельные и менялись несколько раз. Данные противоречивы — агент должен говорить «проверьте у себя».

Источники: [UMA attack, The Block](https://www.theblock.co/post/348171/polymarket-says-governance-attack-by-uma-whale-to-hijack-a-bets-resolution-is-unprecedented), [8 disputes 2026](https://polyscope.pro/8-polymarket-resolution-disputes-that-rocked-trader-trust-in-2026/), [integrity rules](https://coinmarketcap.com/academy/article/polymarket-tightens-market-integrity-rules-amid-manipulation-concerns), [dispute docs](https://docs.polymarket.com/polymarket-learn/markets/dispute), [fees docs](https://docs.polymarket.com/trading/fees), [4% holding](https://www.cryptopolitan.com/polymarket-starts-paying-out-4-rewards/), [US access](https://predscope.com/guide/polymarket-us), [bettingusa](https://www.bettingusa.com/prediction-markets/reviews/polymarket/).

## 3. Публичные API Polymarket (без авторизации, только чтение)

Лимиты (на IP, окно 10 с, при превышении запросы **задерживаются**, а не отклоняются): Gamma общий 4000, `/markets` 300, `/events` 500, `/public-search` 350, `/tags` 200; Data v1 1000 (`/trades` 200, `/positions` 150), Data v2 800; CLOB 9000, `/book` и `/price` 1500, `/prices-history` 1000. [docs](https://docs.polymarket.com/quickstart/introduction/rate-limits)

### Gamma — `https://gamma-api.polymarket.com` (каталог рынков)
- `GET /markets?active=true&closed=false&order=volume24hr&ascending=false&limit=…` — фильтры `tag_id`, `end_date_max`, `end_date_min`, `liquidity_num_min`, `volume_num_min`, `slug`, `condition_ids`, `offset`.
- `GET /events?active=true&closed=false` — событие = группа рынков (`markets[]`, `tags`, `negRisk`, `openInterest`, `commentCount`).
- `GET /public-search?q=fed&limit_per_type=5&events_status=active` → `{events, pagination}` (также tags/profiles).
- `GET /tags`, `GET /comments`.
- **Поля рынка (проверено):** `question`, `slug`, `conditionId`, `questionID`, `clobTokenIds` (JSON-строка, [YES, NO]), `outcomes`, `outcomePrices` (JSON-строки), `bestBid`, `bestAsk`, `spread`, `lastTradePrice`, `oneDayPriceChange`, `volume24hr`, `volume1wk`, `volumeNum`, `liquidityNum`, `startDate`, `endDate`, `acceptingOrders`, `negRisk`, `feesEnabled`, `feeSchedule`, `takerBaseFee`, `rewardsMinSize`, `rewardsMaxSpread`, `holdingRewardsEnabled`, `orderMinSize`, `orderPriceMinTickSize`, `restricted`.
- **Резолюция:** `description` (полный текст правил — главное для анализа), `resolutionSource` (URL), `umaResolutionStatus` (`proposed`/`disputed`/`resolved`…), `umaResolutionStatuses`, `umaBond`, `umaReward`, `customLiveness`, `resolvedBy`.

### CLOB — `https://clob.polymarket.com` (цены и стакан, параметр — token_id)
- `GET /price?token_id=…&side=buy` → `{"price":"0.999"}`
- `GET /midpoint?token_id=…` → `{"mid":"0.9995"}`
- `GET /spread?token_id=…` → `{"spread":"0.001"}`
- `GET /book?token_id=…` → `{market, asset_id, timestamp, hash, bids:[{price,size}], asks:[…]}` (+ tick/min size)
- `GET /prices-history?market=<token_id>&interval=1h|6h|1d|1w|1m|max&fidelity=<мин>` (или `startTs`/`endTs`) → `{"history":[{"t":unix,"p":0.675}]}`

### Data — `https://data-api.polymarket.com` (кошельки, сделки, держатели)
v1 (рабочий, проверено):
- `GET /positions?user=0x…&sortBy=CASHPNL&limit=…` → `size`, `avgPrice`, `initialValue`, `currentValue`, `cashPnl`, `percentPnl`, `realizedPnl`, `curPrice`, `redeemable`, `title`, `slug`, `eventSlug`, `outcome`, `endDate`.
- `GET /closed-positions?user=…` → `avgPrice`, `totalBought`, `realizedPnl`, `curPrice`, `title`.
- `GET /value?user=…` → `[{user, value}]`.
- `GET /activity?user=…` → `type`, `side`, `size`, `usdcSize`, `price`, `outcome`, `timestamp`, `transactionHash`, `title`.
- `GET /trades?market=<conditionId>|user=…&limit=…` → `proxyWallet`, `side`, `size`, `price`, `outcome`, `timestamp`, `name`, `pseudonym`.
- `GET /holders?market=<conditionId>&limit=…` → `[{token, holders:[{proxyWallet, amount, outcomeIndex, name, pseudonym}]}]`.
- `GET /v1/leaderboard?timePeriod=DAY|WEEK|MONTH|ALL&orderBy=PNL|VOL&limit=…` → `rank`, `proxyWallet`, `userName`, `xUsername`, `vol`, `pnl`.

**v2 (новый, OpenAPI: `/v2/openapi.json`, ответы `{data, pagination{next_cursor}}`, snake_case):**
- `/v2/leaderboard?time_period=week&sort_by=PNL&category=…` → `rank`, `user_id`, `pnl`, `volume`, `user_name`
- `/v2/user-stats?user=…` → `trades`, `biggest_win`, `join_date`, `all_time_pnl{realized_market_pnl, unrealized_pnl, maker_rebate, reward_income, …}`
- `/v2/user-pnl?user=…&interval=1m&fidelity=1d` → ряд `points[]` для графика PnL
- `/v2/resolutions?condition=…` → `status`, `was_disputed`, `extended_review`, `proposed_price`, `transaction_hash` — **готовый источник статуса UMA**
- `/v2/oi?condition=…` (открытый интерес), `/v2/biggest-winners?time_period=week`, `/v2/holders?condition=…&include_pnl=true`, `/v2/trades?…&filter_type=CASH&filter_amount=…` (фильтр крупных сделок = киты), `/v2/positions`, `/v2/activity`, `/v2/prices-history`, `/v2/value`, `/v2/status`.

**Рецепты:** топ-трейдеры → `/v2/leaderboard`; кошелёк → `/positions` + `/value` + `/v2/user-stats` + `/v2/user-pnl`; киты в рынке → `/v2/holders?include_pnl=true` + `/v2/trades` с фильтром суммы; связь Gamma↔CLOB: `clobTokenIds[0]` = YES-токен, `conditionId` = ключ для Data API.

## 4. Методы анализа серьёзных трейдеров

1. **Базовые частоты (outside view)**: сначала «как часто такое случалось» (переизбрание действующих, срыв дедлайнов законов, ставка ФРС при данных CME FedWatch), потом корректировка на специфику.
2. **Сверка с внешними ценами**: Kalshi, букмекеры (снять маржу: нормировать implied-вероятности до 100%), агрегаторы опросов, CME FedWatch, Metaculus/Manifold. Расхождение >3–5 п.п. при сопоставимых правилах — сигнал, но сначала проверить, что **правила совпадают** (дата, источник, формулировка).
3. **Доходность к дате**: покупка по p → прибыль (1−p)/p; годовая ≈ ((1/p)^(365/дни) − 1). 0,95 за 30 дней ≈ 86% годовых, но 0,95 за 300 дней ≈ 6% — хуже 4% holding rewards с учётом риска. Учитывать taker-комиссию `rate·p·(1−p)` и замороженный капитал при спорах.
4. **Ликвидность**: спред (`bestAsk−bestBid`), глубина стакана в пределах 1–2 центов, `liquidityNum`, `volume24hr`; считать цену исполнения для конкретной суммы по `/book`. Мид в тонком рынке — не вероятность.
5. **Чтение правил**: `description` + `resolutionSource` построчно — что именно считается событием, часовой пояс и точное время, «объявлено» vs «произошло», что при отмене/переносе, кто источник истины; оценить шанс спора; проверить `umaResolutionStatus` и `/v2/resolutions` (`was_disputed`).
6. **Калибровка**: вести журнал прогнозов, Brier score, проверять, что события «70%» сбываются ~70%. Агент может хранить свои оценки и считать свою калибровку.
7. **Kelly — только как обучение**: f* = (q − p)/(1 − p) для покупки YES по цене p при своей оценке q; на практике ¼–½ Kelly из-за ошибки оценки. Не персональная рекомендация.
8. **Ловушки**: двусмысленные правила; тонкая ликвидность и «стенки» в стакане (спуфинг); один кит двигает цену без информации (проверить его историю PnL); wash-trading объёма; негативный риск в `negRisk`-событиях с многими исходами (сумма YES ≠ 1 → смотреть всё событие); рынки, сильно зависящие от одного источника; крипто-рынки с макс. комиссией 0,07.

Источники методов: [Polymarket docs fees](https://docs.polymarket.com/trading/fees), [resolution guide](https://poly-sim.com/wiki/polymarket-resolution-explained.html), [murmurations on resolution](https://murmurationstwo.substack.com/p/polymarket-needs-to-completely-overhaul), стандартная литература по прогнозированию (Tetlock «Superforecasting»: base rates, Brier).

## 5. Kalshi — публичное чтение без ключа

- Базовый URL: `https://external-api.kalshi.com/trade-api/v2` (документация); `https://api.elections.kalshi.com/trade-api/v2` тоже отвечает (проверено, оба 200).
- `GET /markets?status=open&limit=…&series_ticker=…&event_ticker=…&cursor=…&mve_filter=exclude` (исключить мульти-ивент комбо-рынки, иначе первыми идут парлеи).
- `GET /events?…`, `GET /events/{event_ticker}`, `GET /series/{series_ticker}`, `GET /markets/{ticker}/orderbook`.
- **Поля рынка (проверено):** `ticker`, `event_ticker`, `title`, `yes_sub_title`, `status`, `close_time`, `expected_expiration_time`, `yes_bid_dollars`, `yes_ask_dollars`, `no_bid_dollars`, `no_ask_dollars`, `last_price_dollars`, `previous_price_dollars`, `volume_24h_fp`, `volume_fp`, `open_interest_fp`, `rules_primary`, `rules_secondary`, `result`, `market_type`. Цены — строки в долларах (0–1).
- Сопоставление с Polymarket — по тексту/дате (общего ID нет); сравнивать `rules_primary` с `description` Polymarket перед выводом об арбитраже.

[Kalshi docs](https://docs.kalshi.com/getting_started/quick_start_market_data)

## Выводы для продукта

- Позиционирование: **«аналитик, а не бот»** — разбор рынка, правил, китов и доходности; никакого кошелька и исполнения → нет риска взлома (как у Polycule в январе 2026) и меньше регуляторного риска.
- MVP-сценарии: (1) разбор рынка по ссылке: цена, спред/глубина, доходность к дате, правила и риск спора, Kalshi/внешние коэффициенты, киты; (2) скан «недооценённых» по категории; (3) разбор кошелька/топ-трейдеров; (4) регулярный дайджест + алерты по вотчлисту; (5) отчёт .md.
- Всё нужное доступно бесплатно без ключей: Gamma + CLOB + Data (v1/v2) + Kalshi.
