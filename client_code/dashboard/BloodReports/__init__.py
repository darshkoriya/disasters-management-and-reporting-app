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
    if self.user["is_admin"]:
      self.clear_reports.visible = True
    self.refresh_blood_reports()

  def refresh_blood_reports(self):
    blood_reports = anvil.server.call("get_blood_reports")
    self.repeating_panel_1.items = blood_reports

  def clear_reports_click(self, **event_args):
    anvil.server.call("delete_blood_report")
    self.refresh_disaster_list()
