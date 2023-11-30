import requests
import datetime
import pytz


def get_menu():

    local_timezone = pytz.timezone('EST')  # Replace 'Your_Local_Timezone' with your actual time zone
    today = datetime.datetime.now(local_timezone).date()
    today_format = f"{today.year}{today.month:02d}{today.day:02d}"

    # build url
    # url = f'https://menu.dartmouth.edu/menuapi/mealitems?dates={today_format}'
    url = 'https://menu.dartmouth.edu/menuapi/mealitems?dates=20231117'

    # make request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # parse the JSON response
        data = response.json()


        # initialize the two arrays to be returned
        lunch = []
        dinner = []
        collis_spec = []
        collis_soup = []
        hop_spec = []

        # extract information about each menu item
        for meal_item in data['mealItems']:

            item_name = meal_item['itemName']
            main_location_label = meal_item['mainLocationLabel']
            datesAvailable = meal_item['datesAvailable']
            recipeCategory = meal_item['recipeCategory']

            # get info from datesAvailable if it's a list (sometimes it isn't)
            if type(datesAvailable) is list:
                subLocation = datesAvailable[0]['menus'][0]['subLocation']
                period = datesAvailable[0]['menus'][0]['mealPeriod']

            # Print or process the extracted information as needed
            if main_location_label == "53 Commons" and \
                    subLocation == "Ma Thayer's" and \
                    period in ["Dinner", "Lunch"]:
                
                if period == "Lunch":
                    lunch.append(item_name)
                else:
                    dinner.append(item_name)

            # pull collis menu data
            if main_location_label == "Collis Caf\u00e9":
                if "Soup" in recipeCategory:
                    collis_soup.append(item_name)
                
                if "Entrees" in recipeCategory:
                    collis_spec.append(item_name)

            if main_location_label == "Courtyard Caf\u00e9" and \
                datesAvailable and \
                len(datesAvailable) == 1:
                hop_spec.append(item_name)


        menu_dict = {'lunch':lunch, 'dinner':dinner, 'collis_soup':collis_soup, 'collis_spec':collis_spec, 'hop_spec':hop_spec}

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