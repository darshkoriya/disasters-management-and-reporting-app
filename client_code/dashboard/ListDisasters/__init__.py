from ._anvil_designer import ListDisastersTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ListDisasters(ListDisastersTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        token = anvil.js.window.localStorage.getItem("token")
        state, self.user = anvil.server.call('get_login_data', token)
        if self.user['is_admin']: self.clear_disasters.visible = True
        self.refresh_disaster_list()

    def refresh_disaster_list(self):
        disasters = anvil.server.call('get_disasters')
        self.repeating_panel_1.items = disasters

    def clear_disasters_click(self, **event_args):
      anvil.server.call('delete_disaster')
      self.refresh_disaster_list()


