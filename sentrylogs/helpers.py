from conf import client


def send_message(message, extended_message, params, site, logger):
    client.capture(
        'Message',
        message=message,
        data={
            'sentry.interfaces.Message': {
                'message': extended_message,
                'params': tuple(params),
            },
            'site': site,
            'logger': logger,
        },
    )
