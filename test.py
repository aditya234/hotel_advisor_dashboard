if (hotel.city in cities) and ((hotel.rating is None) and (hotel.rating >= min_rating)) and (
        hotel.best_price is not None) and (
        hotel.best_price <= max_hotel_price) and (hotel.restaurants_nearby is not None) and (
        hotel.restaurants_nearby >= min_nearby_resturants) and (hotel.attractions_nearby is not None) and (
        hotel.attractions_nearby >= min_nearby_places) and (hotel.review_count is not None) and (
        hotel.review_count >= min_total_reviews):
    hotel.cuisines = self.getCommonInMaps(list_one=cuisines,
                                          map_one=hotel.cuisines)
    # if hotel.cuisines is not None and len(hotel.cuisines) > 0:
    #     continue

    hotel.amenities = self.getCommoninLists(list_one=amenities_list, list_two=hotel.amenities)
    # if hotel.amenities is not None and len(hotel.amenities) > 0:
    #     continue

    hotel.languages = self.getCommoninLists(list_one=languages,
                                            list_two=hotel.languages)
    # if hotel.languages is not None and len(hotel.languages) > 0:
    #     continue

    hotel.hotel_classes = self.getCommoninLists(list_one=hotel_classes, list_two=hotel.hotel_classes)
    # if hotel.hotel_classes is not None and len(hotel.hotel_classes) > 0:
    #     continue
    self.filter_hotels_list.append(hotel)