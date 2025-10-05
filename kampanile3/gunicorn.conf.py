def post_worker_init(worker):
    from django.conf import settings

    if settings.MQTT_HOST:
        from mqtt.lib import init_mqtt

        init_mqtt()

    if settings.GPIO:
        from gpio.lib import init_thread

        init_thread()
