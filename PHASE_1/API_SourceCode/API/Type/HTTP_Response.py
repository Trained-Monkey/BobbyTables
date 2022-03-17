from pydantic import BaseModel

class HTTP_Error(BaseModel):
    error_message: str

class HTTP_400(HTTP_Error):
    class Config:
        schema_extra = {
            'example': {
                'error_message': 'Bad request'
            }
        }

class HTTP_404(HTTP_Error):
    class Config:
        schema_extra = {
            'example': {
                'error_message': 'No article found with that given id'
            }
        }

class HTTP_500(HTTP_Error):
    class Config:
        schema_extra = {
            'example': {
                'error_message': 'Internal server error'
            }
        }
