from ._anvil_designer import ReportDisasterTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
natural_disasters = {
    "Severe": [
        "Earthquake", "Tsunami", "Hurricane", "Volcanic Eruption",
        "Major Flood", "Cyclone", "Typhoon", "Wildfire"
    ],
    "Moderate": [
        "Tornado", "Landslide", "Blizzard", "Heatwave",
        "Cold Wave", "Drought"
    ],
    "Mild": [
        "Hailstorm", "Dust Storm", "Lightning Strike", "Sinkhole"
    ]
}

all_disasters = sum(natural_disasters.values(), [])


class ReportDisaster(ReportDisasterTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.drop_down_severity.items = [("All", "All")] + [(key, key) for key in natural_disasters.keys()]
    self.drop_down_disaster.items = [(d, d) for d in all_disasters]
    self.lat = 0
    self.lon = 0
  
    # Any code you write here will run before the form opens.
    token = anvil.js.window.localStorage.getItem("token")
    state, self.user = anvil.server.call('get_login_data', token)
    if not state:
      open_form('Start')


    geolocation = anvil.js.window.navigator.geolocation
    print(geolocation)
  
    if geolocation:
        geolocation.getCurrentPosition(self.location_success, self.location_error)
    else:
        alert("Geolocation is not supported by your browser.")

  def drop_down_severity_change(self, **event_args):
    selected_severity = self.drop_down_severity.selected_value
        
    if selected_severity == "All" or not selected_severity:
        # Show all disasters if "All" is selected
        self.drop_down_disaster.items = [(d, d) for d in all_disasters]
    else:
        # Filter disasters by severity
        self.drop_down_disaster.items = [(d, d) for d in natural_disasters[selected_severity]]
    
    # Reset the disaster selection
    self.drop_down_disaster.selected_value = None


  def location_success(self, position):
        """Callback when location is retrieved successfully"""
        self.lat = position.coords.latitude
        self.lon = position.coords.longitude
        #alert(f"Your Location:\nLatitude: {lat}\nLongitude: {lon}")

  def location_error(self, error):
      """Callback when location retrieval fails"""
      alert(f"Error getting location: {error.message}")

  def drop_down_disaster_change(self, **event_args):
    selected_disaster = self.drop_down_disaster.selected_value
    self.label_1.text = f"Selected Disaster: {selected_disaster}" if selected_disaster else "Select a disaster"

  def button_submit_click(self, **event_args):
    selected_disaster = self.drop_down_disaster.selected_value
    selected_severity = self.drop_down_severity.selected_value

    if selected_severity == "All":
        for severity, disasters in natural_disasters.items():
            if selected_disaster in disasters:
                selected_severity = severity
                break

    anvil.server.call('report_disaster', self.user, selected_disaster, selected_severity, self.lat, self.lon)
    alert('Disaster reported successfully')
    open_form('dashboard')