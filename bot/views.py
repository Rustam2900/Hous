from django.shortcuts import render, get_object_or_404
from .models import House, HouseMeasure, HouseImage

def house_details(request, id):
    house = get_object_or_404(House, id=id)
    house_measure = get_object_or_404(HouseMeasure, house=house)
    house_images = HouseImage.objects.filter(house=house)  # Tasvirlarni olish

    house_details = {
        'title': house.title,
        'description': house.description,
        'zipcode': house.zipcode,
        'room': house.room,
        'price': house.price,
        'living_room_area': house_measure.living_room_area,
        'bedroom_area': house_measure.bedroom_area,
        'bathroom_count': house_measure.bathroom_count,
        'kitchen_area': house_measure.kitchen_area,
        'year_built': house_measure.year_built,
        'total_area': house_measure.total_area,
        'images': house_images  # Tasvirlar qo'shildi
    }

    return render(request, 'house_details.html', {'house_details': house_details})
