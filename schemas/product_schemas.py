from pydantic import BaseModel, Field


class PatchProduct(BaseModel):
    description: str = ''
    price: float = Field(gt=0, default=1)


class ProductCreateSchema(PatchProduct):
    title: str = Field(min_length=5, max_length=1550)
    image: str = Field(default="https://moemisto.ua/img/cache/blog_show_photo/blog/0004/75/fe2a5835d6d62a84d64cc357061c8186a244a1a8.jpeg")

class ProductDataSchema(ProductCreateSchema):
    id: str = Field(examples=['cdb56767b6b748b2b21a138c9be3af14'])


