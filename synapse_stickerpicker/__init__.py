# -*- coding: utf-8 -*
__author__ = 'mizhgun@gmail.com'

import typing
import copy

if typing.TYPE_CHECKING:
    from synapse.module_api import ModuleApi


class AppendStickerPickerData:

    def __init__(self, config=None, api: 'ModuleApi' = None):
        self._store = api.http_client.hs.datastores.main
        self.widget_content = {
            "type": "m.stickerpicker",
            "url": config['stickerpicker_url'],
            "name": "Stickerpicker",
            "creatorUserId": "",
            "data": {}
        }
        api.register_account_validity_callbacks(on_user_registration=self.on_user_registration)

    @staticmethod
    def parse_config(config):
        return config

    async def on_user_registration(self, user: str) -> None:
        content = copy.deepcopy(self.widget_content)
        content['creatorUserId'] = user
        account_data = {
            "stickerpicker": content
        }

        await self._store.add_account_data_for_user(user, 'm.widgets', account_data)
