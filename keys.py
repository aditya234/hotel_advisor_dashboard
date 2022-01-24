from data_operations import DataOperations


class KeyStrings:
    # ---- SIDEBAR KEYS-----
    CITY_FILTER = 'CITY_FILTER'
    RATINGS_FILTER = 'RATINGS_FILTER'
    PRICE_FILTER = 'PRICE_FILTER'
    CUISINE_FILTER = 'CUISINE_FILTER'
    NEARBY_PLACES_FILTER = 'NEARBY_PLACES_FILTER'
    NEARBY_RESTAURANTS_FILTER = 'NEARBY_RESTAURANTS_FILTER'
    REVIEWS_FILTER = 'REVIEWS_FILTER'
    AMENITIES_FILTER = 'AMENITIES_FILTER'
    LANGUAGES_FILTER = 'LANGUAGES_FILTER'
    CLASS_FILTER = 'CLASS_FILTER'


class DashboardDataManager:
    def __init__(self):
        self.data_operations = DataOperations()
        self.cities = self.data_operations.cities
        self.data = self.data_operations.data.copy()
        self.set_thresholds()

    def set_thresholds(self):
        ## calculating thresholds
        self.max_price = (self.data.price.max() // 1000) * 1000  # 32231
        self.max_nearby_places = (self.data.attractions_nearby.max() // 100) * 100  # 380
        self.max_restaurants_nearby = (self.data.restraunts_nearby.max() // 600) * 600  # 3925
        self.max_review_count = (self.data.review_count.max() // 100) * 100  # 725

    def get_filter_data(self):
        self.cuisines = ['NA'] + self.get_list_from_map(self.data_operations.get_all_cuisines(dFrame=self.data))
        self.amenities = ['NA'] + self.get_list(self.data_operations.get_all_amenities(dFrame=self.data))
        self.languages = ['NA'] + self.get_list(self.data_operations.get_all_languages(dFrame=self.data))
        self.classes = ['NA'] + self.get_list(self.data_operations.get_all_classes(dFrame=self.data))

    def set_filters(self, cities, rating, price, cuisine, nearby_places, nearby_restaurants, total_reviews, amenities,
                    languages, hotel_classes):
        self.data = self.data_operations.data.copy()
        # city filter
        if len(cities) > 0:
            self.data = self.data_operations.set_city_filter(dFrame=self.data, cities=cities)
        # rating filter
        if rating != 'All':
            rating_map = {
                '5': 5,
                '4 and above': 4,
                '3 and above': 3,
                '2 and above': 2,
                '1 and above': 1,
            }
            self.data = self.data_operations.set_rating_filter(dFrame=self.data, min_rating=rating_map[rating])
        # price filter
        if price < self.max_price:
            self.data = self.data_operations.set_price_filter(dFrame=self.data, max_price=price)
        # cuisine filter
        if 'NA' not in cuisine and len(cuisine) > 0:
            self.data = self.data_operations.set_cuisine_filter(dFrame=self.data, cuisine_list=cuisine)
        # nearby places filter
        if nearby_places < self.max_nearby_places:
            self.data = self.data_operations.set_attractions_nearby_filter(dFrame=self.data,
                                                                           min_attractions_nearby=nearby_places)
        # nearby restaurants filter
        if nearby_restaurants < self.max_restaurants_nearby:
            self.data = self.data_operations.set_restraunts_nearby_filter(dFrame=self.data,
                                                                          min_restraunts_nearby=nearby_restaurants)
        # reviews filter
        if total_reviews < self.max_review_count:
            self.data = self.data_operations.set_review_filter(dFrame=self.data, min_reviews=total_reviews)
        # amenities filter
        if 'NA' not in amenities and len(amenities) > 0:
            self.data = self.data_operations.set_amenity_filter(dFrame=self.data, amenity_list=amenities)
        # languages filter
        if 'NA' not in languages and len(languages) > 0:
            self.data = self.data_operations.set_language_filter(dFrame=self.data, language_list=languages)
        # class filter
        if 'NA' not in hotel_classes and len(hotel_classes) > 0:
            self.data = self.data_operations.set_class_filter(dFrame=self.data, class_list=hotel_classes)

    def get_list(self, map_list):
        result = []
        for x in map_list:
            result.append(x)
        return result

    def get_list_from_map(self,map_list):
        result = []
        for value in map_list:
            result.append(value[0])
        return result

    def get_top_cusine(self):
        result = self.data_operations.get_all_cuisines(dFrame=self.data)
        if result is not None and len(result) > 0:
            return result[0][0]
        else:
            return "NA"

    def get_top_language(self):
        result = self.data_operations.get_all_languages(dFrame=self.data)
        if result is not None and len(result) > 0:
            return result[0][0]
        else:
            return "NA"

    def get_restaurants(self):
        result = self.data_operations.get_all_restaurants(dFrame=self.data)
        if result is not None and len(result) > 0:
            return result[0][0]
        else:
            return "NA"

    def get_attractions(self):
        result = self.data_operations.get_all_attractions(dFrame=self.data)
        if result is not None and len(result) > 0:
            return result[0][0]
        else:
            return "NA"

    def get_class(self):
        result = self.data_operations.get_all_classes(dFrame=self.data)
        if result is not None and len(result) > 0:
            return result[0][0]
        else:
            return "NA"

    def get_top_20_hotels(self):
        total_enteries = self.data.shape[0]
        loop_itr_num = 0
        result = {}
        if total_enteries > 20:
            loop_itr_num = 20
        else:
            loop_itr_num = total_enteries

        if total_enteries != 0:
            counter = 0
            sorted_df = self.data_operations.sort_df(self.data)
            for index, row in sorted_df.iterrows():
                if counter == 20:
                    break
                else:
                    counter += 1
                result[row['hotel_name']] = 100 - (3* counter)

        self.top_20 = result

    def get_nearby_places_avg(self):
        avg = self.data.attractions_nearby.mean()
        try:
            return f"{int(avg)} (on avg.)"
        except:
            return "NA"
# ------
import numpy as np
import pandas as pd


class DummyData:
    donut_data = {'India': 4500,
                  'Australia': 2500,
                  'Japan': 1053,
                  'America': 500,
                  'Russia': 3200}
    bar_data = pd.DataFrame(dict(
        X_axis=[i for i in range(100)],
        Y_axis=np.random.randint(10, 50, 100)
    ))
