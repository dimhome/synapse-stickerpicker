# -*- coding: utf-8 -*
__author__ = 'mizhgun@gmail.com'

import typing
import copy
import logging

if typing.TYPE_CHECKING:
    from synapse.module_api import ModuleApi

logger = logging.getLogger(__name__)


class AppendStickerPickerData:

    def __init__(self, config=None, api: 'ModuleApi' = None):
        self._store = api.http_client.hs.datastores.main
        self.stickerpicker_data = {
            "stickerpicker": {
                "content": {
                    "type": "m.stickerpicker",
                    "url": config['stickerpicker_url'],
                    "name": "Stickerpicker",
                    "creatorUserId": "",
                    "data": {}
                },
                "sender": "",
                "state_key": "stickerpicker",
                "type": "m.widget",
                "id": "stickerpicker"
            }
        }
        api.register_account_validity_callbacks(on_user_registration=self.on_user_registration)

    @staticmethod
    def parse_config(config):
        return config

    async def on_user_registration(self, user: str) -> None:
        logger.info("AppendStickerPickerData: on_user_registration called for user: %s", user)
        data = copy.deepcopy(self.stickerpicker_data)
        data['stickerpicker']['content']['creatorUserId'] = user
        data['stickerpicker']['sender'] = user
        logger.info("AppendStickerPickerData: saving data for user %s: %s", user, data)
        await self._store.add_account_data_for_user(user, 'm.widgets', data)
