import typing
import time
from urllib.parse import urlencode, urljoin

from aiohttp.client import ClientSession

from app.base.base_accessor import BaseAccessor
from app.store.vk_api.dataclasses import Message, UpdateMessage, UpdateObject, Update
from app.store.vk_api.poller import Poller

if typing.TYPE_CHECKING:
    from app.web.app import Application

API_VERSION = "5.131"


class VkApiAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: ClientSession | None = None
        self.key: str | None = None
        self.server: str | None = None
        self.poller: Poller | None = None
        self.ts: int | None = None

    async def connect(self, app: "Application"):
        self.session = ClientSession()
        await self._get_long_poll_service()
        self.poller = Poller(app.store)
        await self.poller.start()

    async def disconnect(self, app: "Application"):
        if self.poller:
            await self.poller.stop()

        if self.session:
            await self.session.close()

    @staticmethod
    def _build_query(host: str, method: str, params: dict) -> str:
        params.setdefault("v", API_VERSION)
        return f"{urljoin(host, method)}?{urlencode(params)}"

    async def _get_long_poll_service(self):
        url = self._build_query(
            host="https://api.vk.com/",
            method="method/groups.getLongPollServer",
            params={
                "group_id": self.app.config.bot.group_id,
                "access_token": self.app.config.bot.token
            }
        )
        response = await self.session.get(url)
        data = await response.json()

        self.key = data["response"]["key"]
        self.server = data["response"]["server"]
        self.ts = data["response"]["ts"]

    async def poll(self):
        params = {"act": "a_check", "key": self.key, "ts": self.ts, "wait": 25}
        url = f"{self.server}?{urlencode(params)}"
        response = await self.session.get(url)
        data = await response.json()

        if data["ts"]:
            self.ts = data["ts"]

        list_updates = list()
        for update in data["updates"]:
            if update["type"] == "message_new":
                msg = UpdateMessage(
                    from_id=update["object"]["message"]["from_id"],
                    id=update["object"]["message"]["id"],
                    text=update["object"]["message"]["text"]
                )
                update_object = UpdateObject(msg)
                list_updates.append(Update(type=update["type"], object=update_object))

        return list_updates

    async def send_message(self, message: Message) -> None:
        url = self._build_query(
            host="https://api.vk.com/",
            method="method/messages.send",
            params={
                "user_id": message.user_id,
                "message": message.text,
                "access_token": self.app.config.bot.token,
                "random_id": int(time.time() * 1000)
            }
        )

        await self.session.get(url)
