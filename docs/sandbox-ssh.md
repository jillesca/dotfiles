# sandbox-ssh

Generates a fresh local SSH key pair and installs it on a DevNet sandbox VM,
so you can connect without re-typing the VM password on every use. Safe to
re-run against a new sandbox reservation — the key is overwritten each time,
so you don't accumulate stale keys for VMs that no longer exist.

Source: [`sandbox-ssh`](../sandbox-ssh)

## Install

```sh
make install-sandbox-ssh
```

Symlinks the script into `~/.local/bin` (make sure it's on your `PATH`).

## Usage

```sh
sandbox-ssh --ip 10.10.20.15
sandbox-ssh --ip 10.10.20.15 --user admin
sandbox-ssh --ip 10.10.20.15 --key ~/.ssh/other_key
sandbox-ssh --help
```

## Options

| Flag     | Env var        | Default              | Required |
| -------- | -------------- | -------------------- | -------- |
| `--ip`   | `SANDBOX_IP`   | —                    | yes      |
| `--user` | `SANDBOX_USER` | `developer`          | no       |
| `--key`  | `SSH_KEY_PATH` | `~/.ssh/sandbox_key` | no       |

Flags take precedence over the matching environment variable. You'll be
prompted for the sandbox VM's password once, to authorize the new key.

## Origin

This is a standalone fork of the SSH setup script used in the
[XRd-Sandbox](https://github.com/CiscoDevNet/XRd-Sandbox) repo
(`scripts/setup/configure-ssh.sh`), generalized to work against any DevNet
sandbox VM. The two are intentionally not kept in sync — `XRd-Sandbox`'s
copy stays project-specific for teaching purposes.
