from ._anvil_designer import EditProfileTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class EditProfile(EditProfileTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
  

    # Any code you write here will run before the form opens.
    token = anvil.js.window.localStorage.getItem("token")
    state, user = anvil.server.call('get_login_data', token)
    if not state:
      open_form('Start')
    self.username_display.text = user['username']
