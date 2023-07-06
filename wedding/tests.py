import json
from wedding import models
from django.test import TestCase

API_BASE = "/wedding"

class TestViewIndex (TestCase):
    
    def test_get (self):
        """ Test index view """
        
        # Make request
        response = self.client.get(f'{API_BASE}/')
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertContains (response, "Running")
        
class TestViewValidateVipCode (TestCase):
        
    def setUp (self):
        
        # Create VipCodes
        self.vip_code = "12345"
        models.VipCode.objects.create(value=self.vip_code, enabled=True)
        
    def test_valid (self):
        """ Test validate vip code view """
        
        # Make request
        response = self.client.post(
            f'{API_BASE}/validate-vip-code/', 
            json.dumps ({"vip-code": self.vip_code}),
            content_type="application/json"
        )
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "status": "success",
            "message": "valid vip code"
        })
    
    def test_invalid (self):
        """ Test validate vip code view """
        
        # Make request
        response = self.client.post(
            f'{API_BASE}/validate-vip-code/', 
            json.dumps ({"vip-code": "1234567"}),
            content_type="application/json"
        )
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "status": "error",
            "message": "invalid vip code"
        })
        
    def test_missing_vip_code (self):
        """ Test validate vip code view """
        
        # Make request
        response = self.client.post(
            f'{API_BASE}/validate-vip-code/',
            json.dumps ({}),
            content_type="application/json"
        )
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "status": "error",
            "message": "vip-code missing"
        })
        
class TestViewBuy (TestCase):
    
    def setUp (self):
        self.sample_data = {        
            "name": "John",
            "last-name": "Doe",
            "vip-code": "123456",
            "price": 100,
            "stripe-data": {
                "sample": {
                    "amount": 1,
                    "description": "sample product",
                    "image_url": "https://www.darideveloper.com/imgs/logo.png",
                    "price": 100
                }
            }
        }
    
    def test_success (self):
        """ Test buy view """
                
        # Make request
        response = self.client.post(
            f'{API_BASE}/buy/', 
            json.dumps (self.sample_data),
            content_type="application/json"
        )
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertEqual(response.json()["message"], "stripe link generated")
        self.assertIn("checkout.stripe.com/c/pay/", response.json()["stripe_link"])
        
    def text_missing_data (self):
        """ Test buy view without submiting full data """
        
        incomplete_data = self.sample_data.copy()
        incomplete_data.pop("name")
        
        response = self.client.post(
            f'{API_BASE}/buy/', 
            json.dumps (incomplete_data),
            content_type="application/json"
        )
        
         # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "error")
        self.assertEqual(response.json()["message"], "missing data")
    
    def text_eror_stripe_link (self):
        """ Test buy with incorrect stripe data """
        
        incomplete_data = self.sample_data.copy()
        incomplete_data["stripe-data"]["sample"].pop("amount")
        
        response = self.client.post(
            f'{API_BASE}/buy/', 
            json.dumps (incomplete_data),
            content_type="application/json"
        )
        
         # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "error")
        self.assertEqual(response.json()["message"], "error generating stripe link")
        
        
        
# class TestViewTransports (TestCase):