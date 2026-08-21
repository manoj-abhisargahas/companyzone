from rest_framework.pagination import PageNumberPagination

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

    def get_page_size(self, request):
        user_req_page_size = request.query_params.get(self.page_size_query_param);
        if user_req_page_size:
            try:
                page_size = int(user_req_page_size)
                if page_size <= self.max_page_size:
                    return page_size
            except(ValueError, TypeError):
                pass
        return self.page_size