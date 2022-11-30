import requests
import pandas as pd
from io import StringIO
from time import sleep

from .exceptions import YdAPIError, YdAuthError
from .entities import (
    Ad,
    AdImage,
    AdExtension,
    AdGroup,
    Bid,
    AudienceTarget,
    AgencyClient,
    BidsModifier,
    Campaign,
    Change,
    Dictionary,
    DynamicTextAdTarget,
    KeywordBid,
    Keyword,
    Lead,
    NegativeKeywordSharedSet,
    Sitelink,
    KeywordsResearch,
    RetargetingList,
    VCard,
    TurboPage,
    Report,
    Client,
)


class YdResponseReport:

    def __init__(self, response: str) -> None:
        self._df = self._to_pandas(response)
        print('-----------------------------')
        print(self._df)
        print('-----------------------------')

    @staticmethod
    def _to_pandas(report_str: str) -> pd.DataFrame:
        # data_rows = []
        df = pd.read_csv(StringIO(report_str), sep='\t', header=1,
                         dtype=str).iloc[:-1]
        df = df.replace('--', None)
        return df
        # for entry in df.to_numpy().tolist():
        # for entry in df.tolist():
        #     data_row = {k: v for k, v in zip(columns, entry)}
        #     data_rows.append(data_row)
        # return data_rows, columns

    @property
    def columns(self):
        return self._df.columns.values

    @property
    def data(self):
        return self._df.to_dict(orient='records')


class DirectAPI(object):
    API_URL = 'https://api.direct.yandex.com/json/v5/'

    def __init__(self,
                 access_token: str,
                 clid: str,
                 refresh_token: str = '',
                 lang: str = 'ru') -> None:
        """
        :param access_token: str
        :param clid: str
        :param refresh_token: str
        :param lang: str (ru, en, tr, uk)
        """
        self._access_token = access_token
        self._clid = clid
        self._refresh_token = refresh_token
        self._session = requests.Session()
        self._lang = lang.lower()
        self._session.headers['Accept'] = 'application/json'
        self._session.headers['Authorization'] = f'Bearer {self._access_token}'
        self._session.headers.update({
            "Accept-Language": self._lang,
            "Client-Login": self._clid
        })
        # add entities
        self.Ad = Ad(self)
        self.AdImage = AdImage(self)
        self.AdExtension = AdExtension(self)
        self.AdGroup = AdGroup(self)
        self.Bid = Bid(self)
        self.AudienceTarget = AudienceTarget(self)
        self.AgencyClient = AgencyClient(self)
        self.BidsModifier = BidsModifier(self)
        self.Campaign = Campaign(self)
        self.Change = Change(self)
        self.Dictionary = Dictionary(self)
        self.DynamicTextAdTarget = DynamicTextAdTarget(self)
        self.KeywordBid = KeywordBid(self)
        self.Keyword = Keyword(self)
        self.Lead = Lead(self)
        self.NegativeKeywordSharedSet = NegativeKeywordSharedSet(self)
        self.Sitelink = Sitelink(self)
        self.KeywordsResearch = KeywordsResearch(self)
        self.RetargetingList = RetargetingList(self)
        self.VCard = VCard(self)
        self.TurboPage = TurboPage(self)
        self.Report = Report(self)
        self.Client = Client(self)

    def set_clid(self, clid: str) -> None:
        self._clid = clid
        self._set_session_headers({"Client-Login": clid})

    def _set_session_headers(self, headers: dict) -> None:
        self._session.headers.update(**headers)

    def set_lang(self, lang: str) -> None:
        """
        :param lang: str (ru, en, tr, uk)
        :return: None
        """
        self._lang = lang
        self._set_session_headers({"Accept-Language": self._lang})

    def set_access_token(self, access_token: str) -> None:
        self._access_token = access_token
        self._set_session_headers(
            {"Authorization": f'Bearer {self._access_token}'})

    @property
    def clid(self) -> str:
        return self._clid

    @property
    def lang(self) -> str:
        return self._lang

    @property
    def access_token(self) -> str:
        return self._access_token

    def _get_reports(self, params: dict) -> str:
        url = f'{self.API_URL}reports/'
        while True:
            response = self._session.post(url, json=params, timeout=10)
            response.encoding = 'utf-8'
            if response.status_code == 200:
                response_str = response.content.decode('utf-8')
                return YdResponseReport(response_str)
            elif response.status_code == 201:
                # print("Report apply to offline que")
                retryIn = int(response.headers.get("retryIn", 10))
                sleep(retryIn)
            elif response.status_code == 202:
                retryIn = int(response.headers.get("retryIn", 10))
                sleep(retryIn)
            else:
                error = response.json()['error']
                raise YdAPIError(error)

    def _send_api_request(self,
                          service: str,
                          method: str,
                          params: dict,
                          timeout: int = 30) -> requests.Response:
        """
        :param service: str
        :param method: str
        :param params: dict
        :param timeout: int, default=30
        :return: response object
        """
        request_body = {'method': method, 'params': params}
        url = f'{self.API_URL}{service}'
        response = self._session.post(url, json=request_body, timeout=timeout)
        response.raise_for_status()
        if response.status_code > 204:
            error_data = response.json()
            if response.status_code == 401:
                raise YdAuthError(error_data['error'])
            raise YdAPIError(error_data['error'])
        return response
