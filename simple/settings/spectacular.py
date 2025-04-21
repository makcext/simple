# Настройки DRF Spectacular
SPECTACULAR_SETTINGS = {
    "TITLE": "simple",
    # "DESCRIPTION": "simpleAPI",
    "PUBLIC": True,
    "TOS": None,
    "VERSION": "v1.0.1",
    "COMPONENT_SPLIT_REQUEST": True,
    "SERVE_INCLUDE_SCHEMA": False,
    "GENERIC_ADDITIONAL_PROPERTIES": None,
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "displayOperationId": True,
        "filter": True,
        "showExtensions": True,
        "showCommonExtensions": True,
        "requestSnippetsEnabled": True,
        "tryItOutEnabled": True,
    },
    "SCHEMA_PATH_PREFIX": "/api/v1/",
}
