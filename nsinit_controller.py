# TODO: change to read from volume mount later on
# https://kubernetes.io/docs/concepts/configuration/configmap/

import kopf
import logging


@kopf.on.startup()
def configure(settings: kopf.OperatorSettings, **_):
    settings.peering.standalone = True


@kopf.on.update('namespaces')
def update_fn(body, **kwargs):
    logging.info(f"Update handler is called with body: {body}")


@kopf.on.create('namespaces')
def create_fn(body, **kwargs):
    logging.info(f"Create handler is called with body: {body}")

