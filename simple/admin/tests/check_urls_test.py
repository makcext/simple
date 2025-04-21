ADMIN_PATHS = [
    "/admin/simple/",
]


def test_admin_urls(admin_client):
    for path in ADMIN_PATHS:
        assert admin_client.get(path).status_code == 200
