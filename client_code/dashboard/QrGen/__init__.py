from ._anvil_designer import QrGenTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class QrGen(QrGenTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    token = anvil.js.window.localStorage.getItem("token")
    state, self.user = anvil.server.call('get_login_data', token)
    # Any code you write here will run before the form opens.
