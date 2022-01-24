import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import math


class Restaurant:
    def __init__(self, data):
        self.name = data['name'] if 'name' in data else None
        self.cusines = data['cusines'] if 'cusines' in data else []
        self.total_reviews = []
        if ('reviews' in data) and data['reviews']:
            data_list = data['reviews'].split()
            self.total_reviews = int((data_list[0]).replace(',', '')) if len(data_list) > 0 else None


class Hotel:
    def __init__(self, data, city=''):
        self.city = city
        self.name = data['hotel_name'] if 'hotel_name' in data else None

        self.rating = (float(data['rating']) if data['rating'] and data[
            'rating'].isnumeric() else None) if 'rating' in data else None

        self.review_count = None
        if ('review_count' in data) and data['review_count']:
            data_list = data['review_count'].split()
            self.review_count = int(data_list[0]) if len(data_list) > 0 and data_list[0].isnumeric() else None

        self.hotel_rank = None
        if ('hotel_rank' in data) and data['hotel_rank']:
            data_list = data['hotel_rank'].split()
            self.hotel_rank = int(data_list[0][1:]) if len(data_list) > 0 and data_list[0].isnumeric() else None

        self.total_hotels = []
        if ('hotel_rank' in data) and data['hotel_rank']:
            data_list = data['hotel_rank'].split()
            self.total_hotels = int(data_list[2]) if len(data_list) > 2 and data_list[2].isnumeric() else None

        self.best_price = (int(data['price']) if data['price'] else None) if 'price' in data else None
        self.restaurants_nearby = int(data['restraunts_nearby']) if (
                'restraunts_nearby' in data and data['restraunts_nearby']) else None
        self.attractions_nearby = int(data['attractions_nearby']) if (
                'attractions_nearby' in data and data['attractions_nearby']) else None
        self.good_for_walkers_out_of_100 = int(data['good_for_walkers_out_of_100']) if (
                'good_for_walkers_out_of_100' in data and data['good_for_walkers_out_of_100']) else None

        self.amenities = data['amenities'] if 'amenities' in data else []
        self.languages = (data['languages'].split(", ") if data['languages'] else []) if 'languages' in data else []
        self.hotel_classes = data['hotel_class'] if 'hotel_class' in data else []
        self.best_price_source = data['best_price_source'] if 'best_price_source' in data else None
        self.top_cuisines = data['top_cuisines'] if 'top_cuisines' in data else []
        self.restaurants = []
        if ('restaurants' in data) and data['restaurants']:
            for restaurant in data['restaurants']:
                self.restaurants.append(Restaurant(restaurant))

        self.cuisines = {}
        for restaurant in self.restaurants:
            for cuisine in restaurant.cusines:
                if cuisine in self.cuisines.keys():
                    self.cuisines[cuisine] += 1
                else:
                    self.cuisines[cuisine] = 1


class HotelList:
    def __init__(self):
        self.hotels = []
        self.filter_hotels_list = []
        # default filter values
        self.filter_cities = []
        self.filter_min_rating = 1
        self.filter_max_hotel_price = 9999999999999  # taking a very-very large price by default
        self.filter_cuisines = None

    def add_city_data(self, json_data, city):
        for hotel in json_data:
            self.hotels.append(Hotel(data=hotel, city=city))
        self.filter_hotels_list = self.hotels[:]  # copying list by value
        self.filter_cities.append(city)

    def getHotelsByCity(self, cities):
        # filter loop
        temp_hotels = self.filter_hotels_list[:]  # copy by value
        for hotel in temp_hotels:
            # taking cities into account
            if cities is not None:
                self.filter_cities = cities
            if hotel.city not in self.filter_cities:
                continue

            # taking min_rating into account
            if min_rating is not None:
                self.filter_min_rating = min_rating
            if hotel.rating < self.filter_min_rating:
                continue

            # taking max_hotel_price into account
            if max_hotel_price is not None:
                self.filter_max_hotel_price = max_hotel_price
            if hotel.best_price > self.filter_max_hotel_price:
                continue

            # taking cuisines into account
            if cuisines is not None:
                self.filter_cuisines = cuisines
                if len(hotel.cuisines) == 0:
                    continue
                else:
                    common_cuisines = self.getCommonInMaps(list_one=cuisines, map_one=hotel.cuisines)
                    if len(common_cuisines) > 0:
                        hotel.cuisines = common_cuisines
                    else:
                        continue

            #

        print(len(self.filter_hotels_list))
        return self.filter_hotels_list

    def getCommonInLists(self, list_one, list_two):
        result = []
        for item in list_one:
            if item in list_two:
                result.append(item)
        return result

    def getCommonInMaps(self, list_one, map_one):
        commons = self.getCommonInLists(list_one, map_one.keys())
        result = {}
        for key, value in map_one:
            if key in commons:
                result[key] = value
        return result


# testing
if __name__ == "__main__":
    f1 = open('./data/tokyo_hotels.json', "r")
    data1 = json.loads(f1.read())

    f2 = open('./data/london_hotels.json', "r")
    data2 = json.loads(f2.read())

    hotelList = HotelList()
    hotelList.add_city_data(json_data=data1, city='Tokyo')
    hotelList.add_city_data(json_data=data2, city='London')

    hotels = hotelList.getHotels(cities=['Tokyo', 'London'], min_rating=4.5, max_hotel_price=2500,
                                 cuisines=['Italian', 'Polish'],
                                 min_nearby_places=50, min_nearby_resturants=50, min_total_reviews=50,
                                 amenities_list=[], languages=[], hotel_classes=[])
    print(len(hotels))
