from django.http import JsonResponse

def json_test(request):
    # Your logic to retrieve data or perform operations
    data = {
        'key1': 'value1',
        'key2': 'value2',
        # Add more key-value pairs as needed
    }

    # Return a JSON response using JsonResponse
    return JsonResponse(data)
