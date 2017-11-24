import re


class Paginator:
    def __init__(self, collection):
        self.collection = collection

    def find(self, page_size: int, element: str, direction: int, filter_field: str, filter_value: str,
             is_filter_value_changed: bool):
        """

        :param page_size: amount items on page
        :param element: first(if direction == 1 or direction == 0) or last( if direction == -1) element on page
        :param direction: 1 - next page, 0 - this page, -1 - previous page
        :param filter_field: field in collection to sorting and filtering
        :param filter_value: value of filter_field
        :param is_filter_value_changed: new filter or not
        :return: list of documents
        """
        if direction == 0:
            direction_modificator = "$gte"
            sort_direction = 1
        elif direction == 1:
            direction_modificator = "$gt"
            sort_direction = 1
        else:
            direction_modificator = "$lt"
            sort_direction = -1

        if is_filter_value_changed:
            element = ""
            direction_modificator = "$gte"
            sort_direction = 1

        try:
            regex = re.match(r"(?P<regex>^[a-zA-Z0-9-]*)$", filter_value).groupdict()["regex"]
        except AttributeError:
            return []

        condition = {
            "$and": [{
                filter_field: {
                    "$regex": "^{}.*".format(regex)
                }
            }, {
                filter_field: {
                    direction_modificator: "{}".format(element)
                }
            }]
        }
        cursor = self.collection.find(condition).sort(filter_field, sort_direction).limit(page_size)
        return sorted(list(cursor), key=lambda k: k[filter_value])
