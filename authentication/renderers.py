import json
from rest_framework.renderers import JSONRenderer

class UserRenderer(JSONRenderer):
    charset='utf-8'

    # def renderer(self,data,media_type=None,renderer_context=None):
    #     token=data.get('token',None)

    #     if token is not None and isinstance(token,bytes):
    #         data['token']=token.decode('utf-8')
    #     return json.dumps({
    #         'user':data
    #     })

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response=''
        if 'ErrorDetail' in str(data):
            response=json.dumps({'errors':data})
        else:
            response=json.dumps(data)
        return response