from ._anvil_designer import QrGenTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables



class QrGen(QrGenTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    token = anvil.js.window.localStorage.getItem("token")
    state, self.user = anvil.server.call('get_login_data', token)

  def submit_button_click(self, **event_args):
    data = f"""Person Details:
    Name: {self.user['username']}
    DoB: {self.user['birthday']}
    Disabilities: {self.user['disablities']}
    Emergency Contacts: {self.input_contacts.text}
    """

    # Call server function and get the QR code as a Media object
    qr_media = anvil.server.call('generate_qr', data, f'Qr_{self.user["username"]}')

    # Provide download link to the user
    #anvil.js.window.open(qr_media.url, "_blank")  # Opens in new tab

    # Alternatively, use Anvil's built-in download function
    anvil.download(qr_media)

