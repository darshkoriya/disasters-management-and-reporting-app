from ._anvil_designer import BloodReportsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class BloodReports(BloodReportsTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    token = anvil.js.window.localStorage.getItem("token")
    state, self.user = anvil.server.call("get_login_data", token)
    self.lat = 0
    self.lon = 0
    if self.user["is_admin"]:
      self.clear_reports.visible = True
    self.blood_type_input.items = [
    "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-",  # Common ABO groups
    "Bombay Blood Group (hh)",  # Extremely rare
    "Rh-null",  # Golden Blood (very rare)
    "Duffy-negative",  # Common in certain populations
    "Kell-positive (K+)", "Kell-negative (K-)",  # Kell blood system
    "Diego-positive",  # Rare, mostly in Indigenous American & East Asian populations
    "Lutheran B-negative",  # Very rare
    "MNS system variants",  # Rare antigenic variations
    "Junior blood group",  # Rare in certain populations
    "Langereis blood group"  # Rare
]
    geolocation = anvil.js.window.navigator.geolocation
    print(geolocation)
  
    if geolocation:
        geolocation.getCurrentPosition(self.location_success, self.location_error)
    else:
        alert("Geolocation is not supported by your browser.")
      
    self.refresh_blood_reports()

  def location_success(self, position):
        """Callback when location is retrieved successfully"""
        self.lat = position.coords.latitude
        self.lon = position.coords.longitude
        #alert(f"Your Location:\nLatitude: {lat}\nLongitude: {lon}")

  def location_error(self, error):
      """Callback when location retrieval fails"""
      alert(f"Error getting location: {error.message}")

  def refresh_blood_reports(self):
    blood_reports = anvil.server.call("get_blood_reports")
    self.repeating_panel_1.items = blood_reports

  def clear_reports_click(self, **event_args):
    anvil.server.call("delete_blood_report")
    open_form("dashboard.BloodReports")

  def request_blood_button_click(self, **event_args):
    self.report_panel.visible = not self.report_panel.visible

  def submit_click(self, **event_args):
    anvil.server.call('submit_blood_report', self.user['user_id'], f'{self.lat}, {self.lon}', self.blood_type_input.selected_value, self.contact_no_input.text)
    open_form("dashboard.BloodReports")
