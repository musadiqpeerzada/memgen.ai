# Minimal Vercel entrypoint that re-exports the FastAPI ASGI app
# Vercel's Python runtime will import this file; exporting an `app` variable
# that is an ASGI application lets Vercel use it directly.

try:
    from app.main import app  # import the FastAPI instance
except Exception as _import_error:
    # If importing fails during deployment, raise on invocation so the logs show the real error
    import traceback
    _trace = traceback.format_exc()

    def handler(request, context=None):
        raise RuntimeError("Failed to import app.main during startup:\n" + _trace)

    # Also provide a placeholder `app` that raises on use (in case Vercel expects it)
    class _DummyApp:
        async def __call__(self, scope, receive, send):
            raise RuntimeError("Failed to import app.main during startup:\n" + _trace)

    app = _DummyApp()
