import json
import requests
import datetime


def get_menu():
    # get today's date
    year = datetime.date.today().year
    month = datetime.date.today().month
    day = datetime.date.today().day

    # build url
    url = f'https://menu.dartmouth.edu/menuapi/mealitems?dates={year}{month:02d}{day:02d}'

    # make request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # parse the JSON response
        data = response.json()

        # number for item list
        num = 1

        # initialize the two arrays to be returned
        lunch = []
        dinner = []

        # extract information about each menu item
        for meal_item in data['mealItems']:

            item_id = meal_item['id']
            item_name = meal_item['itemName']
            main_location_label = meal_item['mainLocationLabel']
            menu_category = meal_item['menuCategory']
            ingredients = meal_item.get('ingredients', 'N/A')
            nutrients = meal_item.get('nutrients', [])
            datesAvailable = meal_item['datesAvailable']
            subLocation = datesAvailable[0]['menus'][0]['subLocation']
            recipeCategory = meal_item['recipeCategory']

            # get periods
            period = datesAvailable[0]['menus'][0]['mealPeriod']

            # Print or process the extracted information as needed
            if main_location_label == "53 Commons" and \
                    subLocation == "Ma Thayer's" and \
                    "Entrees" in recipeCategory and \
                    period in ["Dinner", "Lunch"]:
                
                if period == "Lunch":
                    lunch.append(item_name)
                else:
                    dinner.append(item_name)

                num += 1

        return lunch, dinner

    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code}, {response.text}")

        return [], []
