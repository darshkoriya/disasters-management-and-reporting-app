from ._anvil_designer import LoginTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.js
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Login(LoginTemplate):
  def __init__(self, **properties):

    self.init_components(**properties)
    token = anvil.js.window.localStorage.getItem("token")
    state, user = anvil.server.call('get_login_data', token)
    if state:
      open_form('dashboard')

  def login_button_click(self, **event_args):
    email = self.email_input.text
    password = self.password_input.text
    
    if not email or not password:
        alert("Please enter both email and password!")
        return
    
    success, message, token = anvil.server.call('login_user', email, password)
    
    if success:
        alert("Login successful! Redirecting...")
        anvil.js.window.localStorage.setItem('token', token)
        open_form('dashboard')
    else:
        alert(f"Login failed: {message}")
