from ._anvil_designer import DisasterRowTemplate
from anvil import *

# Define colors based on severity
severity_colors = {
    "Severe": "#f10700",   # Red
    "Moderate": "#f16600", # Orange
    "Mild": "#f1af00"      # Yellow
}

class DisasterRow(DisasterRowTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        # Set data from ListDisasters
        self.label_disaster.text = self.item.get("disaster_name", "Unknown Disaster")
        self.label_severity.text = f"Severity: {self.item.get('severity', 'Unknown')}"
        self.label_timestamp.text = f"Reported on: {self.item.get('timestamp', 'Unknown')}"
        position = map(float, self.item.get('location').strip().split(','))
        self.lat, self.lon = map(float, self.item.get('location').strip().split(','))


        # Set background color based on severity
        severity = self.item.get("severity", "Mild")  # Default to Mild
        self.role = "card"
        self.background = severity_colors.get(severity, "#FFFFFF")  # Default White

        self.location_map.center = position
        self.location_map.center = 12
        marker = GoogleMap.Marker(position=position)
        self.location_map.add_component(marker)
      
    def location_map_bounds_changed(self, **event_args):
      """This method is called when the viewport bounds have changed."""
      pass
