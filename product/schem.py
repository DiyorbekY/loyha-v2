from drf_yasg.inspectors import SwaggerAutoSchema


class CategorySchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        return ['Category']

class BrandSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        return ['Brands']


class ReviewSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        return ['Review']

class WishListSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        return ['WishList']

class FlashSaleSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        return ['FlashSale']

class ProductViewHistorySchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        return ['ProductViewHistory']
