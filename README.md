# Omada_exporter
##### version: 0.0.3

Prometheus Exporter for [TP-Link Omada](https://www.tp-link.com/en/business-networking/omada/controller/) SDN.

It is FastAPI based application to expose basic network devices' metrics for Prometheus Server to scrape.
Omada controller is queried when `/metrics` endpoint is accessed, 
which means that if this exporter is not in use it do not generate traffic to omada controller.

Due to current limitations of Omada OpenAPI, both Web API and OpenAPI are supported.

## How to run
1. Create the `.env` file to provide necessary values specified in [Parameters](#parameters) section.
2. Start docker compose using `docker compose up -d`
3. Metrics will be available at `http://<your_hostname>:51772/metrics`


> [!IMPORTANT] 
> `.env` file filled with data from table should be saved in `./app` directory before building docker image.

### Parameters
| Name | Description |
|------|-------------|
|`BASE_URL`|The URL to Omada portal, including protocol and port. Both http and https are supported|
|`VERIFY_CERTIFICATE`|Mostly related to HTTPS if you are using untrusted certificate|
|`SITE_NAME`|Name of the site to monitor| 
|`OMADA_CLIENT_ID`|Client ID for app created in section Platform Integration, used for OpenAPI requests|
|`OMADA_CLIENT_SECRET`|Client Secret for app created in section Platform Integration, used for OpenAPI requests|
|`OMADA_USER`|User name of the account which will be used to authenticate to the WebAPI|
|`OMADA_USER_PASSWORD`|Password for the account which will be used to authenticate to the WebAPI|

### Omada Auth objects permissions
- **OpenAPI Application** (*OMADA_CLIENT*) - It can be created at the Global management level of the controller in path: 
`Setttings -> Platform Integration`. 
OpenApi app needs administrator role assigned, 
to be able to query all endpoints used within this exporter
- **User Account** (*OMADA_USER*) - it is a standard user account ,
which can be created at Global management level of the controller,
in path: `Account`. `viewer` role will provide enough access for 
this "service" user account.

## Tested on devices:
- **Switch**: [SG2218 v1.20](https://www.tp-link.com/en/business-networking/omada-switch-smart/sg2218/)
- **Router**: [ER707-M2 v1.0](https://www.tp-link.com/en/business-networking/omada-router-wired-router/er707-m2/v1/)
- **Access Point**: [EAP650(EU) v1.0](https://www.tp-link.com/en/business-networking/omada-wifi-ceiling-mount/eap650/v1/)
- **Omada controller**: [Software Controller v5.13 hosted in Docker container](https://github.com/mbentley/docker-omada-controller)