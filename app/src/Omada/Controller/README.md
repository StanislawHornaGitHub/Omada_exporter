# Omada Controller
Contains methods to fetch data from Omada SDN system.

## AccessPoint
- `.get_info()` - returns list of [AccessPoint](/app/src/Omada/Model/Devices/AccessPoint.py) for all Access Points in the site.
- `.get_port_info()` - returns list of [AccessPointPort](/app/src/Omada/Model/Ports/AccessPointPort.py) for all Access Points in the site.
- `.get_radio_info()` - returns list of [AccessPointRadio](/app/src/Omada/Model/Ports/AccessPointRadio.py) for all Access Points in the site.
- `.get_radio_stats()` - returns list of [AccessPointRadioStats](/app/src/Omada/Model/Ports/AccessPointRadioStats.py) for all Access Points in the site.

## Devices
- `.get_list()` - returns list of [Device](/app/src/Omada/Model/Devices/Device.py), which represents all adopted devices within the site

## HealthCheck
- `.get()` - tests if Omada controller is available and if exporter is able to authenticate to openAPI and webAPI.

## Router
- `.get_info()` - returns list of [Router](/app/src/Omada/Model/Devices/Router.py) for all Routers in the site.
- `.get_port_info()` - returns list of [RouterPort](/app/src/Omada/Model/Ports/RouterPort.py) and list of [RouterPortStats](/app/src/Omada/Model/Ports/RouterPortStats.py) for all Routers in the site.

## Switch
- `.get_info()` - returns list of [Switch](/app/src/Omada/Model/Devices/Switch.py) for all Switches in the site.
- `.get_port_info()` - returns list of [SwitchPort](/app/src/Omada/Model/Ports/SwitchPort.py) and list of [SwitchPortStats](/app/src/Omada/Model/Ports/SwitchPortStats.py) for all Switches in the site.