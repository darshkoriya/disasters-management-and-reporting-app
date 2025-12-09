from ._anvil_designer import dashboardTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.js

from .ListDisasters import ListDisasters
from .ReportDisaster import ReportDisaster
from .EditUser import EditUser
from .BloodReports import BloodReports
from .BloodDonations import BloodDonations


class dashboard(dashboardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    locations = anvil.server.call('get_locations')
    coordinates_map = {tuple(coords): name for name, coords in locations}
    


    token = anvil.js.window.localStorage.getItem("token")
    state, self.user = anvil.server.call('get_login_data', token)
    if not state:
      open_form('Start')
    self.username_display.text = self.user['username']
    self.location_label.text = coordinates_map.get(tuple(map(float, str(self.user['home_location']).split(", "))), "404: Unknown Location")
    self.forms = {
            "ListDisasters": ListDisasters,
            "ReportDisaster": ReportDisaster,
            "EditProfile": EditUser,
            "BloodReports": BloodReports,
            "BloodDonations": BloodDonations
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
    self.load_form('EditProfile')

  def generate_qr_click(self, **event_args):
    data = f"""Person Details:
    Name: {self.user['username']}
    DoB (YY-MM-DD): {self.user['birthday']}
    Disabilities: {self.user['disablities']}
    blood group: {self.user['blood_group']}
    diseases: {self.user['diseases']}
    allergies: {self.user['allergies']}
    Emergency Contacts: {self.user['important_contacts']}
    """

    # Call server function and get the QR code as a Media object
    qr_media = anvil.server.call('generate_qr', data, f'Qr_{self.user["username"]}')

    # Provide download link to the user
    #anvil.js.window.open(qr_media.url, "_blank")  # Opens in new tab

    # Alternatively, use Anvil's built-in download function
    anvil.download(qr_media)

  def home_link_click(self, **event_args):
    self.load_form('ListDisasters')

  def blood_reports_link_click(self, **event_args):
    self.load_form('BloodReports')

  def donate_blood_link_click(self, **event_args):
    print("Button clicked")
    self.load_form('BloodDonations')

