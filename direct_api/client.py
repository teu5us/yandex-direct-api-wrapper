import requests
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
    YdResponse,
)


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

    def _send_api_request(self,
                          service: str,
                          request_body: dict,
                          timeout: int = 30) -> requests.Response:
        """
        :param service: str
        :param method: str
        :param params: dict
        :param timeout: int, default=30
        :return: response object
        """
        url = f'{self.API_URL}{service}'
        response = self._session.post(url, json=request_body, timeout=timeout)
        return response
