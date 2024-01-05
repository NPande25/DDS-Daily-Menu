import requests
import datetime
import pytz
import json

def get_menu():
    # Use Python timezone library to ensure Eastern Time
    local_timezone = pytz.timezone('EST')
    
    # Get today's date in the required format
    today = datetime.datetime.now(local_timezone).date()
    today_format = f"{today.year}{today.month:02d}{today.day:02d}"

    # Build URL for the API request
    url = f'https://menu.dartmouth.edu/menuapi/mealitems?dates={today_format}'

    # Make request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = json.loads(response.text)

        # Initialize lists to be returned
        lunch, dinner, collis_spec, collis_soup, hop_spec = [], [], [], [], []

        # Extract information about each menu item
        for meal_item in data['mealItems']:

            item_name = meal_item['itemName']
            main_location_label = meal_item['mainLocationLabel']
            dates_available = meal_item['datesAvailable']
            recipe_category = meal_item['recipeCategory']
            ingredients = meal_item['ingredients']

            # Get info from dates_available if it's a list (sometimes it isn't)
            if isinstance(dates_available, list) and dates_available:
                sub_location = dates_available[0]['menus'][0]['subLocation']
                date = dates_available[0]['menus']
                period = dates_available[0]['menus'][0]['mealPeriod']

            # Check conditions once and store the result
            is_commons = main_location_label == "53 Commons"
            is_thayers = sub_location == "Ma Thayer's"
            is_specials = sub_location == "Specials"
            is_collis = main_location_label == "Collis Caf\u00e9"
            is_valid_period = period in {"Dinner", "Lunch"}  # use a set for membership test
            is_not_menu_header = "Menu Header" not in recipe_category

            # Use the stored results in your conditions
            if is_commons and is_thayers and is_valid_period and is_not_menu_header:
                if period == "Lunch":
                    lunch.append(item_name)
                else:
                    dinner.append(item_name)

            # Pull Collis menu data
            if is_collis and is_specials and len(dates_available) < 3 \
                and "Sandwiches" not in recipe_category:
                if "Soup" in recipe_category:
                    collis_soup.append(item_name)

                if "Entrees" in recipe_category:
                    collis_spec.append(item_name)

            if (
                main_location_label == "Courtyard Caf\u00e9"
                and dates_available
                and len(dates_available) < 5
            ):
                hop_spec.append(item_name)

        menu_dict = {
            'lunch': lunch,
            'dinner': dinner,
            'collis_soup': collis_soup,
            'collis_spec': collis_spec,
            'hop_spec': hop_spec,
        }

        # Replace empty lists with "None today"
        for key, value in menu_dict.items():
            if not value:  # Check if the list is empty
                value.append("None today")

        return menu_dict

    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code}, {response.text}")
        return {}

print(get_menu())
