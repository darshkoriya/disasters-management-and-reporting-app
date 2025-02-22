from ._anvil_designer import registerTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import base64


def text_to_base64(text: str) -> str:
    encoded_bytes = base64.b64encode(text.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def base64_to_text(base64_string: str) -> str:
    decoded_bytes = base64.b64decode(base64_string)
    return decoded_bytes.decode('utf-8')


class register(registerTemplate):
  global lat, lon
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.home_select_box.items = anvil.server.call('get_locations')
    self.lat = 0
    self.lon = 0

    token = anvil.js.window.localStorage.getItem("token")
    state, user = anvil.server.call('get_login_data', token)
    if state:
      open_form('dashboard')

  def Submit_click(self, **event_args):
    firstname = self.first_name_input.text
    lastname = self.last_name_input.text
    email = self.email_input.text
    password=self.password_input.text
    confirm_password=self.confirm_password.text
    birthday = self.date_picker_1.date
    disabilties = self.disablities_input.text
    home = f'{lat}, {lon}'

    if not firstname or not lastname or not email or not password or not confirm_password or not birthday:
            alert("Please fill in all fields!")
            return
    username = f'{firstname} {lastname}'
    if password != confirm_password:
            alert("Passwords do not match! Please try again")
            return
    success, message = anvil.server.call('register_user', username, email, password, birthday, disabilties, home)


    if success:
        alert("Registration successful! You can now log in.")
        open_form('Login')
    else:
        alert(f"Error: {message}")

  def home_select_box_change(self, **event_args):
    global lat, lon
    selected_data = self.home_select_box.selected_value
    
    if selected_data:
        lat, lon = selected_data
        self.lat = str(lat)
        self.lon = str(lon)


