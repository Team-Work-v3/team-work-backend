from pydantic import BaseModel, Field

class RegModel(BaseModel):
    login: str = Field(min_length=5, max_length=300)
    password: str = Field(min_length=3, max_length=300)

class EventGetModel(BaseModel):
    id: int

class EventAddModel(BaseModel):
    name_event: str = Field(min_length=5, max_length=300)
    description_event: str = Field(min_length=5, max_length=500)
    date_event: str = Field(min_length=1, max_length=300)
    time_event: str = Field(min_length=1, max_length=300)
    location_event: str = Field(min_length=1, max_length=300, default='')
    seats_event: int = Field(default=0)
    price_event: float = Field(default=0)
    event_category: str = Field(default='')
    images_events: str = Field(default='/images/logoEvents.png')
    organizers_event: str = Field(max_length=300, default='')
    program_event: str = Field(max_length=500, default='')
    fullDescription_event: str = Field(min_length=5, max_length=1000)
    created_by: int
    is_active: bool



def validate_object(object, object_type, min_l=1, max_l=5000, restricted=''):
    if object_type == int and isinstance(object, str) and object.isdigit():
        object = int(object)
    if object_type == float and isinstance(object, str) and object.isdigit():
        object = float(object)
    if min_l == 0 and (object is None or object == 0 or object == ''):
        return True
    if isinstance(object, object_type) and min_l <= len(str(object)) <= max_l:
        if True not in [i in object for i in restricted]:
            return True
    return False


def validate_greedy(to_check, dict_object, cant_be_empty=True):
    return False not in [i[0] in dict_object.keys() and validate_object(dict_object[i[0]], i[1], int(cant_be_empty))
                         for i in to_check]
