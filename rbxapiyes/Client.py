from .utils import Requests
from .PlayerInfo import PlayerInfo
from .exceptions import GroupNotFound, PlayerNotFound, GameNotFound
from .Auth_Player import PlayerAuth
from .BundleInfo import BundleInfo
from .AssetInfo import AssetInfo
from .Twocaptcha import TwoCaptcha
import aiohttp
import json


class Client:
    """

    Represents a roblox.py Main Client.

    """

    def __init__(self, cookies: str = None):
        self.cookies = cookies
        self.request = Requests(cookies=cookies)

    @staticmethod
    async def get_cookies_from_credentials(username_or_email, password, login_type, token: TwoCaptcha):

        """
        Returns Cookies using Username/Email and Password

        Parameters
        ----------
        username_or_email : str
            User Email/Password to login in
        password : str
            Password of the account
        login_type : str
            login type to login in, can be "email" or "username"
        token : stc
            roblox_py.TwoCaptcha

        """
        login_type = login_type.lower()
        login_dict = None
        if login_type == "email":
            login_dict = {
                "ctype": "Email",
                "cvalue": f"{username_or_email}",
                "password": f"{password}",
            }
        if login_type == "username":
            login_dict = {
                "ctype": "Username",
                "cvalue": username_or_email,
                "password": password
            }
        xcrsftoken = ""
        async with aiohttp.ClientSession() as ses:
            async def update_xcrsftoken():
                async with ses.post(url="https://auth.roblox.com/") as xcsf_req:
                    try:
                        xcrsftoken = xcsf_req.headers["X-CSRF-TOKEN"]
                        return xcrsftoken
                    except KeyError:
                        xcrsftoken = ""
                        return xcrsftoken

            login_dict = json.dumps(login_dict)
            xcrsftoken = await update_xcrsftoken()

            async with ses.post(url=f'https://auth.roblox.com/v2/login', data=login_dict, headers={
                'X-CSRF-TOKEN': xcrsftoken,
                'DNT': '1',
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                'Content-type': 'application/json',
                'Accept': 'application/json',
                'referer': 'www.roblox.com',
                'Origin': 'www.roblox.com',
            }) as f:
                josn = await f.json()

            if f.status == 403:
                if josn['errors'][0]['message'] == "Token Validation Failed":
                    xcrsftoken = await update_xcrsftoken()
                if josn['errors'][0]['message'] == 'You must pass the robot test before logging in.':
                    et = await token.solve(public_key=f'476068BF-9607-4799-B53D-966BE98E2B81')
                    if login_type == "email":
                        login_dict = {
                            "ctype": "Email",
                            "cvalue": username_or_email,
                            "password": password,
                            'captchaToken': et,
                            "captchaProvider": 'PROVIDER_ARKOSE_LABS'}
                    if login_type == 'username':
                        login_dict = {
                            "ctype": "Username",
                            "cvalue": username_or_email,
                            "password": password,
                            'captchaToken': et,
                            "captchaProvider": 'PROVIDER_ARKOSE_LABS'}
                    login_dict = json.dumps(login_dict)
                    xcrsftoken = await update_xcrsftoken()

                    async with ses.post(url=f'https://auth.roblox.com/v2/login', data=login_dict, headers={
                        'X-CSRF-TOKEN': xcrsftoken,
                        'DNT': '1',
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                        'Content-type': 'application/json',
                        'Accept': 'application/json',
                        'referer': 'www.roblox.com',
                        'Origin': 'www.roblox.com',
                    }) as no:
                        ja = await no.json()
                        if no.status == 403:
                            if ja['errors'][0]['message'] == "Token Validation Failed":
                                xcrsftoken = await update_xcrsftoken()
                        try:
                            cookie_dict = {
                                '.ROBLOSECURITY': f"{no.cookies.get('.ROBLOSECURITY').value}",
                                ".RBXID": f"{no.cookies.get('.RBXID').value}"}
                            return cookie_dict

                        except Exception:
                            return no.cookies

    async def get_user_by_name(self, username: str) -> PlayerInfo:
        """

        Returns Player Info Class By username - Also Calls the update Function

        Parameters
        ----------
        username : str
            Name of the User

        Returns
        -------
        roblox_py.PlayerInfo

        """
        url = f"https://api.roblox.com/users/get-by-username"
        pars = {'username': username}
        json1 = await self.request.request(url=url, parms=pars, method='get')
        if "Id" not in json1.keys():
            raise PlayerNotFound("Username is Invalid")
        else:
            e = PlayerInfo(player_id=json1['Id'], request=self.request)
            await e.update()
            return e

    async def get_user_info(self, Player_Id: int) -> PlayerInfo:
        """

        Returns Player Info Class - Also Calls the update Function

        Parameters
        ----------
        Player_Id : int
            ID of the User

        Returns
        -------
        roblox_py.PlayerInfo

        """
        idkdd = isinstance(Player_Id, str)
        if idkdd:
            raise TypeError(f"{Player_Id} must be an integer")
        yes = PlayerInfo(player_id=Player_Id, request=self.request)
        await yes.update()
        return yes

    async def get_auth_user(self) -> PlayerAuth:
        """
        Returns Authenticated User class

        Returns
        -------
        roblox_py.PlayerAuth

        """
        return PlayerAuth(request=self.request)

    async def get_bundle(self, Bundle_ID: int) -> BundleInfo:
        """
        Returns Bundle Info Class

        Parameters
        ----------
        Bundle_ID : int
            Bundle ID

        Returns
        -------
        roblox_py.BundleInfo

        """
        idkdd = isinstance(Bundle_ID, str)
        if idkdd:
            raise TypeError(f"{Bundle_ID} must be an integer")
        yes = BundleInfo(bundle_id=Bundle_ID, request=self.request)
        await yes.update()
        return yes

    async def get_asset(self, Asset_id: int) -> AssetInfo:
        """

        Returns Asset Info Class - Also Calls the update Function

        Parameters
        ----------
        Asset_id : int
            Asset id

        Returns
        -------
        roblox_py.AssetInfo

        """
        idkdd = isinstance(Asset_id, str)
        if idkdd:
            raise TypeError(f"{Asset_id} must be an integer")
        yes = AssetInfo(asset_id=Asset_id, request=self.request)
        await yes.update()
        return yes