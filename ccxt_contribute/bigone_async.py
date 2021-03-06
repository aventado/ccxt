# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async.base.exchange import Exchange
import base64
import hashlib
import math
import json
import time
import datetime
import jwt
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import NotSupported
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.errors import InvalidNonce
from ccxt.base.errors import PermissionDenied
from ccxt.base.decimal_to_precision import ROUND
from ccxt.base.decimal_to_precision import TRUNCATE
from ccxt.base.decimal_to_precision import SIGNIFICANT_DIGITS


class bigone (Exchange):

    def describe(self):
        return self.deep_extend(super(bigone, self).describe(), {
            'id': 'bigone',
            'name': 'Bigone',
            'countries': 'NA',
            'version': 'v1',
            'rateLimit': 10,
            # new metainfo interface
            'has': {
                'CORS': False,
                'createDepositAddress': False,
                'deposit': False,
                'fetchClosedOrders': True,
                'fetchDepositAddress': False,
                'fetchTradingFees': False,
                'fetchFundingFees': False,
                'fetchMyTrades': True,
                'fetchOHLCV': False,
                'fetchOpenOrders': False,
                'fetchOrder': True,
                'fetchTickers': True,
                'withdraw': False,
            },
            'timeframes': {
                '1m': '1m',
                '5m': '5m',
                '15m': '15m',
                '30m': '30m',
                '1h': '1h',
                '3h': '3h',
                '6h': '6h',
                '12h': '12h',
                '1d': '1D',
                '1w': '7D',
                '2w': '14D',
                '1M': '1M',
            },
            'urls': {
                'logo': 'http://www.bigone.com.my/wp-content/uploads/2017/05/logo-2017.png',
                'api': 'https://b1.run/api/v2',
                'www': 'https://b1.run',
                'doc': [
                    'https://open.big.one/docs/api.html',
                ],
            },
            'api': {
                'public': {
                    'get': [
                        'ping',
                        'tickers',
                        'markets/{id}/ticker',
                        'markets/{id}/depth',
                        'markets/{id}/trades',
                        'markets',
                    ],
                },
                'private': {
                    'get': [
                        'viewer/accounts',
                        'viewer/orders',
                        'viewer/trades',
                        'viewer/orders/{id}',
                        'viewer/withdrawals',
                        'viewer/deposits'
                    ],
                    'post': [
                        'viewer/orders',
                        'viewer/orders/{id}/cancel',
                        'viewer/orders/cancel_all',
                    ],
                },
            },
            'fees': {
            },
            'commonCurrencies': {
                'BCC': 'CST_BCC',
                'BCU': 'CST_BCU',
                'DAT': 'DATA',
                'DSH': 'DASH',  # Bitfinex names Dash as DSH, instead of DASH
                'IOS': 'IOST',
                'IOT': 'IOTA',
                'MNA': 'MANA',
                'QSH': 'QASH',
                'QTM': 'QTUM',
                'SNG': 'SNGLS',
                'SPK': 'SPANK',
                'STJ': 'STORJ',
                'YYW': 'YOYOW',
                'USD': 'USDT',
            },
            'exceptions': {
                '10001': ExchangeError,
                '10002': ExchangeError,
                '10003': ExchangeError,
                '10004': ExchangeError,
                '10005': ExchangeError,
                '10006': ExchangeError,
                '10007': ExchangeError,
                '10008': AuthenticationError,
                '10009': ExchangeError,
                '10010': ExchangeError,
                '10011': ExchangeError,
                '10012': ExchangeError,
                '10013': ExchangeError,
                '10014': AuthenticationError,
                '10015': AuthenticationError,
                '10016': AuthenticationError,
                '10017': ExchangeError,
                '10018': ExchangeError,
                '10019': AuthenticationError,
                '10022': ExchangeError,
                '10023': AuthenticationError,
                '10024': ExchangeError,
                '10025': ExchangeError,
                '10026': ExchangeError,
                '10026': ExchangeError,
                '10027': ExchangeError,
                '10028': ExchangeError,
                '30000': ExchangeError,
                '30001': ExchangeError,
                '30002': ExchangeError,
                '30003': ExchangeError,
                '30004': InsufficientFunds,
                '30005': PermissionDenied,
                '30006': ExchangeError,
                '30007': ExchangeError,
                '30008': ExchangeError,
                '30009': ExchangeError,
                '40001': ExchangeError,
                '40002': ExchangeError,
                '40003': ExchangeError,
                '40004': ExchangeError,
                '40000': ExchangeError,
            },
            'precisionMode': SIGNIFICANT_DIGITS,
        })


    async def fetch_markets(self):
        markets = await self.publicGetMarkets()
        result = []
        for market in markets["data"]:
            id = market['uuid']
            baseId = market['baseAsset']['symbol']
            quoteId = market['quoteAsset']['symbol']
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = base + '/' + quote
            precision = {
                'base': market['baseScale'],
                'quote': market['quoteScale'],
                'amount': market['baseScale'],
                'price': market['quoteScale'],
            }

            limits = {
                'amount': {
                    'min': math.pow(10, -precision['amount']),
                    'max': None,
                },
                'price': {
                    'min': math.pow(10, -precision['price']),
                    'max': None,
                },

            }

            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': True,
                'precision': precision,
                'limits': limits,
                'info': market,
            })
        return result

    def cost_to_precision(self, symbol, cost):
        return self.decimal_to_precision(cost, ROUND, self.markets[symbol]['precision']['price'], self.precisionMode)

    def price_to_precision(self, symbol, price):
        return self.decimal_to_precision(price, ROUND, self.markets[symbol]['precision']['price'], self.precisionMode)

    def amount_to_precision(self, symbol, amount):
        return self.decimal_to_precision(amount, TRUNCATE, self.markets[symbol]['precision']['amount'], self.precisionMode)

    def fee_to_precision(self, currency, fee):
        return self.decimal_to_precision(fee, ROUND, self.currencies[currency]['precision'], self.precisionMode)

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        request = {}

        if symbol:
            await self.load_markets()
            market = self.market(symbol)
            request["market_id"] = market["id"]

        response = await self.privateGetViewerTrades(self.extend(request, params))

        result = self.safe_value(response["data"],"edges",[])

        return self.parse_trades(result, market, since, limit)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privateGetViewerAccounts(params)

        result = {'info': response}
        balances = response['data']
        for balance in balances:
            currency = balance['asset_id']
            if currency in self.currencies_by_id:
                currency = self.currencies_by_id[currency]['code']
            account = {
                'free': 0.0,
                'used': float(balance['locked_balance']),
                'total': float(balance['balance']),
            }
            account['free'] = account['total'] - account['used']
            result[currency] = account
        return self.parse_balance(result)

    async def cancel_order(self, id, symbol=None, params={}):
        if symbol is not None:
            print("symbol param is not supported in bigone!")

        response = await self.privatePostViewerOrdersIdCancel(self.extend({
            'id': int(id),
        }, params))
        return response

    async def cancel_all_order(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)

        response = await self.privatePostViewerOrdersCancelAll(self.extend({
            "market_id":market["id"],
        }, params))
        return response

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        method = 'privatePostViewerOrders'

        if type is not None:
            print("type param is not supported in bigone!")

        order = {
            'market_id': market['id'],
            'price': self.price_to_precision(symbol, price),
            'amount': self.amount_to_string(symbol, amount),
            'side': self.parse_order_side(side.upper()),
        }

        response = await getattr(self, method)(self.extend(order, params))
        return self.parse_order(response["data"])

    async def fetch_order(self, order_id, symbol=None, params={}):
        if symbol is not None:
            print("symbol param is not supported in bigone!")
        await self.load_markets()
        market = self.markets[symbol] if symbol else None
        request = {
            'id': int(order_id),
            'order_id': int(order_id),
        }

        response = await self.privateGetViewerOrdersId(self.extend(request, params))
        return self.parse_order(response["data"], market)

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        if not symbol:
            raise ExchangeError(self.id + ' fetchClosedOrders requires a symbol param')
        orders = await self.fetch_orders(symbol, since, limit, params)
        return self.filter_by(orders, 'status', 'closed')

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        if not symbol:
            raise ExchangeError(self.id + ' fetchOpenOrders requires a symbol param')
        orders = await self.fetch_orders(symbol, since, limit, params)
        return self.filter_by(orders, 'status', 'open')

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        if not symbol:
            raise ExchangeError(self.id + ' fetchOrders requires a symbol param')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market_id': market['id'],
        }

        response = await self.privateGetViewerOrders(self.extend(request, params))

        result = self.safe_value(response["data"],"edges",[])

        return self.parse_orders(result, market, since, limit)

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'id': market['id'],
        }

        response = await self.publicGetMarketsIdTrades(self.extend(request, params))

        result = self.safe_value(response["data"],"edges",[])

        return self.parse_trades(result, market, since, limit)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'id': market['id'],
        }
        if limit is not None:
            # request['limit'] = limit  # default = maximum = 100
            print("limit param is not supported in bigone!")

        response = await self.publicGetMarketsIdDepth(self.extend(request, params))
        orderbook = self.parse_order_book(response["data"],price_key="price", amount_key="amount")
        return orderbook

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        rawTickers = await self.publicGetTickers(params)
        return self.parse_tickers(rawTickers['data'], symbols)

    def parse_tickers(self, rawTickers, symbols=None):
        tickers = []
        for ticker in rawTickers:
            tickers.append(self.parse_ticker(ticker))

        return self.filter_by_array(tickers, 'symbol', symbols)

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        response = await self.publicGetMarketsIdTicker(self.extend({
            'id': market['id'],
        }, params))

        return self.parse_ticker(response["data"], market)

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        iso8601 = None if (timestamp is None) else self.iso8601(timestamp)
        symbol = self.find_symbol(self.safe_string(ticker, 'market_uuid'), market)
        last = self.safe_float(ticker, 'close')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': iso8601,
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker['bid'], 'price'),
            'bidVolume': self.safe_float(ticker['bid'], 'amount'),
            'ask': self.safe_float(ticker['ask'], 'price'),
            'askVolume': self.safe_float(ticker['ask'], 'amount'),
            'vwap': self.safe_float(ticker, 'weightedAvgPrice'),
            'open': self.safe_float(ticker, 'open'),
            'close': last,
            'last': last,
            'previousClose': self.safe_float(ticker, 'prevClosePrice'),  # previous day close
            'change': self.safe_float(ticker, 'daily_change'),
            'percentage': self.safe_float(ticker, 'daily_change_perc'),
            'average': None,
            'baseVolume': self.safe_float(ticker, 'volume'),
            'quoteVolume': self.safe_float(ticker, 'quoteVolume'),
            'info': ticker,
        }

    def parse_trade(self, trade, market=None):
        if 'node' in trade:
            trade = trade['node']
        _datetime = trade['inserted_at']
        timestamp = self.iso8601_to_timestamp(_datetime)
        timestamp = int(timestamp*1000)
        priceField = 'p' if ('p' in list(trade.keys())) else 'price'
        price = float(trade[priceField])
        amountField = 'amount'
        amount = float(trade[amountField])
        idField = 'a' if ('a' in list(trade.keys())) else 'id'
        id = str(trade[idField])
        side = 'buy' if trade['taker_side'] is 'BID' else 'sell'
        order = None
        if 'orderId' in trade:
            order = str(trade['orderId'])

        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': _datetime,
            'symbol': market['symbol'],
            'id': id,
            'order': order,
            'type': None,
            'takerOrMaker': None,
            'side': side,
            'price': price,
            'cost': price * amount,
            'amount': amount,
            'fee': None,
        }

    def parse_order_status(self, status):
        statuses = {
            'PENDING': 'open',
            'FILLED': 'closed',
            'CANCELED': 'canceled',
        }
        return statuses[status] if (status in list(statuses.keys())) else status.lower()

    def parse_order_side(self, side):
        sides = {
            'SELL': 'ASK',
            'BUY': 'BID',
        }
        return sides[side] if (side in list(sides.keys())) else side.upper()

    def parse_order(self, order, market=None):
        if "node" in order:
            order = order["node"]
        status = self.safe_value(order, 'state')
        if status is not None:
            status = self.parse_order_status(status)
        symbol = self.find_symbol(self.safe_string(order, 'market_uuid'), market)

        iso8601 = self.safe_value(order, 'inserted_at')
        timestamp = self.iso8601_to_timestamp(iso8601)
        last_trade_timestamp = self.safe_value(order, 'updated_at')

        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'amount')
        filled = self.safe_float(order, 'filled_amount', 0.0)
        remaining = None
        cost = None
        if filled is not None:
            if amount is not None:
                remaining = max(amount - filled, 0.0)
            if price is not None:
                cost = price * filled
        id = self.safe_string(order, 'id')
        type = self.safe_string(order, 'type')
        if type is not None:
            type = type.lower()
        side = self.safe_string(order, 'side')
        if side is not None:
            side = side.lower()
            side = "buy" if side is "BID" else "sell"

        result = {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': iso8601,
            'lastTradeTimestamp': last_trade_timestamp,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': None,
        }
        return result

    def nonce(self):
        return int(time.time()*10**9)

    def iso8601_to_timestamp(self,iso8601):
        if len(iso8601)>20:
            iso8601 = iso8601[:19] + "Z"
        timestamp = (datetime.datetime.strptime(iso8601, "%Y-%m-%dT%H:%M:%SZ") - datetime.datetime(1970,1,1)).total_seconds()
        return int(timestamp*1000)

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        headers = {
            'Content-Type': 'application/json',
        }
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            if method == 'GET':
                if query:
                    url += '?' + self.urlencode(query)
            elif query:
                body = self.json(query)
            nonce = self.nonce()

            payload = {
                "type": "OpenAPI",
                "sub": self.apiKey,
                "nonce": nonce
            }
            signature = jwt.encode(payload, self.secret, algorithm='HS256')
            headers['Authorization'] = "Bearer " + signature.decode()

        url = self.urls['api'] + url
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
    
    def handle_errors(self, code, reason, url, method, headers, body):
        response = json.loads(body)
        if (code == 418) or (code == 429):
            raise DDoSProtection(self.id + ' ' + str(code) + ' ' + reason + ' ' + body)

        if "errors" in response:
            errors = self.safe_value(response, 'errors')

            for error in errors:    
                error_code = self.safe_string(error, "code")
                error_msg = self.safe_string(error, "message")
                
                exceptions = self.exceptions
                if error_code in exceptions:
                    raise exceptions[error_code](error_msg)
                else:
                    raise ExchangeError(error_msg)
            