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
        
        self.api_endpoint = f'{API_BASE}/validate-vip-code/'
        
        # Create VipCodes
        self.vip_code = "12345"
        models.VipCode.objects.create(value=self.vip_code, enabled=True)
        
    def test_valid (self):
        """ Test validate vip code view """
        
        # Make request
        response = self.client.post(
            self.api_endpoint, 
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
            self.api_endpoint, 
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
            self.api_endpoint,
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
        
        self.api_endpoint = f"{API_BASE}/buy/" 
        
        # Create sample data
        self.sample_data = {        
            "name": "John",
            "last-name": "Doe",
            "vip-code": "123456",
            "price": 100,
            "from-host": "https://www.darideveloper.com",
            "stripe-data": {
                "sample": {
                    "amount": 1,
                    "description": "sample product",
                    "image_url": "https://www.darideveloper.com/imgs/logo.png",
                    "price": 100
                }
            }
        }
        
        self.vip_code = "12345"
        models.VipCode.objects.create(value=self.vip_code, enabled=True)
    
    def test_success (self):
        """ Test buy view """
                
        # Make request
        response = self.client.post(
            self.api_endpoint, 
            json.dumps (self.sample_data),
            content_type="application/json"
        )
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertEqual(response.json()["message"], "stripe link generated")
        self.assertIn("checkout.stripe.com/c/pay/", response.json()["redirect"])
        
    def test_missing_data (self):
        """ Test buy view without submiting full data """
        
        incomplete_data = self.sample_data.copy()
        incomplete_data.pop("name")
        
        response = self.client.post(
            self.api_endpoint, 
            json.dumps (incomplete_data),
            content_type="application/json"
        )
        
         # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "error")
        self.assertEqual(response.json()["message"], "missing data")
    
    def test_eror_stripe_data (self):
        """ Test buy with incorrect stripe data """
        
        incomplete_data = self.sample_data.copy()
        incomplete_data["stripe-data"]["sample"].pop("amount")
        
        response = self.client.post(
            self.api_endpoint, 
            json.dumps (incomplete_data),
            content_type="application/json"
        )
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "error")
        self.assertEqual(response.json()["message"], "error generating stripe link")
        
    def test_vip_sucess (self):
        
        # Replace vip code from sample data
        self.sample_data["vip-code"] = self.vip_code
        
        response = self.client.post(
            self.api_endpoint, 
            json.dumps (self.sample_data),
            content_type="application/json"
        )
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertEqual(response.json()["message"], "sale saved")
        self.assertIn("success", response.json()["redirect"])
        
        
    
class TestViewTransports (TestCase):
    
    def setUp (self):
        
        self.api_endpoint = f"{API_BASE}/transports/"
        
    def test_get (self):
        """ Test get transports """
        
        # Create transport models
        transport_1 = models.Transport.objects.create(
            key="sample 1",
            name="Sample transport 1",
            price=100,
            by_default=True
        )
        
        transport_2 = models.Transport.objects.create(
            key="sample 2",
            name="Sample transport 2",
            price=100,
            by_default=True
        )
                
        response = self.client.get(
            self.api_endpoint
        )
        
        # Format data from models
        data = []
        for transport in [transport_1, transport_2]:
            data.append({
                "id": transport.id,
                "key": transport.key,
                "name": transport.name,
                "price": transport.price,
                "by_default": transport.by_default
            })
            
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertEqual(response.json()["message"], "transports found")
        self.assertEqual(response.json()["data"], data)
        
    def test_no_models (self):
        """ Test get transports without models """
        
        response = self.client.get(
            self.api_endpoint
        )
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "error")
        self.assertEqual(response.json()["message"], "transports not found")
        self.assertEqual(response.json()["data"], [])
        
class TestViewHotels (TestCase):
    
    def setUp (self):
        self.api_endpoint = f"{API_BASE}/hotels/"
        
    def test_get (self):
        """ Test get hotels """
        
        # Create transport models
        hotel_1 = models.Hotel.objects.create(
            name = "Sample hotel 1",
            extra_price = 100.51,
        )
        
        hotel_2 = models.Hotel.objects.create(
            name = "Sample hotel 2",
            extra_price = 100.01,
        )
                
        response = self.client.get(
            self.api_endpoint
        )
        
        # Format data from models
        data = []
        for hotel in [hotel_1, hotel_2]:
                        
            data.append({
                "id": hotel.id,
                "name": hotel.name,
                "extra_price": str(hotel.extra_price),
            })
            
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertEqual(response.json()["message"], "hotels found")
        self.assertEqual(response.json()["data"], data)
        
    def test_no_models (self):
        """ Test get hotels without models """
        
        response = self.client.get(
            self.api_endpoint
        )
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "error")
        self.assertEqual(response.json()["message"], "hotels not found")
        self.assertEqual(response.json()["data"], [])
        
class TestViewFreeDays (TestCase):
    
    def setUp (self):
        self.api_endpoint = f"{API_BASE}/free-days/"
        
    def test_get (self):
        """ Test get free days """
        
        # Create transport models
        arrival_date = "2021-01-01"
        departure_date = "2021-01-02"
        models.Setting.objects.create(
            name="arrival_free_date",
            value=arrival_date
        )
        models.Setting.objects.create(
            name="departure_free_date",
            value=departure_date
        )
        
        response = self.client.get(
            self.api_endpoint
        )

        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertEqual(response.json()["message"], "free days found")
        self.assertEqual(response.json()["data"], {
            "arrival": arrival_date,
            "departure": departure_date
        })
        
    def test_no_models (self):
        """ Test get hotels without models """
        
        response = self.client.get(
            self.api_endpoint
        )
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "error")
        self.assertEqual(response.json()["message"], "error getting free days")
        self.assertEqual(response.json()["data"], {})
        
          