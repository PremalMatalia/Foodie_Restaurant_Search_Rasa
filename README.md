# Foodie_Restaurant_Search_Rasa
Rasa framework based Restaurant search

#### Restaurant Bot :

A restaurant chatbot using open source chat framework RASA : https://rasa.com/. Integrates with Zomato : https://developers.zomato.com/?lang=tr API to fetch restaurant information. 

#### Problem Statement:
An Indian startup named 'Foodie' wants to build a conversational bot (chatbot) which can help users discover restaurants across several Indian cities. You have been hired as the lead data scientist for creating this product.

The main purpose of the bot is to help users discover restaurants quickly and efficiently and to provide a good restaurant discovery experience. The project brief provided to you is as follows.

The bot takes the following inputs from the user:
**City:** Take the input from the customer as a text field. For example:
**Bot:** In which city are you looking for restaurants?
**User:** anywhere in Delhi

#### Important Notes:
Assume that Foodie works only in Tier-1 and Tier-2 cities. You can use the current HRA classification of the cities from here. Under the section 'current classification' on this page, the table categorizes cities as X, Y and Z. Consider 'X ' cities as tier-1 and 'Y' as tier-2. The bot should be able to identify common synonyms of city names, such as Bangalore/Bengaluru, Mumbai/Bombay etc.

Your chatbot should provide results for tier-1 and tier-2 cities only, while for tier-3 cities, it should reply back with something like "We do not operate in that area yet".

**Cuisine Preference:** Take the cuisine preference from the customer. The bot should list out the following six cuisine categories (Chinese, Mexican, Italian, American, South Indian & North Indian) and the customer can select any one out of that. Following is an example for the same:

Bot: What kind of cuisine would you prefer?
Chinese 

Mexican 

Italian 

American 

South Indian 

North Indian
User: I’ll prefer Italian!

**Average budget for two people:** Segment the price range (average budget for two people) into three price categories: 
lesser than 300, 300 to 700 and more than 700. 
The bot should ask the user to select one of the three price categories. For example:

Bot: What price range are you looking at?
**Lesser than Rs. 300 
Rs. 300 to 700 
More than 700**
User: in range of 300 to 700

**NLU training:** One can use rasa-nlu-trainer to create more training examples for entities and intents. Try using regex features and synonyms for extracting entities.

**Build actions for the bot:** Read through the Zomato API documentation to extract the features such as the average price for two people and restaurant’s user rating. One can also build an ‘action’ for sending emails from Python.

**Creating more stories:** Use train_online.py file to create more stories. Refer to the sample conversational stories provided above.


