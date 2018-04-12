from django.conf import settings


import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


from rest_framework import status
class TestMiddleWare():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        print("called")

        # Code to be executed for each request/response after
        # the view is called.

        if status.is_success(response.status_code):
            print("han g    " +str(response.status_code))
            return response

        else:
            print("no g          "+str(response.status_code))
            logger.info('Something went wrong!')

            return response




    # def process_view(self, request, view_func, view_args, view_kwargs):
    #     assert hasattr(request, 'user')
    #     print("kaaam ")
    #     response = self.get_response(request)
