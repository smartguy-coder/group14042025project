from fastapi import FastAPI, status, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates

from schemas.product_schemas import ProductCreateSchema, ProductDataSchema, PatchProduct
from storage import storage

app = FastAPI(
    title='Our project'
)

templates = Jinja2Templates(directory='templates')


@app.get("/", include_in_schema=False)
@app.post("/", include_in_schema=False)
def index(request: Request, q: str = Form(default='')):
    products = storage.get_products(q)
    contex = {'request': request, 'products': products}
    return templates.TemplateResponse('index.html', context=contex)


# API
@app.post("/api/products/create", status_code=status.HTTP_201_CREATED, tags=['Products'])
def product_create(product: ProductCreateSchema) -> ProductDataSchema:
    saved_product = storage.create_product(product)
    return saved_product


@app.get("/api/products", tags=['Products'])
def get_products() -> list[ProductDataSchema]:
    products = storage.get_products()
    return products


@app.get("/api/products/{product_id}", tags=['Products'])
def get_product(product_id: str) -> ProductDataSchema:
    product = storage.get_product(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Product with id {product_id} not found')
    return product


@app.delete("/api/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT, tags=['Products'])
def delete_product(product_id: str):
    storage.delete_product(product_id)


@app.patch("/api/products/{product_id}", tags=['Products'])
def patch_product(product_id: str, product_data: PatchProduct) -> ProductDataSchema:
    return storage.patch_product(product_id, product_data)
