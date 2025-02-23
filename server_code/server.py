import anvil.server
import anvil.tables
import anvil.js
import datetime
from anvil.tables import app_tables
import hashlib
import uuid
import random
import re
import base64
import string
import time
import qrcode
from PIL import Image
import cv2
from io import BytesIO

locations = [
    ('India, Andhra Pradesh, Visakhapatnam', (17.6868, 83.2185)),
    ('India, Arunachal Pradesh, Itanagar', (27.0844, 93.6053)),
    ('India, Assam, Guwahati', (26.1445, 91.7362)),
    ('India, Bihar, Patna', (25.5941, 85.1376)),
    ('India, Chhattisgarh, Raipur', (21.2514, 81.6296)),
    ('India, Goa, Panaji', (15.4909, 73.8278)),
    ('India, Gujarat, Ahmedabad', (23.0225, 72.5714)),
    ('India, Haryana, Chandigarh', (30.7333, 76.7794)),
    ('India, Himachal Pradesh, Shimla', (31.1048, 77.1734)),
    ('India, Jharkhand, Ranchi', (23.3441, 85.3096)),
    ('India, Karnataka, Bengaluru', (12.9716, 77.5946)),
    ('India, Kerala, Thiruvananthapuram', (8.5241, 76.9366)),
    ('India, Madhya Pradesh, Bhopal', (23.2599, 77.4126)),
    ('India, Maharashtra, Mumbai', (19.0760, 72.8777)),
    ('India, Manipur, Imphal', (24.8170, 93.9368)),
    ('India, Meghalaya, Shillong', (25.5788, 91.8933)),
    ('India, Mizoram, Aizawl', (23.7271, 92.7176)),
    ('India, Nagaland, Kohima', (25.6751, 94.1086)),
    ('India, Odisha, Bhubaneswar', (20.2961, 85.8245)),
    ('India, Punjab, Amritsar', (31.6340, 74.8723)),
    ('India, Rajasthan, Jaipur', (26.9124, 75.7873)),
    ('India, Sikkim, Gangtok', (27.3314, 88.6138)),
    ('India, Tamil Nadu, Chennai', (13.0827, 80.2707)),
    ('India, Telangana, Hyderabad', (17.3850, 78.4867)),
    ('India, Tripura, Agartala', (23.8315, 91.2868)),
    ('India, Uttar Pradesh, Lucknow', (26.8467, 80.9462)),
    ('India, Uttarakhand, Dehradun', (30.3165, 78.0322)),
    ('India, West Bengal, Kolkata', (22.5726, 88.3639))
]


def generate_user_id(length: int = 8) -> str:
    """Generate a random numerical user ID with the given length."""
    return ''.join(random.choices("0123456789", k=length))

def generate_random_text(length: int = 10, use_digits: bool = True, use_special_chars: bool = False) -> str:
    """Generate a random text string with the given length."""
    characters = string.ascii_letters  # A-Z, a-z
    
    if use_digits:
        characters += string.digits  # Add 0-9
    
    if use_special_chars:
        characters += string.punctuation

    return ''.join(random.choices(characters, k=length))

def text_to_base64(text: str) -> str:
    encoded_bytes = base64.b64encode(str(text).encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def base64_to_text(base64_string: str) -> str:
    decoded_bytes = base64.b64decode(base64_string)
    return decoded_bytes.decode('utf-8')

SALT = "c2FuanVrdGE="
logged_in_users = set()
def hash_password(password):
    return hashlib.sha256((SALT + password).encode()).hexdigest()

@anvil.server.callable
def is_user_logged_in():
    return anvil.server.session.get('user_email') in logged_in_users

@anvil.server.callable
def register_user(username, email, password, birthday, disabilties, home):
    if app_tables.users.get(email=email):
        return False, "Email already registered!"

    # Validate password strength (min 8 chars, 1 digit, 1 special character)
    if len(password) < 8 or not re.search(r"\d", password) or not re.search(r"[!@#$%^&*]", password):
        return False, "Password must be at least 8 characters long and contain a number & special character!"
    hashed_password = hash_password(password)
    userid = generate_user_id(20)
    token = f"{text_to_base64(userid)}.{text_to_base64(time.time())}.{text_to_base64(generate_random_text(10, True, True))}"
    
    app_tables.users.add_row(token=token, 
                             username=username, 
                             email=email, 
                             password=hashed_password, 
                             birthday=str(birthday), 
                             disablities=disabilties,
                             home_location=home,
                             user_id=userid)

    return True, "User registered successfully!"

@anvil.server.callable
def login_user(email, password):
    user = app_tables.users.get(email=email)
    if user and user['password'] == hash_password(password):
        anvil.server.session['user_email'] = email
        logged_in_users.add(email)
        token = user['token']
        return True, "Login successful!", token
    return False, "Invalid email or password", None

@anvil.server.callable
def get_login_data(token):
  user = app_tables.users.get(token=token)
  if not user:
    return False, user
  return True, user


@anvil.server.callable
def get_locations():
  return locations

@anvil.server.callable
def get_disasters():
    return [
        {
            "disaster_name": row["disaster"],
            "severity": row["severity"],
            "timestamp": datetime.datetime.fromtimestamp(float(row["reported_time"])).strftime("%Y-%m-%d %H:%M:%S") if row["reported_time"] else None,
            "location": row['location']
        }
        for row in app_tables.disasters.search()
    ]


@anvil.server.callable
def generate_qr(message):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,  # Adjust as needed
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(message)
    qr.make(fit=True)

    # Create the QR code image
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # Save to a BytesIO object
    img_io = BytesIO()
    img.save(img_io, format="PNG")
    img_io.seek(0)

    # Return as an Anvil Media object
    return anvil.media.from_file(img_io, "image/png", "qr_code.png")


