import requests
import datetime
import pytz
import json
import os

CACHE_FILE_PATH = 'api_cache.json'
local_timezone = pytz.timezone('EST')


def get_menu():
    # Check if there's a cached response
    if os.path.exists(CACHE_FILE_PATH):
        with open(CACHE_FILE_PATH, 'r') as cache_file:
            cached_data = json.load(cache_file)
            # Check if the cached data is still valid (e.g., not too old)
            if datetime.datetime.now(local_timezone).strftime("%Y-%m-%d") in cached_data['dates']:
                return process_menu_data(cached_data)

                
    # If no valid cache, fetch data from the API
    today = datetime.datetime.now(local_timezone).date()
    today_format = f"{today.year}{today.month:02d}{today.day:02d}"
    url = f'https://menu.dartmouth.edu/menuapi/mealitems?dates={today_format}'
    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.text)
        # Cache the response for future use
        with open(CACHE_FILE_PATH, 'w') as cache_file:
            json.dump(data, cache_file)
        
        return process_menu_data(data)

    else:
        print(f"Error: {response.status_code}, {response.text}")
        return {}

def process_menu_data(data):

    # Initialize lists to be returned
    lunch, dinner, collis_spec, collis_soup, hop_spec = [], [], [], [], []

    # Extract information about each menu item
    for meal_item in data['mealItems']:

        item_name = meal_item['itemName']
        main_location_label = meal_item['mainLocationLabel']
        dates_available = meal_item['datesAvailable']
        recipe_category = meal_item['recipeCategory']
        # ingredients = meal_item['ingredients']

        # Get info from dates_available if it's a list (sometimes it isn't)
        if isinstance(dates_available, list) and dates_available:
            sub_location = dates_available[0]['menus'][0]['subLocation']
            date = dates_available[0]['menus']
            for item in dates_available:
                if item['date'] == datetime.datetime.now(local_timezone).strftime("%Y%m%d"):
                    period = item['menus'][0]['mealPeriod']

        # Check conditions once and store the result
        is_foco = main_location_label == "53 Commons"
        is_thayers = sub_location == "Ma Thayer's"
        is_specials = sub_location == "Specials"
        is_collis = main_location_label == "Collis Caf\u00e9"
        is_valid_period = period in {"Dinner", "Lunch"}  # use a set for membership test
        is_not_menu_header = "Menu Header" not in recipe_category

 
        # Use the stored results in your conditions
        if is_foco and is_thayers and is_valid_period and is_not_menu_header:
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


if __name__ == "__main__":
	print(get_menu())
