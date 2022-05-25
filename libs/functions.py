'''The function takes dictionary objects_data and model Class as ttributes
and returns a list of objects of the given class. Can be used to create or update
many-to-many related fields objects in a nested serializer.'''
def create_or_update_objects(objects_data, model):
    existing_data = []
    new_data = []

    for object in objects_data:
        if object.get("id"):
            existing_data.append(object.get("id"))
        else:
            new_obj = model(**object)
            new_data.append(new_obj)
    objects = model.objects.bulk_create(new_data)
    for obj in objects:
        existing_data.append(obj.id)

    return existing_data



# def update_objects(objects, model, instance, attr):
#     objects_list = []
#     for object in objects:
#         if 'id' in object:
#             objects_list.append(object['id'])

#     all_objects = model.objects.all(filter)
#     for object in all_objects:
#         if object.id not in objects_list:
#             object.delete()
    
#     for object in objects:
#         if 'id' in object:
#             obj = model.get(id=object['id'])
#             super().update(obj, object)
#         else:
#             model.objects.create(attr=instance, **object)
