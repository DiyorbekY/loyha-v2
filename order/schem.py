from drf_yasg.inspectors import SwaggerAutoSchema

class CuponSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        return ['Cupon']

class OrderProductSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        return ['OrderProduct']