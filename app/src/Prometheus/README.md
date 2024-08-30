# Prometheus
Definition of Prometheus metrics exposed on default `/metrics` endpoint.

# Supported metrics
|Device|Metric|Description|
|-|-|-|
|AccessPoint|cpu_usage|CPU usage in %|
|AccessPoint|device|Device information|
|AccessPoint|memory_usage|Memory usage in %|
|AccessPoint|access_point_port|Access point port info|
|AccessPoint|access_point_port_rx|Sum of received bytes|
|AccessPoint|access_point_port_tx|Sum of transmitted bytes|
|AccessPoint|radio|Access point radio details|
|AccessPoint|radio_rx|Sum of received bytes|
|AccessPoint|radio_rx_pkts|Sum of received packets|
|AccessPoint|radio_rx_pkts_dropped|Sum of dropped rx packets|
|AccessPoint|radio_rx_pkts_error|Sum of error rx packets|
|AccessPoint|radio_rx_pkts_retry|Sum of retry rx packets|
|AccessPoint|radio_rx_rate|Received bits per second|
|AccessPoint|radio_rx_retry_pkts_rate|Received packets retry|
|AccessPoint|radio_rx_util|Percentage of receive channel bandwidth usage|
|AccessPoint|radio_tx|Sum of transmitted bytes|
|AccessPoint|radio_tx_pkts|Sum of transmitted packets|
|AccessPoint|radio_tx_pkts_dropped|Sum of dropped tx packets|
|AccessPoint|radio_tx_pkts_error|Sum of error tx packets|
|AccessPoint|radio_tx_pkts_retry|Sum of retry tx packets|
|AccessPoint|radio_tx_rate|Transmitted bits per second|
|AccessPoint|radio_tx_retry_pkts_rate|Transmitted packets retry|
|AccessPoint|radio_tx_util|Percentage of transmit channel bandwidth usage|
|Router|cpu_usage|CPU usage in %|
|Router|device|Device information|
|Router|memory_usage|Memory usage in %|
|Router|router_port_drop_pkts|Dropped packets|
|Router|router_port_err_pkts|Errored packets|
|Router|router_port|Router port information details|
|Router|router_port_ipv4_config|Router port ipv4 config|
|Router|router_port_ipv6_config|Router port ipv6 config|
|Router|router_port_latency|Latency in ms on particular port|
|Router|router_port_loss|Percentage of packet loss on particular port|
|Router|router_port_rx|Sum of received bytes|
|Router|router_port_rx_pkts|Received packets|
|Router|router_port_rx_rate|Received bytes per second|
|Router|router_port_tx|Sum of transmitted bytes|
|Router|router_port_tx_pkts|Transmitted packets|
|Router|router_port_tx_rate|Transmitted bytes per second|
|Router|router_temperature|Router temperature in Celsius|
|Switch|cpu_usage|CPU usage in %|
|Switch|device|Device information|
|Switch|memory_usage|Memory usage in %|
|Switch|switch_drop_pkts|Dropped packets|
|Switch|switch_port|Switch port information details|
|Switch|switch_port_rx|Sum of received bytes|
|Switch|switch_port_rx_err_pkts|Received packets errors|
|Switch|switch_port_rx_pkts|Received packets|
|Switch|switch_port_rx_rate|Received bytes per second|
|Switch|switch_port_tx|Sum of transmitted bytes|
|Switch|switch_port_tx_err_pkts|Transmitted packets errors|
|Switch|switch_port_tx_pkts|Transmitted packets|
|Switch|switch_port_tx_rate|Transmitted bytes per second|
