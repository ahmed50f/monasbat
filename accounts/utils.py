from django.conf import settings
import pyotp
from django.utils.translation import gettext_lazy as _
from typing import Optional, Dict, Any
import requests
from django.core.cache import cache
from django.contrib.auth import get_user_model
import logging
from .models import Notification
logger = logging.getLogger(__name__)

User = get_user_model()

class CypartaServices:
    """
    Dispatcher class to interact with Cyparta messaging services API.
    Handles SMS, WhatsApp, and Email sending through the API.
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize the CypartaServices dispatcher.
        
        Args:
            api_key: Optional API key. If not provided, will use CYPARTA_SERVICES_API_KEY from settings.
            base_url: Optional base URL. If not provided, will use CYPARTA_SERVICES_BASE_URL from settings.
        """
        self.api_key = api_key or getattr(settings, 'CYPARTA_SERVICES_API_KEY', None)
        self.base_url = base_url or getattr(settings, 'CYPARTA_SERVICES_BASE_URL', None)
        
        if not self.api_key:
            raise ValueError("API key is required. Set CYPARTA_SERVICES_API_KEY in Django settings.")
        if not self.base_url:
            raise ValueError("Base URL is required. Set CYPARTA_SERVICES_BASE_URL in Django settings.")
        
        self.session = requests.Session()
        self._set_authentication()
    
    def _set_authentication(self):
        """Set the authentication header for all requests."""
        self.session.headers.update({
            'Authorization': f'Api-Key {self.api_key}',
            'Content-Type': 'application/json'
        })
    
    def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a POST request to the specified endpoint.
        
        Args:
            endpoint: API endpoint path
            data: Request payload
            
        Returns:
            API response as dictionary
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            
            # Try to parse JSON response
            try:
                result = response.json()
            except ValueError:
                result = {
                    "status": "error",
                    "message": f"Invalid JSON response from server. Status: {response.status_code}",
                    "raw_response": response.text
                }
            
            # Add status code to result for debugging
            result['http_status_code'] = response.status_code
            
            return result
            
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"Request failed: {str(e)}",
                "http_status_code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
            }
    
    def send_sms(self, phone_number: str, message: str) -> Dict[str, Any]:
        """
        Send an SMS message.
        
        Args:
            phone_number: Phone number in E.164 format (e.g., +201234567890)
            message: SMS content
            
        Returns:
            API response dictionary
        """
        data = {
            'phone_number': phone_number,
            'message': message
        }
        
        return self._make_request('send-sms/', data)
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the connection by trying to send a test SMS.
        This will fail gracefully if the API key is invalid.
        
        Returns:
            Test result dictionary
        """
        test_result = self.send_sms("+1234567890", "Test connection")
        
        if test_result.get('status') == 'error' and 'API key' in test_result.get('message', ''):
            return {
                "status": "error",
                "message": "Authentication failed - invalid API key",
                "connected": False
            }
        
        return {
            "status": "success",
            "message": "Connection test completed",
            "connected": True,
            "test_response": test_result
        }
        
        
class Util:
            
   @staticmethod
   def send_sms_verification(user, **kwargs):
        phone_number = kwargs.get('phone_number', None)
        otp = kwargs.get('otp', None)
    

        if not phone_number and not getattr(user, 'phone_number', None):
            raise ValueError("No phone number provided for sending SMS verification")

        if phone_number:
            phone_number = str(phone_number)
        else:
            phone_number = str(user.phone_number)

        user = User.objects.get(pk=user.id)
        
        if not otp:
            totp = pyotp.TOTP('base32secret3232', digits=4)
            otp = totp.now()
            cache.set(f"otp_{phone_number}", otp, timeout=300)
        print(otp)

        app_name = getattr(settings, "PROJECT_NAME", "wedding_halls")
        message = f"Your verification code is {otp} for {app_name}. Do not share this code with anyone."

        try:
            cyparta = CypartaServices()
            result = cyparta.send_sms(phone_number=phone_number, message=message)

            if result.get('status') == 'error':
                logger.error(f"SMS sending failed: {result}")
                return {"success": False, "error": result.get("message", "Unknown error")}
            return {"success": True, "result": result}

        except Exception as e:
            logger.exception("SMS provider threw an exception")
            return {"success": False, "error": str(e)}


def send_notification(user, sender, title, message, type="general"):
    return Notification.objects.create(
        user=user,
        sender=sender,
        title=title,
        message=message,
        type=type
    )