# Integration ha_sense

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]




Integration to report power usage to [sense][ha_sense] through kasa plug emulation.  This will create a disabled entity for each entity in home assistant that reports power usage in watts, ignoring those from sense and tplink integrations. Enable any created entity to begin emulating a kasa plug for it, disable to stop emulation. Names are copied from derived entity. 

**This integration will set up the following platforms.**

Platform | Description
-- | --
`sensor` | Represents kasa emulation device, when enabled will report power usage to sense over local network.

## Installation ##
You can install this either manually copying files or using HACS. Configuration can be done on UI, you need to enter your username and password.

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Troubleshooting ##
1. You can enable logging for this integration specifically and share your logs, so I can have a deep dive investigation. To enable logging, update your `configuration.yaml` like this, we can get more information in Configuration -> Logs page
```
logger:
  default: warning
  logs:
    custom_components.ha_sense: debug
```


***

[ha_sense]: https://github.com/dahlb/ha_sense
[commits-shield]: https://img.shields.io/github/commit-activity/y/dahlb/ha_sense.svg?style=for-the-badge
[commits]: https://github.com/dahlb/ha_sense/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/dahlb/ha_sense.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Bren%20Dahl%20%40dahlb-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/dahlb/ha_sense.svg?style=for-the-badge
[releases]: https://github.com/dahlb/ha_sense/releases
