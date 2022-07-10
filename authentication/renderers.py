from email import charset
import json
from lib2to3.pgen2 import token
from rest_framework.renderers import JSONRenderer

class UserJSONRenderer(JSONRenderer):
    charset='utf-8'

    def renderer(self,data,media_type=None,renderer_context=None):
        token=data.get('token',None)

        if token is not None and isinstance(token,bytes):
            data['token']=token.decode('utf-8')
        return json.dumps({
            'user':data
        })