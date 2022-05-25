def create_objects(objects_data, model):
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
