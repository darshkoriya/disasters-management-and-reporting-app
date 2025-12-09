from ._anvil_designer import StartTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Start(StartTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    token = anvil.js.window.localStorage.getItem("token")
    state, user = anvil.server.call('get_login_data', token)
    if state:
      open_form('dashboard')

  def login_redirect_click(self, **event_args):
    open_form('Login')

  def Sign_up_redirect_click(self, **event_args):
    open_form('register')
