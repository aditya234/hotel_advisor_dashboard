import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import math


class DataOperations:
    def __init__(self):
        self.data = None
        self.cities = []
        # loading json data from file
        f1 = open('./data/tokyo_hotels.json', "r")
        data1 = json.loads(f1.read())
        f1.close()

        f2 = open('./data/london_hotels.json', "r")
        data2 = json.loads(f2.read())
        f1.close()

        f3 = open('./data/singapore_hotels.json', "r")
        data3 = json.loads(f3.read())
        f1.close()

        # adding data into dataframe
        self.add_city(data1, 'Tokyo')
        self.add_city(data2, 'London')
        self.add_city(data3, 'Singapore')

        # process data
        self.process_data()

    def add_city(self, json_data, city):
        df_new = pd.json_normalize(json_data)
        df_new['city'] = city
        self.cities.append(city)
        if self.data is None:
            self.data = df_new
        else:
            self.data = self.data.append(df_new)

    def process_data(self):
        # data manipulation and cleaning
        self.data = self.data.drop(['reviews', 'top_cuisines'], axis=1)

        self.data.languages = self.data.languages.apply(lambda x: (str(x)).split(", "))

        self.data.review_count = self.data.review_count.apply(lambda x: (str(x)).split()[0])

        self.data.hotel_rank = self.data.hotel_rank.apply(lambda x: (str(x)).split()[0][1:])

        self.data['cuisines'] = self.data.restaurants.apply(self.group_cuisines)

        self.data['restaurant_names'] = self.data.restaurants.apply(self.restaurant_names)
        self.data = self.data.drop(['restaurants'], axis=1)

        # data type fixing
        self.data.rating = self.data.rating.apply(lambda x: float(x) if self.isfloat(x) else np.nan)
        self.data.review_count = self.data.review_count.apply(lambda x: int(x) if self.isint(x) else np.nan)
        self.data.hotel_rank = self.data.hotel_rank.apply(lambda x: int(x) if self.isint(x) else np.nan)
        self.data.price = self.data.price.apply(lambda x: float(x) if self.isfloat(x) else np.nan)
        self.data.restraunts_nearby = self.data.restraunts_nearby.apply(lambda x: int(x) if self.isint(x) else np.nan)
        self.data.attractions_nearby = self.data.attractions_nearby.apply(lambda x: int(x) if self.isint(x) else np.nan)
        self.data.good_for_walkers_out_of_100 = self.data.good_for_walkers_out_of_100.apply(
            lambda x: int(x) if self.isint(x) else np.nan)

    # filters
    def set_amenity_filter(self, dFrame, amenity_list):
        mask = dFrame.amenities.apply(lambda x: any(item for item in amenity_list if item in x))
        return dFrame[mask]

    def set_language_filter(self, dFrame, language_list):
        mask = dFrame.languages.apply(lambda x: any(item for item in language_list if item in x))
        return dFrame[mask]

    def set_class_filter(self, dFrame, class_list):
        mask = dFrame.hotel_class.apply(lambda x: any(item for item in class_list if item in x))
        return dFrame[mask]

    def set_cuisine_filter(self, dFrame, cuisine_list):
        mask = dFrame.cuisines.apply(lambda x: any(item for item in cuisine_list if item in x.keys()))
        return dFrame[mask]

    def set_rating_filter(self, dFrame, min_rating):
        return dFrame[dFrame.rating >= min_rating]

    def set_review_filter(self, dFrame, min_reviews):
        return dFrame[dFrame.review_count >= min_reviews]

    def set_rank_filter(self, dFrame, max_rank):
        return dFrame[dFrame.hotel_rank <= max_rank]

    def set_price_filter(self, dFrame, max_price):
        return dFrame[dFrame.price <= max_price]

    def set_restraunts_nearby_filter(self, dFrame, min_restraunts_nearby):
        return dFrame[dFrame.restraunts_nearby >= min_restraunts_nearby]

    def set_attractions_nearby_filter(self, dFrame, min_attractions_nearby):
        return dFrame[dFrame.attractions_nearby >= min_attractions_nearby]

    def set_good_for_walkers_out_of_100_filter(self, dFrame, min_good_for_walkers_out_of_100):
        return dFrame[dFrame.good_for_walkers_out_of_100 <= min_good_for_walkers_out_of_100]

    def set_city_filter(self, dFrame, cities):
        return dFrame[dFrame.city.isin(cities)]

    # sorting df
    def sort_df(self, dFrame):
        result = dFrame.sort_values(by=['price'], ascending=True)
        result = result.sort_values(by=['hotel_rank'], ascending=True)
        result = result.sort_values(by=['rating'], ascending=False)
        return result

    # get filter data
    def get_all_amenities(self, dFrame):
        amenities = {}
        for index, row in dFrame.iterrows():
            for amenity in row['amenities']:
                if amenity is not None and amenity != 'None':
                    if amenity in amenities.keys():
                        amenities[amenity] += 1
                    else:
                        amenities[amenity] = 1
        # sorting in descending order
        sorted(amenities.items(), key=lambda x: x[1], reverse=True)
        return amenities

    def get_all_languages(self, dFrame):
        languages = {}
        for index, row in dFrame.iterrows():
            for language in row['languages']:
                if language is not None and language != 'None':
                    if language in languages:
                        languages[language] += 1
                    else:
                        languages[language] = 1
        # sorting in descending order
        languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)
        return languages

    def get_all_classes(self, dFrame):
        classes = {}
        for index, row in dFrame.iterrows():
            for hotel_class in row['hotel_class']:
                if hotel_class is not None and hotel_class != 'None':
                    if hotel_class in classes:
                        classes[hotel_class] += 1
                    else:
                        classes[hotel_class] = 1
        # sorting in descending order
        classes = sorted(classes.items(), key=lambda x: x[1], reverse=True)
        return classes

    def get_all_cuisines(self, dFrame):
        cuisines = {}
        for index, row in dFrame.iterrows():
            for cuisine, count in row['cuisines'].items():
                if cuisine is not None and cuisine != 'None':
                    if cuisine in cuisines.keys():
                        cuisines[cuisine] += 1
                    else:
                        cuisines[cuisine] = 1
        # sorting in descending order
        cuisines = sorted(cuisines.items(), key=lambda x: x[1], reverse=True)
        return cuisines

    def get_all_restaurants(self, dFrame):
        restaurants = {}
        for index, row in dFrame.iterrows():
            for restaurant in row['restaurant_names']:
                if restaurant is not None and restaurant != 'None':
                    if restaurant in restaurants:
                        restaurants[restaurant] += 1
                    else:
                        restaurants[restaurant] = 1
        # sorting in descending order
        restaurants = sorted(restaurants.items(), key=lambda x: x[1], reverse=True)
        return restaurants

    # helpers
    def group_cuisines(self, restaurant_list):
        cuisines = {}
        if type(restaurant_list) == list:
            for restaurant in restaurant_list:
                for cuisine in restaurant['cusines']:
                    cuisine = cuisine.replace(", ", "")
                    cuisine = cuisine.replace(",", "")
                    cuisine = cuisine.strip()
                    if len(cuisine) > 2:
                        if cuisine in cuisines.keys():
                            cuisines[cuisine] += 1
                        else:
                            cuisines[cuisine] = 1
            # sorting in descending order
            sorted(cuisines.items(), key=lambda x: x[1], reverse=True)
        return cuisines

    def restaurant_names(self, restaurant_list):
        restaurants = []
        if type(restaurant_list) == list:
            for restaurant in restaurant_list:
                restaurants.append(restaurant['name'])
        return restaurants

    def isfloat(self, num):
        if num is None or num is np.nan:
            return False
        try:
            float(num)
            return True
        except ValueError:
            return False

    def isint(self, num):
        if num is None or num is np.nan:
            return False
        try:
            int(num)
            return True
        except ValueError:
            return False


# # testing
# if __name__ == "__main__":
#     data_operations = DataOperations()
#     print(data_operations.set_class_filter(dFrame=data_operations.data, class_list=['Budget']))
