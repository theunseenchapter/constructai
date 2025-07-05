from fastapi import APIRouter

# Import endpoints with error handling
api_router = APIRouter()

# Add root endpoint first
try:
    from .endpoints import root
    api_router.include_router(root.router, tags=["Root"])
except Exception as e:
    print(f"⚠️ Root endpoint not loaded: {e}")

try:
    from .endpoints import auth
    api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
except Exception as e:
    print(f"⚠️ Auth endpoint not loaded: {e}")

try:
    from .endpoints import users
    api_router.include_router(users.router, prefix="/users", tags=["Users"])
except Exception as e:
    print(f"⚠️ Users endpoint not loaded: {e}")

try:
    from .endpoints import projects
    api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
except Exception as e:
    print(f"⚠️ Projects endpoint not loaded: {e}")

try:
    from .endpoints import files
    api_router.include_router(files.router, prefix="/files", tags=["Files"])
except Exception as e:
    print(f"⚠️ Files endpoint not loaded: {e}")

try:
    from .endpoints import boq
    api_router.include_router(boq.router, prefix="/boq", tags=["BOQ"])
except Exception as e:
    print(f"⚠️ BOQ endpoint not loaded: {e}")

try:
    from .endpoints import pricing
    api_router.include_router(pricing.router, prefix="/pricing", tags=["Pricing"])
except Exception as e:
    print(f"⚠️ Pricing endpoint not loaded: {e}")

try:
    from .endpoints import safety
    api_router.include_router(safety.router, prefix="/safety", tags=["Safety"])
except Exception as e:
    print(f"⚠️ Safety endpoint not loaded: {e}")

try:
    from .endpoints import chat
    api_router.include_router(chat.router, prefix="/chat", tags=["AI Chat"])
except Exception as e:
    print(f"⚠️ Chat endpoint not loaded: {e}")

try:
    from .endpoints import ai
    api_router.include_router(ai.router, prefix="/ai", tags=["AI"])
except Exception as e:
    print(f"⚠️ AI endpoint not loaded: {e}")
