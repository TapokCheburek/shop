import os
import jwt
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
import httpx

app = FastAPI(title="API Gateway")

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8002")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:8000")
ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://order-service:8001")
JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-key")

# We use httpx.AsyncClient to forward requests
client = httpx.AsyncClient()

async def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Unauthorized: Missing Authorization header")
    try:
        scheme, token = auth_header.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid token scheme")
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway(request: Request, path: str):
    user_id = None
    # Endpoints that require authentication:
    # All /orders endpoints (or maybe just my_orders).
    # All /products POST/PUT/DELETE. We can keep GET /products public.
    
    if path.startswith("orders") or (path.startswith("products") and request.method != "GET"):
        user_id = await verify_token(request)
        
    try:
        body = await request.body()
    except:
        body = None
            
    target_url = None
    if path.startswith("auth"):
        target_url = f"{AUTH_SERVICE_URL}/{path}"
    elif path.startswith("products"):
        target_url = f"{PRODUCT_SERVICE_URL}/{path}"
    elif path.startswith("orders"):
        target_url = f"{ORDER_SERVICE_URL}/{path}"
    else:
        return JSONResponse(status_code=404, content={"message": "Not Found"})

    headers = dict(request.headers)
    headers.pop("host", None)
    if user_id:
        headers["x-user-id"] = user_id

    try:
        # Forward request
        response = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            params=request.query_params,
            content=body
        )
        import json
        content = None
        try:
            content = response.json()
        except:
            content = response.text

        return JSONResponse(status_code=response.status_code, content=content)
    except httpx.RequestError as e:
        return JSONResponse(status_code=500, content={"message": "Gateway error inside microservice call"})
