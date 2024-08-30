# Omada Request
Automatically detects required Authentication type (*OpenAPI*, *UserBased*).

Currently supported methods:
- **get** params:
    - `path` - Omada API path, without protocol, hostname, port. i.e.: `/openapi/v1/{omadacId}/sites/{siteId}/aps/{apMac}`
    - `arguments` - (*optional*) dictionary of args to fill in provided path. i.e.: `{"apMac":<some_ap_mac_address>}`. Values `omadacId` and `siteId` are completed automatically.
    - `include_auth` - (*optional*) bool value whether auth headers should be included (works for OpenAPI only)
    - `include_params` - (*optional*) bool value whether page params should be included (works for OpenAPI only)
- **post** params:
    - `path` - Omada API path, without protocol, hostname, port. i.e.: `/openapi/v1/{omadacId}/sites/{siteId}/aps/{apMac}`
    - `arguments` - (*optional*) dictionary of args to fill in provided path. i.e.: `{"apMac":<some_ap_mac_address>}`. Values `omadacId` and `siteId` are completed automatically.
    - `body` - (*optional*) dictionary with request body contents.
