## Check point: User agrees for restaurant details with emailid
> check_email_question
* send_email{"email": "premal.matalia@gmail.com"}
    - slot{"email": "premal.matalia@gmail.com"}
    - action_send_email
	- action_restart
	
## Check point: User agrees for restaurant details but didn't provide emailid
> check_email_question
* affirm
    - utter_ask_emailid
* send_email{"email": "abcd.1890@facebook.com"}
    - slot{"email": "abcd.1890@facebook.com"}
    - action_send_email
	- action_restart
	
## Check point: User denies for restaurant detials on email
> check_email_question
* deny
    - utter_goodbye
	- action_restart

## Check point: 
> check_restaurant_found
    - slot{"price": null}
    - slot{"restaurant_exist": false}
    - utter_ask_price
* restaurant_search{"price": "More than 700"}
    - restaurant_form
    - form{"name": "restaurant_form"}
    - slot{"location": "mumbai"}
    - slot{"cuisine": "italian"}
    - slot{"price": "More than 700"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_search_restaurants


## interactive_story --> Happy path: Story with no entity provided
* greet
    - utter_greet
* restaurant_search
    - restaurant_form
    - form{"name": "restaurant_form"}
    - slot{"requested_slot": "location"}
* form: restaurant_search{"location": "pune"}
    - form: restaurant_form
    - slot{"location": "pune"}
    - slot{"requested_slot": "cuisine"}
* form: restaurant_search{"cuisine": "italian"}
    - form: restaurant_form
    - slot{"cuisine": "italian"}
    - slot{"requested_slot": "price"}
* form: restaurant_search{"price": "More than 700"}
    - form: restaurant_form
    - slot{"price": "More than 700"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_search_restaurants
> check_restaurant_found	
    - slot{"location": "pune"}
    - slot{"restaurant_exist": true}
    - utter_ask_email
> check_email_question


## interactive_story --> Happy path: Story with Location provided 
* greet
    - utter_greet
* restaurant_search{"location": "pune"}
    - restaurant_form
    - form{"name": "restaurant_form"}
    - slot{"location": "pune"}
    - slot{"requested_slot": "cuisine"}
* form: restaurant_search{"cuisine": "italian"}
    - form: restaurant_form
    - slot{"cuisine": "italian"}
    - slot{"requested_slot": "price"}
* form: restaurant_search{"price": "300 to 700"}
    - form: restaurant_form
    - slot{"price": "300 to 700"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_search_restaurants
> check_restaurant_found
    - slot{"location": "pune"}
    - slot{"restaurant_exist": true}
    - utter_ask_email
> check_email_question	

## interactive_story --> Happy path: Story with Cuisine provided 
* greet
    - utter_greet
* restaurant_search{"cuisine": "chinese"}
    - restaurant_form
    - form{"name": "restaurant_form"}
    - slot{"cuisine": "chinese"}
    - slot{"requested_slot": "location"}
* form: restaurant_search{"location": "prayagraj"}
    - form: restaurant_form
    - slot{"location": "prayagraj"}
    - slot{"requested_slot": "price"}
* form: restaurant_search{"price": "300 to 700"}
    - form: restaurant_form
    - slot{"price": "300 to 700"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_search_restaurants
> check_restaurant_found	
    - slot{"location": "prayagraj"}
    - slot{"restaurant_exist": true}
    - utter_ask_email
> check_email_question

## interactive_story --> Happy path: Story with price provided 
* greet
    - utter_greet
* restaurant_search{"price": "300 to 700"}
    - restaurant_form
    - form{"name": "restaurant_form"}
    - slot{"price": "300 to 700"}
    - slot{"requested_slot": "location"}
* form: restaurant_search{"location": "nanded"}
    - form: restaurant_form
    - slot{"location": "nanded"}
    - slot{"requested_slot": "cuisine"}
* form: restaurant_search{"cuisine": "south indian"}
    - form: restaurant_form
    - slot{"cuisine": "south indian"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_search_restaurants
> check_restaurant_found	
    - slot{"location": "nanded"}
    - slot{"restaurant_exist": true}
    - utter_ask_email
> check_email_question
	
## interactive_story --> Happy path: Story with Cuisine and Location provided 
* greet
    - utter_greet
* restaurant_search{"cuisine": "italian", "location": "mumbai"}
    - restaurant_form
    - form{"name": "restaurant_form"}
    - slot{"location": "mumbai"}
    - slot{"cuisine": "italian"}
    - slot{"requested_slot": "price"}
* form: restaurant_search{"price": "More than 700"}
    - form: restaurant_form
    - slot{"price": "More than 700"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_search_restaurants
> check_restaurant_found
    - slot{"location": "mumbai"}
    - slot{"restaurant_exist": true}
    - utter_ask_email
> check_email_question
	
	
## interactive_story --> Happy path: Story with price and Location provided 
* greet
    - utter_greet
* restaurant_search{"location": "mathura", "price": "300 to 700"}
    - restaurant_form
    - form{"name": "restaurant_form"}
    - slot{"location": "mathura"}
    - slot{"price": "300 to 700"}
    - slot{"requested_slot": "cuisine"}
* form: restaurant_search{"cuisine": "american"}
    - form: restaurant_form
    - slot{"cuisine": "american"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_search_restaurants
> check_restaurant_found    
	- slot{"location": "mathura"}
    - slot{"restaurant_exist": true}
    - utter_ask_email
> check_email_question

## interactive_story --> Happy path: Story with price and cuisine provided 
* greet
    - utter_greet
* restaurant_search{"cuisine": "north indian", "price": "lesser than 300"}
    - restaurant_form
    - form{"name": "restaurant_form"}
    - slot{"cuisine": "north indian"}
    - slot{"price": "lesser than 300"}
    - slot{"requested_slot": "location"}
* form: restaurant_search{"location": "bhiwandi"}
    - form: restaurant_form
    - slot{"location": "bhiwandi"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_search_restaurants
> check_restaurant_found
    - slot{"location": "bhiwandi"}
    - slot{"restaurant_exist": true}
    - utter_ask_email
> check_email_question

## interactive_story --> Happy path: Story with location, price and cuisine provided
* greet
    - utter_greet
* restaurant_search{"cuisine": "italian", "location": "mumbai", "price": "lesser than 300"}
    - restaurant_form
    - form{"name": "restaurant_form"}
    - slot{"location": "mumbai"}
    - slot{"cuisine": "italian"}
    - slot{"price": "lesser than 300"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_search_restaurants
> check_restaurant_found
	- slot{"location": "bhiwandi"}
    - slot{"restaurant_exist": true}
    - utter_ask_email
> check_email_question