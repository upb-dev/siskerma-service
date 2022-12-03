from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = {'success': True, 'message': 'success', 'data': None, 'errors': []}
        if data and 'success' in data and not data['success']:
            response_data = data
        elif data and 'detail' in data and len(data) == 1:
            response_data['message'] = data.get('detail')
        else:
            response_data['data'] = data if data or isinstance(data, list) else None

        # call super to render the response
        response = super(CustomJSONRenderer, self).render(response_data, accepted_media_type, renderer_context)

        return response
