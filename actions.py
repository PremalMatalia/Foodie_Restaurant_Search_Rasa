from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from typing import Dict , Text , Any , List , Union , Optional

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import zomatopy
import json
from email.message import EmailMessage
import smtplib
from flask import Flask
from flask_mail import Mail , Message
from flask_mail import Message

# ***Global variable so it can be used in ActionSearchRestaurants and ActionSendEmail both***#
email_response = ""
email_response_count = 0

class ActionSearchRestaurants(Action):
    def name(self):
        return 'action_search_restaurants'

    def run(self , dispatcher , tracker , domain):
        config = {"user_key": "531a13542df1225df159aa1793ff8d1d"}
        zomato = zomatopy.initialize_app(config)
        loc = tracker.get_slot('location')
        cuisine = tracker.get_slot('cuisine')
        price = tracker.get_slot('price')

        # *** logic for price range ***#
        lprice = 0
        hprice = 0
        if price == 'lesser than 300':
            hprice = 300
        elif price == '300 to 700':
            lprice = 300
            hprice = 700
        else:
            lprice = 700
            hprice = 100000

        location_detail = zomato.get_location(loc , 1)
        json_location_detail = json.loads(location_detail)
        lat = json_location_detail["location_suggestions"][0]["latitude"]
        lon = json_location_detail["location_suggestions"][0]["longitude"]
        # *** This cuisine ids have been taken from get_cuisine zomato api ***#
        cuisines_dict = {'chinese': 25 , 'Mexican': 73 , 'italian': 55 , 'American': 1 , 'north indian': 50 ,
                         'south indian': 85}

        # *** Call restaurant_search function to get 20 (max zomato api results) search results ***#
        results = zomato.restaurant_search("" , lat , lon , str(cuisines_dict.get(cuisine)) , 20)
        json_results = json.loads(results)

        # ****Response variable for rasa bot and email***#
        response = ""
        global email_response
        email_response = " "
        response_count = 0
        email_response_count = 0
        restaurant_exist = False

        #if json_results['results_found'] == 0:
        #    response = "Sorry there are no restaurant with this criteria"

        if json_results['results_found'] > 0:
            for restaurant in json_results['restaurants']:
                if lprice <= restaurant['restaurant']['average_cost_for_two'] < hprice and response_count < 5:
                    restaurant_exist = True
                    response_count += 1
                    response = response + str(response_count) + ". " + \
                               str(restaurant['restaurant']['name']) + " in " + \
                               str(restaurant['restaurant']['location']['address']) + " has been rated " + \
                               str(restaurant['restaurant']['user_rating']['aggregate_rating']) + \
                               " with price range " + str(restaurant['restaurant']['average_cost_for_two']) + "\n"

                if lprice <= restaurant['restaurant']['average_cost_for_two'] < hprice and email_response_count < 10:
                    email_response_count += 1
                    email_response = email_response + str(email_response_count) + ". " + \
                                     "Restaurant Name: " + str(restaurant['restaurant']['name']) + "\n" + \
                                     "Restaurant locality address: " + str(restaurant['restaurant']['location']['address']) + "\n" + \
                                     "Zomato user rating: " + str(restaurant['restaurant']['user_rating']['aggregate_rating']) + "\n" + \
                                     "Average budget for two people: " + str(restaurant['restaurant']['average_cost_for_two']) + "\n\n"

        if response == "":
            dispatcher.utter_message("Sorry there are no restaurant with this criteria. Please select another price range.")
            return [SlotSet('price',None),SlotSet('restaurant_exist' , restaurant_exist)]
            #return {"price": None}
        else:
            dispatcher.utter_message("\n"+"Showing you top rated restaurants:" + "\n"+"\n" + response + "\n"+"\n")
            #dispatcher.utter_message(template="utter_ask_email")
            return [SlotSet('location' , loc) , SlotSet('restaurant_exist' , restaurant_exist)]


class RestaurantForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "restaurant_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["location" , "cuisine" , "price"]

    def slot_mappings(self) -> Dict[Text , Union[Dict , List[Dict]]]:
        """A dictionary to map required slots to
			- an extracted entity
			- intent: value pairs
			- a whole message
			or a list of them, where a first match will be picked"""
        return {
            "location": self.from_entity(entity="location" , intent=["restaurant_search"]) ,
            "cuisine": self.from_entity(entity="cuisine" , intent=["restaurant_search"]) ,
            "price": self.from_entity(entity="price" , intent=["restaurant_search"]) ,
            "email": self.from_entity(entity="email" , intent=["send_email"])
        }

    @staticmethod
    def location_db() -> List[Text]:
        """Database of supported location"""
        return [
            "ahmedabad" , "bangalore" , "bengaluru" , "chennai" , "delhi" ,
            "hyderabad" ,"kolkata" , "mumbai" , "pune" ,  "agra" ,
            "ajmer" , "aligarh" , "amravati" , "amritsar" , "asansol" , "aurangabad" , "bareilly" , "belgaum" ,
            "belagavi" , "bhavnagar" , "bhiwandi" , "bhopal" , "bhubaneswar" , "bikaner" , "bilaspur" ,
            "bokaro steel city" ,
            "chandigarh" , "coimbatore" , "kovai" , "cuttack" , "dehradun" , "dera doon" , "dhanbad" , "bhilai" ,
            "durgapur" , "erode" ,
            "faridabad" , "firozabad" , "ghaziabad" , "gorakhpur" , "gulbarga" , "kalaburagi" ,
            "guntur" , "gwalior" , "gurgaon" , "guwahati" , "hamirpur" , "hubli-dharwad" , "hubballi" ,
            "dharwad" , "indore" , "jabalpur" , "jaipur" , "jalandhar" , "jammu" , "jamnagar" , "jamshedpur" ,
            "jhansi" ,"jodhpur" , "kakinada" , "kannur" , "kanpur" , "kochi" , "cochin" , "kolhapur" , "kollam" ,
            "kozhikode" , "calicut" , "kurnool" , "ludhiana" , "lucknow" , "madurai" , "madura" , "malappuram" ,
            "mathura" , "goa" , "mangalore" , "mangaluru" , "meerut" , "moradabad" , "mysore" , "nagpur" ,
            "nanded" , "nashik" , "nellore" , "noida" ,
            "patna" , "pondicherry" , "purulia" , "prayagraj" , "prayag" , "allahabad" , "illahabad" , "raipur" ,
            "rajkot" , "rajahmundry" , "rajamahendravaram" , "ranchi" , "rourkela" , "salem" , "sangli" ,
            "shimla" , "siliguri" , "solapur" , "srinagar" , "surat" , "thiruvananthapuram" ,
            "thrissur" , "trichur" , "tiruchirappalli" , "tiruppur" , "tirupur" , "ujjain" ,
            "bijapur" , "vijayapura" , "vadodara"  , "varanasi" , "Kashi" , "vasai-virar city" , "vijayawada" , "visakhapatnam" , "vellore" , "warangal"
        ]

    def validate_location(
            self ,
            value: Text ,
            dispatcher: CollectingDispatcher ,
            tracker: Tracker ,
            domain: Dict[Text , Any] ,
    ) -> Dict[Text , Any]:
        """Validate cuisine value."""
        try:
            #print("location fetched:" , value,type(value))
            if isinstance(value , list):
                value = str(list(set(value))[0])

            #print("after removing:",value,type(value))
            if value.lower() in self.location_db():
                # validation succeeded, set the value of the "cuisine" slot to value
                return {"location": value}
            else:
                dispatcher.utter_message(template="utter_city_notfound")
                # validation failed, set this slot to None, meaning the
                # user will be asked for the slot again
                return {"location": None}
        except:
            dispatcher.utter_message(template="utter_city_notfound")
            return {"location": None}

    @staticmethod
    def cuisine_db() -> List[Text]:
        """Database of supported cuisine"""
        return ["chinese" , "mexican" , "italian" , "american" , "south indian" , "north indian"]

    def validate_cuisine(
            self ,
            value: Text ,
            dispatcher: CollectingDispatcher ,
            tracker: Tracker ,
            domain: Dict[Text , Any] ,
    ) -> Dict[Text , Any]:
        """Validate cuisine value."""
        try:
            #print("Cuisine fetched:" , value,list(set(value)),type(value))
            if isinstance(value , list):
                value = str(list(set(value))[0])

            if value.lower() in self.cuisine_db():
                # validation succeeded, set the value of the "cuisine" slot to value
                return {"cuisine": value}
            else:
                dispatcher.utter_message(template="utter_cuisine_notfound")
                # validation failed, set this slot to None, meaning the
                # user will be asked for the slot again
                return {"cuisine": None}
        except:
            dispatcher.utter_message(template="utter_cuisine_notfound")
            return {"cuisine": None}

    ### Validation of Price Range ###
    @staticmethod
    def price_db() -> List[Text]:
        """Database of supported cuisine"""
        return ["lesser than 300","300 to 700","more than 700"]

    def validate_price(
            self ,
            value: Text ,
            dispatcher: CollectingDispatcher ,
            tracker: Tracker ,
            domain: Dict[Text , Any] ,
    ) -> Dict[Text , Any]:
        """Validate cuisine value."""
        try:
            #print("price fetched:" , value , list(set(value)) , type(value))
            if isinstance(value , list):
                value = str(list(set(value))[0])

            if value.lower() in self.price_db():
                # validation succeeded, set the value of the "cuisine" slot to value
                return {"price": value}
            else:
                dispatcher.utter_message(template="utter_price_notfound")
                # validation failed, set this slot to None, meaning the
                # user will be asked for the slot again
                return {"price": None}
        except:
            dispatcher.utter_message(template="utter_price_notfound")
            return {"price": None}

    def submit(
            self ,
            dispatcher: CollectingDispatcher ,
            tracker: Tracker ,
            domain: Dict[Text , Any] ,
    ) -> List[Dict]:
        """Define what the form has to do
		after all required slots are filled"""

        # utter submit template
        #dispatcher.utter_message(template="utter_pleasewait")
        # dispatcher.utter_message()
        return []

class actionsendemail(Action):
    def name(self):
        return 'action_send_email'

    def run(self , dispatcher , tracker , domain):
        global email_response

        cuisine = tracker.get_slot('cuisine')
        loc = tracker.get_slot('location')
        email = tracker.get_slot('email')
        email_subj = "Top " + cuisine.capitalize() + " restaurants in " + loc.capitalize()
        email_msg = "Hi there! Here are the " + email_subj + "." + "\n\n" + \
                    email_response + "\n\n" + "Thanks for using services from 'Foodie'"

        app = Flask(__name__)
        app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        app.config['MAIL_PORT'] = 465
        app.config['MAIL_USERNAME'] = 'upgrad.aiml@gmail.com'
        app.config['MAIL_PASSWORD'] = 'Upgrad123'
        app.config['MAIL_USE_SSL'] = True
        mail = Mail(app)

        with app.app_context():
            try:
                msg = Message(email_subj ,
                              sender="upgrad.aiml@gmail.com" ,
                              recipients=[email])
                msg.body = email_msg
                mail.send(msg)
                dispatcher.utter_message("Email has been sent..!!")
            except Exception as e:
                #print("step3")
                dispatcher.utter_message("It seems there is some issue with email id so could not send the email to given email ID..!!")
            # return str(e)
            dispatcher.utter_message(template="utter_goodbye")
        return []