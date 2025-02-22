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
        self.refresh_disaster_list()

    def refresh_disaster_list(self):
        disasters = anvil.server.call('get_disasters')
        self.repeating_panel_1.items = disasters  # ✅ This sends data to DisasterRow


