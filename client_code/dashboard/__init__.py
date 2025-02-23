from ._anvil_designer import dashboardTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.js

from .ListDisasters import ListDisasters
from .QrGen import QrGen
from .ReportDisaster import ReportDisaster


class dashboard(dashboardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    locations = anvil.server.call('get_locations')
    coordinates_map = {tuple(coords): name for name, coords in locations}
    


    token = anvil.js.window.localStorage.getItem("token")
    state, user = anvil.server.call('get_login_data', token)
    if not state:
      open_form('Start')
    self.username_display.text = user['username']
    self.location_label.text = coordinates_map.get(tuple(map(float, str(user['home_location']).split(", "))), "404: Unknown Location")
    self.forms = {
            "ListDisasters": ListDisasters,
            "QrGen": QrGen,
            "ReportDisaster": ReportDisaster
        }
    self.load_form('ListDisasters')

  def load_form(self, form_name):
      if form_name in self.forms:
          self.content_panel.clear()
          form_instance = self.forms[form_name]()
          self.content_panel.add_component(form_instance)
    
  def toogle_user_menue_button_click(self, **event_args):
    self.user_menu_panel.visible = not self.user_menu_panel.visible

  def logout_link_click(self, **event_args):
    anvil.js.window.localStorage.setItem('token', 'None')
    open_form('Start')

  def report_disaster_button_click(self, **event_args):
    self.load_form('ReportDisaster')

  def link_user_profile_click(self, **event_args):
    open_form('dashboard.EditProfile')

  def generate_qr_click(self, **event_args):
    self.load_form('QrGen')
