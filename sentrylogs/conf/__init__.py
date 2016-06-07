from raven import Client
import settings

# configure Raven client
client = Client(dsn=settings.SENTRY_DSN)
