from ._anvil_designer import EditUserTemplate
from anvil import *
import anvil.server
import anvil.tables.query as q
import base64

def text_to_base64(text: str) -> str:
    encoded_bytes = base64.b64encode(text.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def base64_to_text(base64_string: str) -> str:
    decoded_bytes = base64.b64decode(base64_string)
    return decoded_bytes.decode('utf-8')

class EditUser(EditUserTemplate):
    def __init__(self, user_id=None, **properties):
        self.init_components(**properties)
        token = anvil.js.window.localStorage.getItem("token")
        state, self.user = anvil.server.call('get_login_data', token)
        self.user_id = self.user['user_id']
        
        self.home_select_box.items = anvil.server.call('get_locations')
        self.blood_group_selecton.items = [
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
        
        self.lat = 0
        self.lon = 0
        self.load_user_data()

    def load_user_data(self):
        if not self.user_id:
            alert("No user ID provided.")
            return
        
        if not self.user:
            alert("User not found.")
            return

        full_name = self.user['username']  # Assuming the name is stored as one string
        name_parts = full_name.split()  # Split by spaces

        # Assign first, middle, and last names dynamically
        self.first_name_input.text = name_parts[0] if len(name_parts) > 0 else ''
        self.middle_name_input.text = name_parts[1] if len(name_parts) > 2 else ''
        self.last_name_input.text = name_parts[-1] if len(name_parts) > 1 else ''
      
        self.email_input.text = self.user['email']
        self.date_picker_1.date = self.user['birthday']
        self.disablities_input.text = self.user['disablities']
        self.blood_group_selecton.selected_value = self.user['blood_group']
        self.allergies_input.text = self.user['allergies']
        self.diseases_input.text = self.user['diseases']
        self.contact_input.text = self.user['important_contacts']
        
        location = self.user['home_location']
        self.lat, self.lon = map(float, location.split(','))

    def Submit_click(self, **event_args):
      username = f'{self.first_name_input.text} ' + (f'{self.middle_name_input.text} ' if self.middle_name_input.text else '') + self.last_name_input.text
      updated_data = {
            "user_id": self.user_id,
            "username": username,
            "email": self.email_input.text,
            "birthday": str(self.date_picker_1.date),
            "disabilities": self.disablities_input.text,
            "blood_group": self.blood_group_selecton.selected_value,
            "allergies": self.allergies_input.text,
            "diseases": self.diseases_input.text,
            "contacts": self.contact_input.text,
            "home": f"{self.lat}, {self.lon}"
        }
        
      success, message = anvil.server.call('update_user', updated_data)
      
      if success:
          alert("User information updated successfully!")
          open_form('dashboard')
      else:
          alert(f"Error: {message}")
