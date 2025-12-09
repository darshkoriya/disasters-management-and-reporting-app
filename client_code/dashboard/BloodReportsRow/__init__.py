from ._anvil_designer import BloodReportsRowTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class BloodReportsRow(BloodReportsRowTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    token = anvil.js.window.localStorage.getItem("token")
    state, self.user = anvil.server.call("get_login_data", token)

    # Set data from ListDisasters
    self.label_blood_type.text = f"Blood Type: {self.item.get('blood_type', 'Unknown')}"
    self.label_contact.text = f"Contact: {self.item.get('contact', 'Unknow')}"
    self.lat, self.lon = map(float, self.item.get("location").strip().split(","))
    self.report_id = self.item.get("id")
    position = GoogleMap.LatLng(self.lat, self.lon)
    print(self.item)

    if self.user["is_admin"]:
      self.delete_report.visible = True
    if self.user["user_id"] == self.item.get("user_id"):
      self.delete_report.visible = True

    # Set background color based on severity
    self.role = "card"
    self.background = "#00c928"

    self.location_map.center = position
    self.location_map.zoom = 12
    marker = GoogleMap.Marker(position=position)
    self.location_map.add_component(marker)

  def location_map_bounds_changed(self, **event_args):
    """This method is called when the viewport bounds have changed."""
    pass

  def show_location_click(self, **event_args):
    self.location_map.visible = not self.location_map.visible

  def delete_report_click(self, **event_args):
    success = anvil.server.call("delete_blood_report", self.report_id)
    if success:
      self.parent.items = [
        item for item in self.parent.items if item.get("id") != self.report_id
      ]
      open_form("dashboard")
