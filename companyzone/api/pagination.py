from rest_framework.pagination import PageNumberPagination, NotFound
from rest_framework.response import Response

class StandardPagination(PageNumberPagination):
    page_size = 3 # Default size if client asks for nothing

    # Allows the client frontend (like a React app, mobile app, or Postman) 
    # to dynamically choose how many items they want to see on a single page by changing the URL
    # if you allows client to ask for specific size like:
    #     Request: GET /api/items/?page_size=25
    #     Response: Returns 25 items instead of 10
    #     Request: GET /api/items/?page=2&limit=5 (if you set page_size_query_param = 'limit')
    #     Response: Returns items 6 to 10 (Page 2, with 5 items per page)
    page_size_query_param = 'limit'

    # Use 'max_page_size' with 'page_size_query_param' 
    # When you allow clients to request any page size, 
    #   a malicious user or a bug could request ?page_size=1000000
    #   So set Absolute Limit, even if client asks 5000
    max_page_size = 100

    # No need for now:
    # If someone passes an out-of-bounds page or weird text into the ?page= parameter, 
    # paginate_queryset intercepts the crash and sends back an empty response (results: [])
    # def get_page_size(self, request):
    #     user_req_page_size = request.query_params.get(self.page_size_query_param);
    #     if user_req_page_size:
    #         try:
    #             page_size = int(user_req_page_size)
    #             if page_size <= self.max_page_size:
    #                 return page_size
    #         except(ValueError, TypeError):
    #             pass
    #     return self.page_size

    def paginate_queryset(self, queryset, request, view=None):
        try:
            return super().paginate_queryset(queryset, request, view)
        except NotFound:
            self.request = request
            self.page = None
            # Use DRF's native variable name to store the count! 
            self.count = queryset.count()
            return []

    def get_paginated_response(self, data):
        if(self.page==None):
            return Response({
                'count': self.count,
                'next': None,
                'previous': None,
                'results': data, # here data is []
            })
        return super().get_paginated_response(data)