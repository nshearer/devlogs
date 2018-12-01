import os
import sys
import shutil
from threading import Thread
from tempfile import TemporaryDirectory
from textwrap import dedent
from random import randint
from time import sleep

from devlogs import main

LONG_CONTENT = dedent("""\
    Nov 29 06:09:07 ubuntu-bionic systemd-modules-load[395]: Inserted module 'iscsi_tcp'
    Nov 29 06:09:07 ubuntu-bionic systemd-modules-load[395]: Inserted module 'ib_iser'
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Load Kernel Modules.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting Apply Kernel Variables...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Mounting FUSE Control File System...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Mounting Kernel Configuration File System...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Create Static Device Nodes in /dev.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started udev Coldplug all Devices.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Apply Kernel Variables.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Mounted POSIX Message Queue File System.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Remount Root and Kernel File Systems.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Mounted Huge Pages File System.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Mounted Kernel Debug File System.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Mounted FUSE Control File System.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Mounted Kernel Configuration File System.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started LVM2 metadata daemon.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting Load/Save Random Seed...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting Initial cloud-init job (pre-networking)...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting Flush Journal to Persistent Storage...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting udev Kernel Device Manager...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Set the console keyboard layout.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Monitoring of LVM2 mirrors, snapshots etc. using dmeventd or progress polling.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Load/Save Random Seed.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Reached target Local File Systems (Pre).
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Reached target Local File Systems.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting Set console font and keymap...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting Tell Plymouth To Write Out Runtime Data...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting Commit a transient machine-id on disk...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting ebtables ruleset management...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting AppArmor initialization...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started udev Kernel Device Manager.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Set console font and keymap.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Tell Plymouth To Write Out Runtime Data.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Dispatch Password Requests to Console Directory Watch.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Reached target Local Encrypted Volumes.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Flush Journal to Persistent Storage.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting Create Volatile Files and Directories...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Commit a transient machine-id on disk.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Create Volatile Files and Directories.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting Update UTMP about System Boot/Shutdown...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Update UTMP about System Boot/Shutdown.
    Nov 29 06:09:07 ubuntu-bionic apparmor[443]:  * Starting AppArmor profiles
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started ebtables ruleset management.
    Nov 29 06:09:07 ubuntu-bionic systemd-udevd[457]: link_config: autonegotiation is unset or enabled, the speed and duplex are not writable.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Found device /dev/ttyS0.
    Nov 29 06:09:07 ubuntu-bionic systemd-udevd[455]: link_config: autonegotiation is unset or enabled, the speed and duplex are not writable.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Listening on Load/Save RF Kill Switch Status /dev/rfkill Watch.
    Nov 29 06:09:07 ubuntu-bionic apparmor[443]: Skipping profile in /etc/apparmor.d/disable: usr.sbin.rsyslogd
    Nov 29 06:09:07 ubuntu-bionic apparmor[443]:    ...done.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started AppArmor initialization.
    Nov 29 06:09:07 ubuntu-bionic cloud-init[421]: Cloud-init v. 18.4-0ubuntu1~18.04.1 running 'init-local' at Thu, 29 Nov 2018 06:09:03 +0000. Up 10.72 seconds.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Initial cloud-init job (pre-networking).
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Reached target Network (Pre).
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting Network Service...
    Nov 29 06:09:07 ubuntu-bionic systemd-networkd[602]: Enumeration completed
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Network Service.
    Nov 29 06:09:07 ubuntu-bionic systemd-networkd[602]: lo: Link is not managed by us
    Nov 29 06:09:07 ubuntu-bionic systemd-networkd[602]: enp0s3: IPv6 successfully enabled
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting Wait for Network to be Configured...
    Nov 29 06:09:07 ubuntu-bionic systemd-networkd[602]: enp0s3: Gained carrier
    Nov 29 06:09:07 ubuntu-bionic systemd-networkd[602]: enp0s3: DHCPv4 address 10.0.2.15/24 via 10.0.2.2
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting Network Name Resolution...
    Nov 29 06:09:07 ubuntu-bionic systemd-resolved[639]: Positive Trust Anchors:
    Nov 29 06:09:07 ubuntu-bionic systemd-resolved[639]: . IN DS 19036 8 2 49aac11d7b6f6446702e54a1607371607a1a41855200fd2ce1cdde32f24e8fb5
    Nov 29 06:09:07 ubuntu-bionic systemd-resolved[639]: . IN DS 20326 8 2 e06d44b80b8f1d39a95c0b0d7c65d08458e880409bbc683457104237c7f8ec8d
    Nov 29 06:09:07 ubuntu-bionic systemd-resolved[639]: Negative trust anchors: 10.in-addr.arpa 16.172.in-addr.arpa 17.172.in-addr.arpa 18.172.in-addr.arpa 19.172.in-addr.arpa 20.172.in-addr.arpa 21.172.in-addr.arpa 22.172.in-addr.arpa 23.172.in-addr.arpa 24.172.in-addr.arpa 25.172.in-addr.arpa 26.172.in-addr.arpa 27.172.in-addr.arpa 28.172.in-addr.arpa 29.172.in-addr.arpa 30.172.in-addr.arpa 31.172.in-addr.arpa 168.192.in-addr.arpa d.f.ip6.arpa corp home internal intranet lan local private test
    Nov 29 06:09:07 ubuntu-bionic systemd-resolved[639]: Using system hostname 'ubuntu-bionic'.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Network Name Resolution.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Reached target Host and Network Name Lookups.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Reached target Network.
    Nov 29 06:09:07 ubuntu-bionic systemd-networkd[602]: enp0s3: Gained IPv6LL
    Nov 29 06:09:07 ubuntu-bionic systemd-networkd[602]: enp0s3: Configured
    Nov 29 06:09:07 ubuntu-bionic systemd-networkd-wait-online[632]: managing: enp0s3
    Nov 29 06:09:07 ubuntu-bionic systemd-networkd-wait-online[632]: ignoring: lo
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Wait for Network to be Configured.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting Initial cloud-init job (metadata service crawler)...
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: Cloud-init v. 18.4-0ubuntu1~18.04.1 running 'init' at Thu, 29 Nov 2018 06:09:05 +0000. Up 13.37 seconds.
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: ci-info: ++++++++++++++++++++++++++++++++++++++Net device info++++++++++++++++++++++++++++++++++++++
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: ci-info: +--------+------+----------------------------+---------------+--------+-------------------+
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: ci-info: | Device |  Up  |          Address           |      Mask     | Scope  |     Hw-Address    |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: ci-info: +--------+------+----------------------------+---------------+--------+-------------------+
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: ci-info: | enp0s3 | True |         10.0.2.15          | 255.255.255.0 | global | 02:67:f0:a3:a8:75 |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: ci-info: | enp0s3 | True | fe80::67:f0ff:fea3:a875/64 |       .       |  link  | 02:67:f0:a3:a8:75 |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: ci-info: |   lo   | True |         127.0.0.1          |   255.0.0.0   |  host  |         .         |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: ci-info: |   lo   | True |          ::1/128           |       .       |  host  |         .         |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: ci-info: +--------+------+----------------------------+---------------+--------+-------------------+
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: ci-info: ++++++++++++++++++++++++++++Route IPv4 info+++++++++++++++++++++++++++++
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: ci-info: +-------+-------------+----------+-----------------+-----------+-------+
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: ci-info: | Route | Destination | Gateway  |     Genmask     | Interface | Flags |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: ci-info: +-------+-------------+----------+-----------------+-----------+-------+
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: ci-info: |   0   |   0.0.0.0   | 10.0.2.2 |     0.0.0.0     |   enp0s3  |   UG  |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: ci-info: |   1   |   10.0.2.0  | 0.0.0.0  |  255.255.255.0  |   enp0s3  |   U   |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: ci-info: |   2   |   10.0.2.2  | 0.0.0.0  | 255.255.255.255 |   enp0s3  |   UH  |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: ci-info: +-------+-------------+----------+-----------------+-----------+-------+
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: ci-info: +++++++++++++++++++Route IPv6 info+++++++++++++++++++
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: ci-info: +-------+-------------+---------+-----------+-------+
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: ci-info: | Route | Destination | Gateway | Interface | Flags |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: ci-info: +-------+-------------+---------+-----------+-------+
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: ci-info: |   1   |  fe80::/64  |    ::   |   enp0s3  |   U   |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: ci-info: |   3   |    local    |    ::   |   enp0s3  |   U   |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: ci-info: |   4   |   ff00::/8  |    ::   |   enp0s3  |   U   |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: ci-info: +-------+-------------+---------+-----------+-------+
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: Generating public/private rsa key pair.
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: Your identification has been saved in /etc/ssh/ssh_host_rsa_key.
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: Your public key has been saved in /etc/ssh/ssh_host_rsa_key.pub.
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: The key fingerprint is:
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: SHA256:mhAYpzYqwD56A4dSW12SoDClJlRIV2LAFqdci7Im+FI root@ubuntu-bionic
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: The key's randomart image is:
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: +---[RSA 2048]----+
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |=*BB+o...        |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |+BB*o..o         |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |**B.o .          |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |B* + .           |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |X+E .   S        |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |*=.  . o         |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |o +   o          |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: | o .             |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |                 |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: +----[SHA256]-----+
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: Generating public/private dsa key pair.
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: Your identification has been saved in /etc/ssh/ssh_host_dsa_key.
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: Your public key has been saved in /etc/ssh/ssh_host_dsa_key.pub.
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: The key fingerprint is:
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: SHA256:gooHNyf3s2ICFX0v6oEbT8PvLjzA/76BaMDGxpr3HkQ root@ubuntu-bionic
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: The key's randomart image is:
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: +---[DSA 1024]----+
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |   .             |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |  . . .          |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |   .E. .         |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |+ .. .. .        |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |oO+o=...S        |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |=*=O*o .         |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |+.*Xo++          |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: | +o.X..+         |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |   +oOB.         |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: +----[SHA256]-----+
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: Generating public/private ecdsa key pair.
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: Your identification has been saved in /etc/ssh/ssh_host_ecdsa_key.
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: Your public key has been saved in /etc/ssh/ssh_host_ecdsa_key.pub.
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: The key fingerprint is:
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: SHA256:NKhdA817D0+vBWOpXS7R8zEgn1qslxwxMWKtjcZD1eQ root@ubuntu-bionic
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: The key's randomart image is:
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] Linux version 4.15.0-39-generic (buildd@lgw01-amd64-054) (gcc version 7.3.0 (Ubuntu 7.3.0-16ubuntu3)) #42-Ubuntu SMP Tue Oct 23 15:48:01 UTC 2018 (Ubuntu 4.15.0-39.42-generic 4.15.18)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] Command line: BOOT_IMAGE=/boot/vmlinuz-4.15.0-39-generic root=LABEL=cloudimg-rootfs ro console=tty1 console=ttyS0
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] KERNEL supported cpus:
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000]   Intel GenuineIntel
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000]   AMD AuthenticAMD
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000]   Centaur CentaurHauls
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] x86/fpu: Supporting XSAVE feature 0x001: 'x87 floating point registers'
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] x86/fpu: Supporting XSAVE feature 0x002: 'SSE registers'
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] x86/fpu: Supporting XSAVE feature 0x004: 'AVX registers'
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] x86/fpu: xstate_offset[2]:  576, xstate_sizes[2]:  256
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] x86/fpu: Enabled xstate features 0x7, context size is 832 bytes, using 'standard' format.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] e820: BIOS-provided physical RAM map:
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] BIOS-e820: [mem 0x0000000000000000-0x000000000009fbff] usable
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] BIOS-e820: [mem 0x000000000009fc00-0x000000000009ffff] reserved
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] BIOS-e820: [mem 0x00000000000f0000-0x00000000000fffff] reserved
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] BIOS-e820: [mem 0x0000000000100000-0x000000007ffeffff] usable
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] BIOS-e820: [mem 0x000000007fff0000-0x000000007fffffff] ACPI data
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] BIOS-e820: [mem 0x00000000fec00000-0x00000000fec00fff] reserved
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] BIOS-e820: [mem 0x00000000fee00000-0x00000000fee00fff] reserved
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] BIOS-e820: [mem 0x00000000fffc0000-0x00000000ffffffff] reserved
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] NX (Execute Disable) protection: active
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] SMBIOS 2.5 present.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] DMI: innotek GmbH VirtualBox/VirtualBox, BIOS VirtualBox 12/01/2006
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] Hypervisor detected: KVM
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] e820: update [mem 0x00000000-0x00000fff] usable ==> reserved
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] e820: remove [mem 0x000a0000-0x000fffff] usable
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] e820: last_pfn = 0x7fff0 max_arch_pfn = 0x400000000
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] MTRR default type: uncachable
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] MTRR variable ranges disabled:
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] MTRR: Disabled
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] x86/PAT: MTRRs disabled, skipping PAT initialization too.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] CPU MTRRs all blank - virtualized system.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] x86/PAT: Configuration [0-7]: WB  WT  UC- UC  WB  WT  UC- UC  
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] found SMP MP-table at [mem 0x0009fff0-0x0009ffff] mapped at [        (ptrval)]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] Scanning 1 areas for low memory corruption
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] Base memory trampoline at [        (ptrval)] 99000 size 24576
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] BRK [0x3893f000, 0x3893ffff] PGTABLE
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] BRK [0x38940000, 0x38940fff] PGTABLE
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] BRK [0x38941000, 0x38941fff] PGTABLE
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] BRK [0x38942000, 0x38942fff] PGTABLE
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] BRK [0x38943000, 0x38943fff] PGTABLE
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] BRK [0x38944000, 0x38944fff] PGTABLE
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] RAMDISK: [mem 0x35ae3000-0x36d68fff]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] ACPI: Early table checksum verification disabled
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] ACPI: RSDP 0x00000000000E0000 000024 (v02 VBOX  )
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] ACPI: XSDT 0x000000007FFF0030 00003C (v01 VBOX   VBOXXSDT 00000001 ASL  00000061)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] ACPI: FACP 0x000000007FFF00F0 0000F4 (v04 VBOX   VBOXFACP 00000001 ASL  00000061)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] ACPI: DSDT 0x000000007FFF0470 0021FF (v02 VBOX   VBOXBIOS 00000002 INTL 20100528)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] ACPI: FACS 0x000000007FFF0200 000040
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] ACPI: FACS 0x000000007FFF0200 000040
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] ACPI: APIC 0x000000007FFF0240 00005C (v02 VBOX   VBOXAPIC 00000001 ASL  00000061)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] ACPI: SSDT 0x000000007FFF02A0 0001CC (v01 VBOX   VBOXCPUT 00000002 INTL 20100528)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] ACPI: Local APIC address 0xfee00000
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] No NUMA configuration found
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] Faking a node at [mem 0x0000000000000000-0x000000007ffeffff]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] NODE_DATA(0) allocated [mem 0x7ffc5000-0x7ffeffff]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] kvm-clock: cpu 0, msr 0:7ff44001, primary cpu clock
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] kvm-clock: Using msrs 4b564d01 and 4b564d00
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] kvm-clock: using sched offset of 6275781556 cycles
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] clocksource: kvm-clock: mask: 0xffffffffffffffff max_cycles: 0x1cd42e4dffb, max_idle_ns: 881590591483 ns
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] Zone ranges:
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000]   DMA      [mem 0x0000000000001000-0x0000000000ffffff]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000]   DMA32    [mem 0x0000000001000000-0x000000007ffeffff]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000]   Normal   empty
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000]   Device   empty
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] Movable zone start for each node
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] Early memory node ranges
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000]   node   0: [mem 0x0000000000001000-0x000000000009efff]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000]   node   0: [mem 0x0000000000100000-0x000000007ffeffff]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] Initmem setup node 0 [mem 0x0000000000001000-0x000000007ffeffff]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] On node 0 totalpages: 524174
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000]   DMA zone: 64 pages used for memmap
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000]   DMA zone: 21 pages reserved
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000]   DMA zone: 3998 pages, LIFO batch:0
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000]   DMA32 zone: 8128 pages used for memmap
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000]   DMA32 zone: 520176 pages, LIFO batch:31
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] Reserved but unavailable: 98 pages
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] ACPI: PM-Timer IO Port: 0x4008
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] ACPI: Local APIC address 0xfee00000
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] IOAPIC[0]: apic_id 2, version 32, address 0xfec00000, GSI 0-23
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] ACPI: INT_SRC_OVR (bus 0 bus_irq 0 global_irq 2 dfl dfl)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] ACPI: INT_SRC_OVR (bus 0 bus_irq 9 global_irq 9 low level)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] ACPI: IRQ0 used by override.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] ACPI: IRQ9 used by override.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] Using ACPI (MADT) for SMP configuration information
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] smpboot: Allowing 2 CPUs, 0 hotplug CPUs
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] PM: Registered nosave memory: [mem 0x00000000-0x00000fff]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] PM: Registered nosave memory: [mem 0x0009f000-0x0009ffff]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] PM: Registered nosave memory: [mem 0x000a0000-0x000effff]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] PM: Registered nosave memory: [mem 0x000f0000-0x000fffff]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] e820: [mem 0x80000000-0xfebfffff] available for PCI devices
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] Booting paravirtualized kernel on KVM
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] clocksource: refined-jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 7645519600211568 ns
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] random: get_random_bytes called from start_kernel+0x99/0x4fd with crng_init=0
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] setup_percpu: NR_CPUS:8192 nr_cpumask_bits:2 nr_cpu_ids:2 nr_node_ids:1
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] percpu: Embedded 46 pages/cpu @        (ptrval) s151552 r8192 d28672 u1048576
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] pcpu-alloc: s151552 r8192 d28672 u1048576 alloc=1*2097152
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] pcpu-alloc: [0] 0 1 
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] PV qspinlock hash table entries: 256 (order: 0, 4096 bytes)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] Built 1 zonelists, mobility grouping on.  Total pages: 515961
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] Policy zone: DMA32
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] Kernel command line: BOOT_IMAGE=/boot/vmlinuz-4.15.0-39-generic root=LABEL=cloudimg-rootfs ro console=tty1 console=ttyS0
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] Calgary: detecting Calgary via BIOS EBDA area
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] Calgary: Unable to locate Rio Grande table in EBDA - bailing!
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] Memory: 2015808K/2096696K available (12300K kernel code, 2472K rwdata, 4248K rodata, 2408K init, 2416K bss, 80888K reserved, 0K cma-reserved)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] SLUB: HWalign=64, Order=0-3, MinObjects=0, CPUs=2, Nodes=1
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] Kernel/User page tables isolation: enabled
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] ftrace: allocating 39178 entries in 154 pages
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.004000] Hierarchical RCU implementation.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.004000] 	RCU restricting CPUs from NR_CPUS=8192 to nr_cpu_ids=2.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.004000] 	Tasks RCU enabled.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.004000] RCU: Adjusting geometry for rcu_fanout_leaf=16, nr_cpu_ids=2
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.004000] NR_IRQS: 524544, nr_irqs: 440, preallocated irqs: 16
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.004000] Console: colour VGA+ 80x25
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.004000] console [tty1] enabled
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.004000] console [ttyS0] enabled
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.004000] ACPI: Core revision 20170831
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.004000] ACPI: 2 ACPI AML tables successfully acquired and loaded
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.004000] APIC: Switch to symmetric I/O mode setup
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.004284] x2apic enabled
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.008005] Switched APIC routing to physical x2apic.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.009973] ..TIMER: vector=0x30 apic1=0 pin1=2 apic2=-1 pin2=-1
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.012006] tsc: Detected 3310.820 MHz processor
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.016015] Calibrating delay loop (skipped) preset value.. 6621.64 BogoMIPS (lpj=13243280)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.017991] pid_max: default: 32768 minimum: 301
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.018835] Security Framework initialized
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.020006] Yama: becoming mindful.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.020631] AppArmor: AppArmor initialized
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.022514] Dentry cache hash table entries: 262144 (order: 9, 2097152 bytes)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.025377] Inode-cache hash table entries: 131072 (order: 8, 1048576 bytes)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.028036] Mount-cache hash table entries: 4096 (order: 3, 32768 bytes)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.029175] Mountpoint-cache hash table entries: 4096 (order: 3, 32768 bytes)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.032004] mce: CPU supports 0 MCE banks
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.036031] Last level iTLB entries: 4KB 512, 2MB 8, 4MB 8
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.040010] Last level dTLB entries: 4KB 512, 2MB 32, 4MB 32, 1GB 0
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.044009] Spectre V2 : Mitigation: Full generic retpoline
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.048008] Spectre V2 : Spectre v2 / SpectreRSB mitigation: Filling RSB on context switch
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.049543] Speculative Store Bypass: Vulnerable
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.050509] Freeing SMP alternatives memory: 36K
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.056000] smpboot: CPU0: Intel(R) Core(TM) i5-2500K CPU @ 3.30GHz (family: 0x6, model: 0x2a, stepping: 0x7)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.056000] Performance Events: unsupported p6 CPU model 42 no PMU driver, software events only.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.056000] Hierarchical SRCU implementation.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.056579] NMI watchdog: Perf event create on CPU 0 failed with -2
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.057800] NMI watchdog: Perf NMI watchdog permanently disabled
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.060093] smp: Bringing up secondary CPUs ...
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.060938] x86: Booting SMP configuration:
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.064009] .... node  #0, CPUs:      #1
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.004000] kvm-clock: cpu 1, msr 0:7ff44041, secondary cpu clock
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.004000] mce: CPU supports 0 MCE banks
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.082845] smp: Brought up 1 node, 2 CPUs
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.082845] smpboot: Max logical packages: 1
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.084009] smpboot: Total of 2 processors activated (13243.28 BogoMIPS)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.088221] devtmpfs: initialized
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.088769] x86/mm: Memory block size: 128MB
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.092204] evm: security.selinux
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.092821] evm: security.SMACK64
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.093406] evm: security.SMACK64EXEC
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.094055] evm: security.SMACK64TRANSMUTE
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.095039] evm: security.SMACK64MMAP
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.095706] evm: security.apparmor
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.096008] evm: security.ima
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.096819] evm: security.capability
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.097690] clocksource: jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 7645041785100000 ns
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.100040] futex hash table entries: 512 (order: 3, 32768 bytes)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.104079] pinctrl core: initialized pinctrl subsystem
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.108178] RTC time:  6:08:52, date: 11/29/18
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.109170] NET: Registered protocol family 16
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.112090] audit: initializing netlink subsys (disabled)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.116006] audit: type=2000 audit(1543471739.439:1): state=initialized audit_enabled=0 res=1
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.117880] cpuidle: using governor ladder
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.117880] cpuidle: using governor menu
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.117880] ACPI: bus type PCI registered
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.120011] acpiphp: ACPI Hot Plug PCI Controller Driver version: 0.5
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.124131] PCI: Using configuration type 1 for base access
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.129036] HugeTLB registered 2.00 MiB page size, pre-allocated 0 pages
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.132209] ACPI: Added _OSI(Module Device)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.132978] ACPI: Added _OSI(Processor Device)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.133737] ACPI: Added _OSI(3.0 _SCP Extensions)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.134641] ACPI: Added _OSI(Processor Aggregator Device)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.135653] ACPI: Added _OSI(Linux-Dell-Video)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.136037] ACPI: Added _OSI(Linux-Lenovo-NV-HDMI-Audio)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.140367] ACPI: Executed 1 blocks of module-level executable AML code
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.145866] ACPI: Interpreter enabled
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.146586] ACPI: (supports S0 S5)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.147190] ACPI: Using IOAPIC for interrupt routing
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.148257] PCI: Using host bridge windows from ACPI; if necessary, use "pci=nocrs" and report a bug
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.150290] ACPI: Enabled 2 GPEs in block 00 to 07
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.159391] ACPI: PCI Root Bridge [PCI0] (domain 0000 [bus 00-ff])
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.160010] acpi PNP0A03:00: _OSC: OS supports [ASPM ClockPM Segments MSI]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.161172] acpi PNP0A03:00: _OSC: not requesting OS control; OS requires [ExtendedConfig ASPM ClockPM MSI]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.162751] acpi PNP0A03:00: fail to add MMCONFIG information, can't access extended PCI configuration space under this bridge.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.164423] PCI host bridge to bus 0000:00
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.165396] pci_bus 0000:00: root bus resource [io  0x0000-0x0cf7 window]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.168009] pci_bus 0000:00: root bus resource [io  0x0d00-0xffff window]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.169145] pci_bus 0000:00: root bus resource [mem 0x000a0000-0x000bffff window]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.171217] pci_bus 0000:00: root bus resource [mem 0x80000000-0xfdffffff window]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.172016] pci_bus 0000:00: root bus resource [bus 00-ff]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.176067] pci 0000:00:00.0: [8086:1237] type 00 class 0x060000
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.176726] pci 0000:00:01.0: [8086:7000] type 00 class 0x060100
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.177496] pci 0000:00:01.1: [8086:7111] type 00 class 0x01018a
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.177916] pci 0000:00:01.1: reg 0x20: [io  0xd000-0xd00f]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.178088] pci 0000:00:01.1: legacy IDE quirk: reg 0x10: [io  0x01f0-0x01f7]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.180013] pci 0000:00:01.1: legacy IDE quirk: reg 0x14: [io  0x03f6]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.181197] pci 0000:00:01.1: legacy IDE quirk: reg 0x18: [io  0x0170-0x0177]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.184004] pci 0000:00:01.1: legacy IDE quirk: reg 0x1c: [io  0x0376]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.185577] pci 0000:00:02.0: [80ee:beef] type 00 class 0x030000
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.188304] pci 0000:00:02.0: reg 0x10: [mem 0xe0000000-0xe0ffffff pref]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.200836] pci 0000:00:03.0: [8086:100e] type 00 class 0x020000
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.202145] pci 0000:00:03.0: reg 0x10: [mem 0xf0000000-0xf001ffff]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.205406] pci 0000:00:03.0: reg 0x18: [io  0xd010-0xd017]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.211063] pci 0000:00:04.0: [80ee:cafe] type 00 class 0x088000
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.212274] pci 0000:00:04.0: reg 0x10: [io  0xd020-0xd03f]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.213709] pci 0000:00:04.0: reg 0x14: [mem 0xf0400000-0xf07fffff]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.214828] pci 0000:00:04.0: reg 0x18: [mem 0xf0800000-0xf0803fff pref]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.220549] pci 0000:00:05.0: [8086:2415] type 00 class 0x040100
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.220703] pci 0000:00:05.0: reg 0x10: [io  0xd100-0xd1ff]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.220785] pci 0000:00:05.0: reg 0x14: [io  0xd200-0xd23f]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.221446] pci 0000:00:07.0: [8086:7113] type 00 class 0x068000
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.221972] pci 0000:00:07.0: quirk: [io  0x4000-0x403f] claimed by PIIX4 ACPI
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.223906] pci 0000:00:07.0: quirk: [io  0x4100-0x410f] claimed by PIIX4 SMB
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.224419] pci 0000:00:14.0: [1000:0030] type 00 class 0x010000
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.228167] pci 0000:00:14.0: reg 0x10: [io  0xd300-0xd3ff]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.229525] pci 0000:00:14.0: reg 0x14: [mem 0xf0820000-0xf083ffff]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.230672] pci 0000:00:14.0: reg 0x18: [mem 0xf0840000-0xf085ffff]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.237573] ACPI: PCI Interrupt Link [LNKA] (IRQs 5 9 10 *11)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.240388] ACPI: PCI Interrupt Link [LNKB] (IRQs 5 9 *10 11)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.241666] ACPI: PCI Interrupt Link [LNKC] (IRQs 5 *9 10 11)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.244126] ACPI: PCI Interrupt Link [LNKD] (IRQs 5 9 10 *11)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.248595] SCSI subsystem initialized
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.252075] libata version 3.00 loaded.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.252075] pci 0000:00:02.0: vgaarb: setting as boot VGA device
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.253193] pci 0000:00:02.0: vgaarb: VGA device added: decodes=io+mem,owns=io+mem,locks=none
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.254638] pci 0000:00:02.0: vgaarb: bridge control possible
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.256018] vgaarb: loaded
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.256603] ACPI: bus type USB registered
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.257338] usbcore: registered new interface driver usbfs
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.258303] usbcore: registered new interface driver hub
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.260057] usbcore: registered new device driver usb
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.261236] EDAC MC: Ver: 3.0.0
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.264355] PCI: Using ACPI for IRQ routing
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.264821] PCI: pci_cache_line_size set to 64 bytes
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.265010] e820: reserve RAM buffer [mem 0x0009fc00-0x0009ffff]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.265014] e820: reserve RAM buffer [mem 0x7fff0000-0x7fffffff]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.265142] NetLabel: Initializing
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.265807] NetLabel:  domain hash size = 128
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.268014] NetLabel:  protocols = UNLABELED CIPSOv4 CALIPSO
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.269005] NetLabel:  unlabeled traffic allowed by default
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.276129] clocksource: Switched to clocksource kvm-clock
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.289773] VFS: Disk quotas dquot_6.6.0
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.290515] VFS: Dquot-cache hash table entries: 512 (order 0, 4096 bytes)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.291790] AppArmor: AppArmor Filesystem Enabled
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.292640] pnp: PnP ACPI init
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.293364] pnp 00:00: Plug and Play ACPI device, IDs PNP0303 (active)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.293436] pnp 00:01: Plug and Play ACPI device, IDs PNP0f03 (active)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.293840] pnp 00:02: Plug and Play ACPI device, IDs PNP0501 (active)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.294404] pnp: PnP ACPI: found 3 devices
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.366567] clocksource: acpi_pm: mask: 0xffffff max_cycles: 0xffffff, max_idle_ns: 2085701024 ns
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.421621] pci_bus 0000:00: resource 4 [io  0x0000-0x0cf7 window]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.421623] pci_bus 0000:00: resource 5 [io  0x0d00-0xffff window]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.421624] pci_bus 0000:00: resource 6 [mem 0x000a0000-0x000bffff window]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.421626] pci_bus 0000:00: resource 7 [mem 0x80000000-0xfdffffff window]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.421697] NET: Registered protocol family 2
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.423417] TCP established hash table entries: 16384 (order: 5, 131072 bytes)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.452941] TCP bind hash table entries: 16384 (order: 6, 262144 bytes)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.455160] TCP: Hash tables configured (established 16384 bind 16384)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.458038] UDP hash table entries: 1024 (order: 3, 32768 bytes)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.488063] UDP-Lite hash table entries: 1024 (order: 3, 32768 bytes)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.489766] NET: Registered protocol family 1
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.490656] pci 0000:00:00.0: Limiting direct PCI/PCI transfers
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.491729] pci 0000:00:01.0: Activating ISA DMA hang workarounds
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.492924] pci 0000:00:02.0: Video device with shadowed ROM at [mem 0x000c0000-0x000dffff]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.607925] PCI: CLS 0 bytes, default 64
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.607977] Unpacking initramfs...
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.910584] Freeing initrd memory: 18968K
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.911548] platform rtc_cmos: registered platform RTC device (no PNP device found)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.913151] Scanning for low memory corruption every 60 seconds
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.914769] Initialise system trusted keyrings
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.915538] Key type blacklist registered
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.916342] workingset: timestamp_bits=36 max_order=19 bucket_order=0
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.932905] zbud: loaded
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.940817] squashfs: version 4.0 (2009/01/31) Phillip Lougher
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.942044] fuse init (API version 7.26)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.945248] Key type asymmetric registered
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.945982] Asymmetric key parser 'x509' registered
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.946810] Block layer SCSI generic (bsg) driver version 0.4 loaded (major 246)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.960571] io scheduler noop registered
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.961252] io scheduler deadline registered
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.962036] io scheduler cfq registered (default)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.963077] intel_idle: Please enable MWAIT in BIOS SETUP
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.963190] ACPI: AC Adapter [AC] (on-line)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.963968] input: Power Button as /devices/LNXSYSTM:00/LNXPWRBN:00/input/input0
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.965270] ACPI: Power Button [PWRF]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.965997] input: Sleep Button as /devices/LNXSYSTM:00/LNXSLPBN:00/input/input1
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.973969] ACPI: Sleep Button [SLPF]
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.975111] Serial: 8250/16550 driver, 32 ports, IRQ sharing enabled
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.006017] 00:02: ttyS0 at I/O 0x3f8 (irq = 4, base_baud = 115200) is a 16550A
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.010869] Linux agpgart interface v0.103
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.013984] loop: module loaded
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.014710] ata_piix 0000:00:01.1: version 2.13
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.015132] scsi host0: ata_piix
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.015962] scsi host1: ata_piix
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.016594] ata1: PATA max UDMA/33 cmd 0x1f0 ctl 0x3f6 bmdma 0xd000 irq 14
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.024972] ata2: PATA max UDMA/33 cmd 0x170 ctl 0x376 bmdma 0xd008 irq 15
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.026550] libphy: Fixed MDIO Bus: probed
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.027255] tun: Universal TUN/TAP device driver, 1.6
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.028188] PPP generic driver version 2.4.2
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.035738] ehci_hcd: USB 2.0 'Enhanced' Host Controller (EHCI) Driver
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.037257] ehci-pci: EHCI PCI platform driver
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.038175] ehci-platform: EHCI generic platform driver
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.039121] ohci_hcd: USB 1.1 'Open' Host Controller (OHCI) Driver
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.040140] ohci-pci: OHCI PCI platform driver
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.040924] ohci-platform: OHCI generic platform driver
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.041848] uhci_hcd: USB Universal Host Controller Interface driver
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.042922] i8042: PNP: PS/2 Controller [PNP0303:PS2K,PNP0f03:PS2M] at 0x60,0x64 irq 1,12
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.044804] serio: i8042 KBD port at 0x60,0x64 irq 1
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.045637] serio: i8042 AUX port at 0x60,0x64 irq 12
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.046683] mousedev: PS/2 mouse device common for all mice
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.055263] input: AT Translated Set 2 keyboard as /devices/platform/i8042/serio0/input/input2
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.056769] rtc_cmos rtc_cmos: rtc core: registered rtc_cmos as rtc0
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.057930] rtc_cmos rtc_cmos: alarms up to one day, 114 bytes nvram
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.065599] i2c /dev entries driver
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.066245] pcie_mp2_amd: AMD(R) PCI-E MP2 Communication Driver Version: 1.0
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.075395] device-mapper: uevent: version 1.0.3
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.076267] device-mapper: ioctl: 4.37.0-ioctl (2017-09-20) initialised: dm-devel@redhat.com
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.083970] ledtrig-cpu: registered to indicate activity on CPUs
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.086745] NET: Registered protocol family 10
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.091131] Segment Routing with IPv6
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.091876] NET: Registered protocol family 17
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.092724] Key type dns_resolver registered
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.093638] RAS: Correctable Errors collector initialized.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.094610] sched_clock: Marking stable (1093542887, 0)->(2190376226, -1096833339)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.096195] registered taskstats version 1
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.101121] Loading compiled-in X.509 certificates
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.106898] Loaded X.509 cert 'Build time autogenerated kernel key: 28c680bedc8638650c29d29ff1fd33ae66a2014d'
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.108685] zswap: loaded using pool lzo/zbud
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.115260] Key type big_key registered
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.115940] Key type trusted registered
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.118505] Key type encrypted registered
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.121559] AppArmor: AppArmor sha1 policy hashing enabled
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.129587] ima: No TPM chip found, activating TPM-bypass! (rc=-19)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.132314] ima: Allocated hash algorithm: sha1
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.133397] evm: HMAC attrs: 0x1
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.134753]   Magic number: 10:908:115
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.135687] rtc_cmos rtc_cmos: setting system clock to 2018-11-29 06:08:53 UTC (1543471733)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.144482] BIOS EDD facility v0.16 2004-Jun-25, 0 devices found
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.145567] EDD information not available.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.189886] Freeing unused kernel memory: 2408K
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.201356] Write protecting the kernel read-only data: 20480k
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.205186] Freeing unused kernel memory: 2008K
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.217741] Freeing unused kernel memory: 1896K
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.231823] x86/mm: Checked W+X mappings: passed, no W+X pages found.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.234943] x86/mm: Checking user space page tables
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.246842] x86/mm: Checked W+X mappings: passed, no W+X pages found.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.373994] e1000: Intel(R) PRO/1000 Network Driver - version 7.3.21-k8-NAPI
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.375548] e1000: Copyright (c) 1999-2006 Intel Corporation.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.394460] Fusion MPT base driver 3.04.20
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.395333] Copyright (c) 1999-2008 LSI Corporation
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.402095] Fusion MPT SPI Host driver 3.04.20
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.419616] AVX version of gcm_enc/dec engaged.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.427341] AES CTR mode by8 optimization enabled
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.597339] input: ImExPS/2 Generic Explorer Mouse as /devices/platform/i8042/serio1/input/input4
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.869738] e1000 0000:00:03.0 eth0: (PCI:33MHz:32-bit) 02:67:f0:a3:a8:75
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.882645] e1000 0000:00:03.0 eth0: Intel(R) PRO/1000 Network Connection
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.892659] mptbase: ioc0: Initiating bringup
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.893058] e1000 0000:00:03.0 enp0s3: renamed from eth0
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.916465] tsc: Refined TSC clocksource calibration: 3312.111 MHz
    Nov 29 06:09:07 ubuntu-bionic kernel: [    1.917873] clocksource: tsc: mask: 0xffffffffffffffff max_cycles: 0x2fbdfd255e3, max_idle_ns: 440795316638 ns
    Nov 29 06:09:07 ubuntu-bionic kernel: [    2.025300] ioc0: LSI53C1030 A0: Capabilities={Initiator}
    Nov 29 06:09:07 ubuntu-bionic kernel: [    3.621422] scsi host2: ioc0: LSI53C1030 A0, FwRev=00000000h, Ports=1, MaxQ=256, IRQ=20
    Nov 29 06:09:07 ubuntu-bionic kernel: [    4.060892] scsi 2:0:0:0: Direct-Access     VBOX     HARDDISK         1.0  PQ: 0 ANSI: 5
    Nov 29 06:09:07 ubuntu-bionic kernel: [    4.140109] scsi target2:0:0: Beginning Domain Validation
    Nov 29 06:09:07 ubuntu-bionic kernel: [    4.153260] scsi target2:0:0: Domain Validation skipping write tests
    Nov 29 06:09:07 ubuntu-bionic kernel: [    4.619076] scsi target2:0:0: Ending Domain Validation
    Nov 29 06:09:07 ubuntu-bionic kernel: [    4.621910] scsi target2:0:0: asynchronous
    Nov 29 06:09:07 ubuntu-bionic kernel: [    4.626551] scsi 2:0:1:0: Direct-Access     VBOX     HARDDISK         1.0  PQ: 0 ANSI: 5
    Nov 29 06:09:07 ubuntu-bionic kernel: [    4.668026] scsi target2:0:1: Beginning Domain Validation
    Nov 29 06:09:07 ubuntu-bionic kernel: [    4.669444] random: fast init done
    Nov 29 06:09:07 ubuntu-bionic kernel: [    4.687565] scsi target2:0:1: Domain Validation skipping write tests
    Nov 29 06:09:07 ubuntu-bionic kernel: [    4.689192] scsi target2:0:1: Ending Domain Validation
    Nov 29 06:09:07 ubuntu-bionic kernel: [    5.085138] scsi target2:0:1: asynchronous
    Nov 29 06:09:07 ubuntu-bionic kernel: [    5.621731] random: systemd-udevd: uninitialized urandom read (16 bytes read)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    5.621984] sd 2:0:0:0: Attached scsi generic sg0 type 0
    Nov 29 06:09:07 ubuntu-bionic kernel: [    5.622233] sd 2:0:0:0: [sda] 20971520 512-byte logical blocks: (10.7 GB/10.0 GiB)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    5.622282] sd 2:0:0:0: [sda] Write Protect is off
    Nov 29 06:09:07 ubuntu-bionic kernel: [    5.622283] sd 2:0:0:0: [sda] Mode Sense: 04 00 10 00
    Nov 29 06:09:07 ubuntu-bionic kernel: [    5.622375] sd 2:0:0:0: [sda] Incomplete mode parameter data
    Nov 29 06:09:07 ubuntu-bionic kernel: [    5.622376] sd 2:0:0:0: [sda] Assuming drive cache: write through
    Nov 29 06:09:07 ubuntu-bionic kernel: [    5.622991] sd 2:0:1:0: Attached scsi generic sg1 type 0
    Nov 29 06:09:07 ubuntu-bionic kernel: [    5.623251]  sda: sda1
    Nov 29 06:09:07 ubuntu-bionic kernel: [    5.623407] sd 2:0:1:0: [sdb] 20480 512-byte logical blocks: (10.5 MB/10.0 MiB)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    5.623449] sd 2:0:1:0: [sdb] Write Protect is off
    Nov 29 06:09:07 ubuntu-bionic kernel: [    5.623450] sd 2:0:1:0: [sdb] Mode Sense: 04 00 10 00
    Nov 29 06:09:07 ubuntu-bionic kernel: [    5.623576] sd 2:0:1:0: [sdb] Incomplete mode parameter data
    Nov 29 06:09:07 ubuntu-bionic kernel: [    5.623577] sd 2:0:1:0: [sdb] Assuming drive cache: write through
    Nov 29 06:09:07 ubuntu-bionic kernel: [    5.623687] sd 2:0:0:0: [sda] Attached SCSI disk
    Nov 29 06:09:07 ubuntu-bionic kernel: [    5.625439] sd 2:0:1:0: [sdb] Attached SCSI disk
    Nov 29 06:09:07 ubuntu-bionic kernel: [    5.770666] random: systemd-udevd: uninitialized urandom read (16 bytes read)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    5.775050] random: systemd-udevd: uninitialized urandom read (16 bytes read)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    7.324292] raid6: sse2x1   gen()  7717 MB/s
    Nov 29 06:09:07 ubuntu-bionic kernel: [    7.372336] raid6: sse2x1   xor()  5236 MB/s
    Nov 29 06:09:07 ubuntu-bionic kernel: [    7.420043] raid6: sse2x2   gen()  9409 MB/s
    Nov 29 06:09:07 ubuntu-bionic kernel: [    7.468616] raid6: sse2x2   xor()  6407 MB/s
    Nov 29 06:09:07 ubuntu-bionic kernel: [    7.516367] raid6: sse2x4   gen()  9147 MB/s
    Nov 29 06:09:07 ubuntu-bionic kernel: [    7.572232] raid6: sse2x4   xor()  5875 MB/s
    Nov 29 06:09:07 ubuntu-bionic kernel: [    7.573081] raid6: using algorithm sse2x2 gen() 9409 MB/s
    Nov 29 06:09:07 ubuntu-bionic kernel: [    7.574065] raid6: .... xor() 6407 MB/s, rmw enabled
    Nov 29 06:09:07 ubuntu-bionic kernel: [    7.580205] raid6: using ssse3x2 recovery algorithm
    Nov 29 06:09:07 ubuntu-bionic kernel: [    7.583249] xor: automatically using best checksumming function   avx       
    Nov 29 06:09:07 ubuntu-bionic kernel: [    7.586975] async_tx: api initialized (async)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    7.659558] Btrfs loaded, crc32c=crc32c-intel
    Nov 29 06:09:07 ubuntu-bionic kernel: [    7.692047] EXT4-fs (sda1): mounted filesystem with ordered data mode. Opts: (null)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    7.923773] ip_tables: (C) 2000-2006 Netfilter Core Team
    Nov 29 06:09:07 ubuntu-bionic kernel: [    7.934572] systemd[1]: systemd 237 running in system mode. (+PAM +AUDIT +SELINUX +IMA +APPARMOR +SMACK +SYSVINIT +UTMP +LIBCRYPTSETUP +GCRYPT +GNUTLS +ACL +XZ +LZ4 +SECCOMP +BLKID +ELFUTILS +KMOD -IDN2 +IDN -PCRE2 default-hierarchy=hybrid)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    7.945023] systemd[1]: Detected virtualization oracle.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    7.953953] systemd[1]: Detected architecture x86-64.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    7.975639] systemd[1]: Set hostname to <ubuntu>.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    7.979533] systemd[1]: Initializing machine ID from random generator.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    7.981590] systemd[1]: Installed transient /etc/machine-id file.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    8.240857] systemd[1]: Created slice User and Session Slice.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    8.243454] systemd[1]: Reached target Swap.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    8.245537] systemd[1]: Started Forward Password Requests to Wall Directory Watch.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    8.249375] systemd[1]: Created slice System Slice.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    8.358591] Loading iSCSI transport class v2.0-870.
    Nov 29 06:09:07 ubuntu-bionic kernel: [    8.403766] iscsi: registered transport (tcp)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    8.512130] iscsi: registered transport (iser)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    8.682914] EXT4-fs (sda1): re-mounted. Opts: (null)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    9.040060] systemd-journald[404]: Received request to flush runtime journal from PID 1
    Nov 29 06:09:07 ubuntu-bionic kernel: [    9.306539] ACPI: Video Device [GFX0] (multi-head: yes  rom: no  post: no)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    9.306610] input: Video Bus as /devices/LNXSYSTM:00/LNXSYBUS:00/PNP0A03:00/LNXVIDEO:00/input/input5
    Nov 29 06:09:07 ubuntu-bionic kernel: [    9.458081] vgdrvHeartbeatInit: Setting up heartbeat to trigger every 2000 milliseconds
    Nov 29 06:09:07 ubuntu-bionic kernel: [    9.458420] input: Unspecified device as /devices/pci0000:00/0000:00:04.0/input/input6
    Nov 29 06:09:07 ubuntu-bionic kernel: [    9.464579] vboxguest: misc device minor 55, IRQ 20, I/O port d020, MMIO at 00000000f0400000 (size 0x400000)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    9.464581] vboxguest: Successfully loaded version 5.2.8_KernelUbuntu (interface 0x00010004)
    Nov 29 06:09:07 ubuntu-bionic kernel: [    9.556924] random: crng init done
    Nov 29 06:09:07 ubuntu-bionic kernel: [    9.556926] random: 7 urandom warning(s) missed due to ratelimiting
    Nov 29 06:09:07 ubuntu-bionic kernel: [   10.316278] audit: type=1400 audit(1543471742.676:2): apparmor="STATUS" operation="profile_load" profile="unconfined" name="/sbin/dhclient" pid=505 comm="apparmor_parser"
    Nov 29 06:09:07 ubuntu-bionic kernel: [   10.317562] audit: type=1400 audit(1543471742.680:3): apparmor="STATUS" operation="profile_load" profile="unconfined" name="/usr/lib/NetworkManager/nm-dhcp-client.action" pid=505 comm="apparmor_parser"
    Nov 29 06:09:07 ubuntu-bionic kernel: [   10.324749] audit: type=1400 audit(1543471742.688:4): apparmor="STATUS" operation="profile_load" profile="unconfined" name="/usr/lib/NetworkManager/nm-dhcp-helper" pid=505 comm="apparmor_parser"
    Nov 29 06:09:07 ubuntu-bionic kernel: [   10.325888] audit: type=1400 audit(1543471742.688:5): apparmor="STATUS" operation="profile_load" profile="unconfined" name="/usr/lib/connman/scripts/dhclient-script" pid=505 comm="apparmor_parser"
    Nov 29 06:09:07 ubuntu-bionic kernel: [   10.398524] audit: type=1400 audit(1543471742.760:6): apparmor="STATUS" operation="profile_load" profile="unconfined" name="/usr/bin/lxc-start" pid=540 comm="apparmor_parser"
    Nov 29 06:09:07 ubuntu-bionic kernel: [   10.596913] audit: type=1400 audit(1543471742.956:7): apparmor="STATUS" operation="profile_load" profile="unconfined" name="lxc-container-default" pid=504 comm="apparmor_parser"
    Nov 29 06:09:07 ubuntu-bionic kernel: [   10.596922] audit: type=1400 audit(1543471742.960:8): apparmor="STATUS" operation="profile_load" profile="unconfined" name="lxc-container-default-cgns" pid=504 comm="apparmor_parser"
    Nov 29 06:09:07 ubuntu-bionic kernel: [   10.597149] audit: type=1400 audit(1543471742.960:9): apparmor="STATUS" operation="profile_load" profile="unconfined" name="lxc-container-default-with-mounting" pid=504 comm="apparmor_parser"
    Nov 29 06:09:07 ubuntu-bionic kernel: [   10.598035] audit: type=1400 audit(1543471742.960:10): apparmor="STATUS" operation="profile_load" profile="unconfined" name="lxc-container-default-with-nesting" pid=504 comm="apparmor_parser"
    Nov 29 06:09:07 ubuntu-bionic kernel: [   10.660372] audit: type=1400 audit(1543471743.020:11): apparmor="STATUS" operation="profile_load" profile="unconfined" name="/usr/bin/man" pid=550 comm="apparmor_parser"
    Nov 29 06:09:07 ubuntu-bionic kernel: [   10.924783] ISO 9660 Extensions: Microsoft Joliet Level 3
    Nov 29 06:09:07 ubuntu-bionic kernel: [   10.927291] ISO 9660 Extensions: RRIP_1991A
    Nov 29 06:09:07 ubuntu-bionic kernel: [   11.410658] IPv6: ADDRCONF(NETDEV_UP): enp0s3: link is not ready
    Nov 29 06:09:07 ubuntu-bionic kernel: [   11.416871] e1000: enp0s3 NIC Link is Up 1000 Mbps Full Duplex, Flow Control: RX
    Nov 29 06:09:07 ubuntu-bionic kernel: [   11.417193] IPv6: ADDRCONF(NETDEV_CHANGE): enp0s3: link becomes ready
    Nov 29 06:09:07 ubuntu-bionic kernel: [   13.837017] EXT4-fs (sda1): resizing filesystem from 576000 to 2621179 blocks
    Nov 29 06:09:07 ubuntu-bionic kernel: [   13.884362] EXT4-fs (sda1): resized filesystem to 2621179
    Nov 29 06:09:07 ubuntu-bionic kernel: [   15.187424] new mount options do not match the existing superblock, will be ignored
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: +---[ECDSA 256]---+
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |      .o   oo++. |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |       oo .o.=o. |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |      . =.o Bo=E |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |     o o.oo*BB+o |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |    . . S..O*Booo|
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |          .o=++ .|
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |            .+   |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |            .    |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |                 |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: +----[SHA256]-----+
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: Generating public/private ed25519 key pair.
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: Your identification has been saved in /etc/ssh/ssh_host_ed25519_key.
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: Your public key has been saved in /etc/ssh/ssh_host_ed25519_key.pub.
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: The key fingerprint is:
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: SHA256:6ZnAE12MifYiPKDUERsr5/oTnE04XBsgGq3PNe7GOqY root@ubuntu-bionic
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: The key's randomart image is:
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: +--[ED25519 256]--+
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |.o.=+  . +.      |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |.o+.+oo.o..      |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |o+.*o.+..        |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |o ++*+....       |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: | o.+=++.S        |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |  ++.. + o       |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: | . o.   +        |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |  +.+            |
    Nov 29 06:09:07 ubuntu-bionic rsyslogd: imuxsock: Acquired UNIX socket '/run/systemd/journal/syslog' (fd 3) from systemd.  [v8.32.0]
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Initial cloud-init job (metadata service crawler).
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: |Eo.=.            |
    Nov 29 06:09:07 ubuntu-bionic cloud-init[659]: +----[SHA256]-----+
    Nov 29 06:09:07 ubuntu-bionic rsyslogd: rsyslogd's groupid changed to 106
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Reached target System Initialization.
    Nov 29 06:09:07 ubuntu-bionic rsyslogd: rsyslogd's userid changed to 102
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Daily Cleanup of Temporary Directories.
    Nov 29 06:09:07 ubuntu-bionic networkd-dispatcher[797]: No valid path found for iwconfig
    Nov 29 06:09:07 ubuntu-bionic networkd-dispatcher[797]: No valid path found for iw
    Nov 29 06:09:07 ubuntu-bionic rsyslogd:  [origin software="rsyslogd" swVersion="8.32.0" x-pid="877" x-info="http://www.rsyslog.com"] start
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Message of the Day.
    Nov 29 06:09:07 ubuntu-bionic apport[811]:  * Starting automatic crash report generation: apport
    Nov 29 06:09:07 ubuntu-bionic dbus-daemon[899]: [system] AppArmor D-Bus mediation is enabled
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Daily apt download activities.
    Nov 29 06:09:07 ubuntu-bionic dbus-daemon[899]: [system] Activating via systemd: service name='org.freedesktop.PolicyKit1' unit='polkit.service' requested by ':1.5' (uid=0 pid=849 comm="/usr/lib/accountsservice/accounts-daemon " label="unconfined")
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Listening on Open-iSCSI iscsid Socket.
    Nov 29 06:09:07 ubuntu-bionic pollinate[932]: client sent challenge to [https://entropy.ubuntu.com/]
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Daily apt upgrade and clean activities.
    Nov 29 06:09:07 ubuntu-bionic lxcfs[848]: mount namespace: 5
    Nov 29 06:09:07 ubuntu-bionic lxcfs[848]: hierarchies:
    Nov 29 06:09:07 ubuntu-bionic lxcfs[848]:   0: fd:   6: net_cls,net_prio
    Nov 29 06:09:07 ubuntu-bionic lxcfs[848]:   1: fd:   7: hugetlb
    Nov 29 06:09:07 ubuntu-bionic lxcfs[848]:   2: fd:   8: blkio
    Nov 29 06:09:07 ubuntu-bionic lxcfs[848]:   3: fd:   9: pids
    Nov 29 06:09:07 ubuntu-bionic lxcfs[848]:   4: fd:  10: cpuset
    Nov 29 06:09:07 ubuntu-bionic lxcfs[848]:   5: fd:  11: devices
    Nov 29 06:09:07 ubuntu-bionic lxcfs[848]:   6: fd:  12: freezer
    Nov 29 06:09:07 ubuntu-bionic lxcfs[848]:   7: fd:  13: memory
    Nov 29 06:09:07 ubuntu-bionic lxcfs[848]:   8: fd:  14: rdma
    Nov 29 06:09:07 ubuntu-bionic lxcfs[848]:   9: fd:  15: cpu,cpuacct
    Nov 29 06:09:07 ubuntu-bionic lxcfs[848]:  10: fd:  16: perf_event
    Nov 29 06:09:07 ubuntu-bionic lxcfs[848]:  11: fd:  17: name=systemd
    Nov 29 06:09:07 ubuntu-bionic lxcfs[848]:  12: fd:  18: unified
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Listening on D-Bus System Message Bus Socket.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting LXD - unix socket.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started ACPI Events Check.
    Nov 29 06:09:07 ubuntu-bionic grub-common[878]:  * Recording successful boot for GRUB
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Reached target Paths.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting Socket activation for snappy daemon.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Listening on UUID daemon activation socket.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Listening on ACPID Listen Socket.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Discard unused blocks once a week.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Reached target Timers.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Reached target Network is Online.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting Availability of block devices...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Reached target Remote File Systems (Pre).
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Reached target Remote File Systems.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Reached target Cloud-config availability.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Listening on LXD - unix socket.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Listening on Socket activation for snappy daemon.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Availability of block devices.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Reached target Sockets.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Reached target Basic System.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Unattended Upgrades Shutdown.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting Dispatcher daemon for systemd-networkd...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting LSB: automatic crash report generation...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting Login Service...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting Permit User Sessions...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started FUSE filesystem for LXC.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting Accounts Service...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Deferred execution scheduler.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting System Logging Service...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting LSB: Record successful boot for GRUB...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started D-Bus System Message Bus.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started irqbalance daemon.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting Virtualbox guest utils...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting Pollinate to seed the pseudo random number generator...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Regular background program processing daemon.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting Snappy daemon...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Starting LXD - container startup/shutdown...
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started System Logging Service.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Dispatcher daemon for systemd-networkd.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Permit User Sessions.
    Nov 29 06:09:07 ubuntu-bionic systemd[1]: Started Login Service.
    Nov 29 06:09:07 ubuntu-bionic snapd[956]: AppArmor status: apparmor is enabled and all features are available
    Nov 29 06:09:07 ubuntu-bionic cron[955]: (CRON) INFO (pidfile fd = 3)
    Nov 29 06:09:07 ubuntu-bionic cron[955]: (CRON) INFO (Running @reboot jobs)
    Nov 29 06:09:08 ubuntu-bionic systemd[1]: Starting Authorization Manager...
    Nov 29 06:09:08 ubuntu-bionic systemd[1]: Starting Terminate Plymouth Boot Screen...
    Nov 29 06:09:08 ubuntu-bionic systemd[1]: Starting Hold until boot process finishes up...
    Nov 29 06:09:08 ubuntu-bionic systemd[1]: Started Hold until boot process finishes up.
    Nov 29 06:09:08 ubuntu-bionic systemd[1]: Started Terminate Plymouth Boot Screen.
    Nov 29 06:09:08 ubuntu-bionic systemd[1]: Started Serial Getty on ttyS0.
    Nov 29 06:09:08 ubuntu-bionic systemd[1]: Starting Set console scheme...
    Nov 29 06:09:08 ubuntu-bionic apport[811]:    ...done.
    Nov 29 06:09:08 ubuntu-bionic systemd[1]: Started LSB: automatic crash report generation.
    Nov 29 06:09:08 ubuntu-bionic systemd[1]: Started Set console scheme.
    Nov 29 06:09:08 ubuntu-bionic systemd[1]: Created slice system-getty.slice.
    Nov 29 06:09:08 ubuntu-bionic grub-common[878]:    ...done.
    Nov 29 06:09:08 ubuntu-bionic virtualbox-guest-utils[923]:  * Starting VirtualBox Additions
    Nov 29 06:09:08 ubuntu-bionic systemd[1]: Started Getty on tty1.
    Nov 29 06:09:08 ubuntu-bionic systemd[1]: Reached target Login Prompts.
    Nov 29 06:09:08 ubuntu-bionic systemd[1]: Started LSB: Record successful boot for GRUB.
    Nov 29 06:09:08 ubuntu-bionic kernel: [   15.843395] vboxsf: Successfully loaded version 5.2.8_KernelUbuntu (interface 0x00010004)
    Nov 29 06:09:08 ubuntu-bionic systemd[1]: Started LXD - container startup/shutdown.
    Nov 29 06:09:08 ubuntu-bionic polkitd[1049]: started daemon version 0.105 using authority implementation `local' version `0.105'
    Nov 29 06:09:08 ubuntu-bionic dbus-daemon[899]: [system] Successfully activated service 'org.freedesktop.PolicyKit1'
    Nov 29 06:09:08 ubuntu-bionic systemd[1]: Started Authorization Manager.
    Nov 29 06:09:08 ubuntu-bionic accounts-daemon[849]: started daemon version 0.6.45
    Nov 29 06:09:08 ubuntu-bionic systemd[1]: Started Accounts Service.
    Nov 29 06:09:08 ubuntu-bionic virtualbox-guest-utils[923]: VBoxService 5.2.18_Ubuntu r123745 (verbosity: 0) linux.amd64 (Oct 10 2018 13:27:01) release log
    Nov 29 06:09:08 ubuntu-bionic virtualbox-guest-utils[923]: 00:00:00.000099 main     Log opened 2018-11-29T06:09:08.287916000Z
    Nov 29 06:09:08 ubuntu-bionic virtualbox-guest-utils[923]: 00:00:00.000210 main     OS Product: Linux
    Nov 29 06:09:08 ubuntu-bionic virtualbox-guest-utils[923]: 00:00:00.000248 main     OS Release: 4.15.0-39-generic
    Nov 29 06:09:08 ubuntu-bionic virtualbox-guest-utils[923]: 00:00:00.000282 main     OS Version: #42-Ubuntu SMP Tue Oct 23 15:48:01 UTC 2018
    Nov 29 06:09:08 ubuntu-bionic kernel: [   15.923579] VBoxService 5.2.18_Ubuntu r123745 (verbosity: 0) linux.amd64 (Oct 10 2018 13:27:01) release log
    Nov 29 06:09:08 ubuntu-bionic kernel: [   15.923579] 00:00:00.000099 main     Log opened 2018-11-29T06:09:08.287916000Z
    Nov 29 06:09:08 ubuntu-bionic kernel: [   15.923645] 00:00:00.000210 main     OS Product: Linux
    Nov 29 06:09:08 ubuntu-bionic kernel: [   15.923680] 00:00:00.000248 main     OS Release: 4.15.0-39-generic
    Nov 29 06:09:08 ubuntu-bionic kernel: [   15.923714] 00:00:00.000282 main     OS Version: #42-Ubuntu SMP Tue Oct 23 15:48:01 UTC 2018
    Nov 29 06:09:08 ubuntu-bionic kernel: [   15.923756] 00:00:00.000315 main     Executable: /usr/sbin/VBoxService
    Nov 29 06:09:08 ubuntu-bionic kernel: [   15.923756] 00:00:00.000316 main     Process ID: 1127
    Nov 29 06:09:08 ubuntu-bionic kernel: [   15.923756] 00:00:00.000316 main     Package type: LINUX_64BITS_GENERIC (OSE)
    Nov 29 06:09:08 ubuntu-bionic virtualbox-guest-utils[923]: 00:00:00.000315 main     Executable: /usr/sbin/VBoxService
    Nov 29 06:09:08 ubuntu-bionic virtualbox-guest-utils[923]: 00:00:00.000316 main     Process ID: 1127
    Nov 29 06:09:08 ubuntu-bionic virtualbox-guest-utils[923]: 00:00:00.000316 main     Package type: LINUX_64BITS_GENERIC (OSE)
    Nov 29 06:09:08 ubuntu-bionic virtualbox-guest-utils[923]: 00:00:00.001670 main     5.2.18_Ubuntu r123745 started. Verbose level = 0
    Nov 29 06:09:08 ubuntu-bionic virtualbox-guest-utils[923]:    ...done.
    Nov 29 06:09:08 ubuntu-bionic kernel: [   15.925117] 00:00:00.001670 main     5.2.18_Ubuntu r123745 started. Verbose level = 0
    Nov 29 06:09:08 ubuntu-bionic systemd[1]: Started Virtualbox guest utils.
    Nov 29 06:09:08 ubuntu-bionic snapd[956]: 2018/11/29 06:09:08.321249 helpers.go:119: error trying to compare the snap system key: system-key missing on disk
    Nov 29 06:09:08 ubuntu-bionic snapd[956]: 2018/11/29 06:09:08.329014 daemon.go:343: started snapd/2.34.2+18.04 (series 16; classic) ubuntu/18.04 (amd64) linux/4.15.0-39-generic.
    Nov 29 06:09:08 ubuntu-bionic systemd[1]: Started Snappy daemon.
    Nov 29 06:09:08 ubuntu-bionic systemd[1]: Starting Wait until snapd is fully seeded...
    Nov 29 06:09:09 ubuntu-bionic pollinate[932]: client verified challenge/response with [https://entropy.ubuntu.com/]
    Nov 29 06:09:09 ubuntu-bionic pollinate[932]: client hashed response from [https://entropy.ubuntu.com/]
    Nov 29 06:09:09 ubuntu-bionic pollinate[932]: client successfully seeded [/dev/urandom]
    Nov 29 06:09:09 ubuntu-bionic systemd[1]: Started Pollinate to seed the pseudo random number generator.
    Nov 29 06:09:09 ubuntu-bionic systemd[1]: Starting OpenBSD Secure Shell server...
    Nov 29 06:09:09 ubuntu-bionic systemd[1]: Started OpenBSD Secure Shell server.
    Nov 29 06:09:10 ubuntu-bionic systemd[1]: Created slice User Slice of vagrant.
    Nov 29 06:09:10 ubuntu-bionic systemd[1]: Starting User Manager for UID 1000...
    Nov 29 06:09:10 ubuntu-bionic systemd[1]: Started Session 1 of user vagrant.
    Nov 29 06:09:10 ubuntu-bionic systemd[1228]: Listening on GnuPG cryptographic agent and passphrase cache.
    Nov 29 06:09:10 ubuntu-bionic systemd[1228]: Listening on GnuPG network certificate management daemon.
    Nov 29 06:09:10 ubuntu-bionic systemd[1228]: Listening on GnuPG cryptographic agent and passphrase cache (restricted).
    Nov 29 06:09:10 ubuntu-bionic systemd[1228]: Listening on GnuPG cryptographic agent and passphrase cache (access for web browsers).
    Nov 29 06:09:10 ubuntu-bionic systemd[1228]: Listening on GnuPG cryptographic agent (ssh-agent emulation).
    Nov 29 06:09:10 ubuntu-bionic systemd[1228]: Reached target Sockets.
    Nov 29 06:09:10 ubuntu-bionic systemd[1228]: Reached target Paths.
    Nov 29 06:09:10 ubuntu-bionic systemd[1228]: Reached target Timers.
    Nov 29 06:09:10 ubuntu-bionic systemd[1228]: Reached target Basic System.
    Nov 29 06:09:10 ubuntu-bionic systemd[1]: Started User Manager for UID 1000.
    Nov 29 06:09:10 ubuntu-bionic systemd[1228]: Reached target Default.
    Nov 29 06:09:10 ubuntu-bionic systemd[1228]: Startup finished in 63ms.
    Nov 29 06:09:12 ubuntu-bionic systemd[1]: Started Wait until snapd is fully seeded.
    Nov 29 06:09:12 ubuntu-bionic systemd[1]: Starting Apply the settings specified in cloud-config...
    Nov 29 06:09:12 ubuntu-bionic systemd[1]: Reached target Multi-User System.
    Nov 29 06:09:12 ubuntu-bionic systemd[1]: Reached target Graphical Interface.
    Nov 29 06:09:12 ubuntu-bionic systemd[1]: Starting Update UTMP about System Runlevel Changes...
    Nov 29 06:09:12 ubuntu-bionic systemd[1]: Started Update UTMP about System Runlevel Changes.
    Nov 29 06:09:13 ubuntu-bionic cloud-init[1299]: Cloud-init v. 18.4-0ubuntu1~18.04.1 running 'modules:config' at Thu, 29 Nov 2018 06:09:12 +0000. Up 20.33 seconds.
    Nov 29 06:09:13 ubuntu-bionic systemd[1]: Started Apply the settings specified in cloud-config.
    Nov 29 06:09:13 ubuntu-bionic systemd[1]: Starting Execute cloud user/final scripts...
    Nov 29 06:09:14 ubuntu-bionic ec2: 
    Nov 29 06:09:14 ubuntu-bionic ec2: #############################################################
    Nov 29 06:09:14 ubuntu-bionic ec2: -----BEGIN SSH HOST KEY FINGERPRINTS-----
    Nov 29 06:09:14 ubuntu-bionic ec2: 1024 SHA256:gooHNyf3s2ICFX0v6oEbT8PvLjzA/76BaMDGxpr3HkQ root@ubuntu-bionic (DSA)
    Nov 29 06:09:14 ubuntu-bionic ec2: 256 SHA256:NKhdA817D0+vBWOpXS7R8zEgn1qslxwxMWKtjcZD1eQ root@ubuntu-bionic (ECDSA)
    Nov 29 06:09:14 ubuntu-bionic ec2: 256 SHA256:6ZnAE12MifYiPKDUERsr5/oTnE04XBsgGq3PNe7GOqY root@ubuntu-bionic (ED25519)
    Nov 29 06:09:14 ubuntu-bionic ec2: 2048 SHA256:mhAYpzYqwD56A4dSW12SoDClJlRIV2LAFqdci7Im+FI root@ubuntu-bionic (RSA)
    Nov 29 06:09:14 ubuntu-bionic ec2: -----END SSH HOST KEY FINGERPRINTS-----
    Nov 29 06:09:14 ubuntu-bionic ec2: #############################################################
    Nov 29 06:09:14 ubuntu-bionic cloud-init[1410]: Cloud-init v. 18.4-0ubuntu1~18.04.1 running 'modules:final' at Thu, 29 Nov 2018 06:09:14 +0000. Up 21.79 seconds.
    Nov 29 06:09:14 ubuntu-bionic cloud-init[1410]: ci-info: no authorized ssh keys fingerprints found for user ubuntu.
    Nov 29 06:09:14 ubuntu-bionic cloud-init[1410]: Cloud-init v. 18.4-0ubuntu1~18.04.1 finished at Thu, 29 Nov 2018 06:09:14 +0000. Datasource DataSourceNoCloud [seed=/dev/sdb][dsmode=net].  Up 22.01 seconds
    Nov 29 06:09:14 ubuntu-bionic systemd[1]: Started Execute cloud user/final scripts.
    Nov 29 06:09:14 ubuntu-bionic systemd[1]: Reached target Cloud-init target.
    Nov 29 06:09:14 ubuntu-bionic systemd[1]: Startup finished in 7.899s (kernel) + 14.232s (userspace) = 22.132s.
    Nov 29 06:09:17 ubuntu-bionic systemd[1]: Stopping User Manager for UID 1000...
    Nov 29 06:09:17 ubuntu-bionic systemd[1228]: Stopped target Default.
    Nov 29 06:09:17 ubuntu-bionic systemd[1228]: Stopped target Basic System.
    Nov 29 06:09:17 ubuntu-bionic systemd[1228]: Stopped target Sockets.
    Nov 29 06:09:17 ubuntu-bionic systemd[1228]: Closed GnuPG network certificate management daemon.
    Nov 29 06:09:17 ubuntu-bionic systemd[1228]: Closed GnuPG cryptographic agent (ssh-agent emulation).
    Nov 29 06:09:17 ubuntu-bionic systemd[1228]: Closed GnuPG cryptographic agent and passphrase cache (access for web browsers).
    Nov 29 06:09:17 ubuntu-bionic systemd[1228]: Closed GnuPG cryptographic agent and passphrase cache.
    Nov 29 06:09:17 ubuntu-bionic systemd[1228]: Stopped target Timers.
    Nov 29 06:09:17 ubuntu-bionic systemd[1228]: Stopped target Paths.
    Nov 29 06:09:17 ubuntu-bionic systemd[1228]: Closed GnuPG cryptographic agent and passphrase cache (restricted).
    Nov 29 06:09:17 ubuntu-bionic systemd[1228]: Reached target Shutdown.
    Nov 29 06:09:17 ubuntu-bionic systemd[1228]: Starting Exit the Session...
    Nov 29 06:09:17 ubuntu-bionic systemd[1228]: Received SIGRTMIN+24 from PID 1627 (kill).
    Nov 29 06:09:17 ubuntu-bionic systemd[1]: Stopped User Manager for UID 1000.
    Nov 29 06:09:17 ubuntu-bionic systemd[1]: Removed slice User Slice of vagrant.
    Nov 29 06:09:17 ubuntu-bionic systemd[1]: Created slice User Slice of vagrant.
    Nov 29 06:09:17 ubuntu-bionic systemd[1]: Starting User Manager for UID 1000...
    Nov 29 06:09:17 ubuntu-bionic systemd[1]: Started Session 3 of user vagrant.
    Nov 29 06:09:17 ubuntu-bionic systemd[1630]: Listening on GnuPG cryptographic agent and passphrase cache (restricted).
    Nov 29 06:09:17 ubuntu-bionic systemd[1630]: Listening on GnuPG cryptographic agent and passphrase cache.
    Nov 29 06:09:17 ubuntu-bionic systemd[1630]: Reached target Paths.
    Nov 29 06:09:17 ubuntu-bionic systemd[1630]: Listening on GnuPG cryptographic agent and passphrase cache (access for web browsers).
    Nov 29 06:09:17 ubuntu-bionic systemd[1630]: Listening on GnuPG cryptographic agent (ssh-agent emulation).
    Nov 29 06:09:17 ubuntu-bionic systemd[1630]: Listening on GnuPG network certificate management daemon.
    Nov 29 06:09:17 ubuntu-bionic systemd[1630]: Reached target Sockets.
    Nov 29 06:09:17 ubuntu-bionic systemd[1630]: Reached target Timers.
    Nov 29 06:09:17 ubuntu-bionic systemd[1630]: Reached target Basic System.
    Nov 29 06:09:17 ubuntu-bionic systemd[1630]: Reached target Default.
    Nov 29 06:09:17 ubuntu-bionic systemd[1630]: Startup finished in 40ms.
    Nov 29 06:09:17 ubuntu-bionic systemd[1]: Started User Manager for UID 1000.
    Nov 29 06:09:21 ubuntu-bionic systemd-resolved[639]: Server returned error NXDOMAIN, mitigating potential DNS violation DVE-2018-0001, retrying transaction with reduced feature level UDP.
    Nov 29 06:10:54 ubuntu-bionic systemd-resolved[639]: Server returned error NXDOMAIN, mitigating potential DNS violation DVE-2018-0001, retrying transaction with reduced feature level UDP.
    Nov 29 06:12:12 ubuntu-bionic systemd[1]: Stopping User Manager for UID 1000...
    Nov 29 06:12:12 ubuntu-bionic systemd[1630]: Stopped target Default.
    Nov 29 06:12:12 ubuntu-bionic systemd[1630]: Stopped target Basic System.
    Nov 29 06:12:12 ubuntu-bionic systemd[1630]: Stopped target Paths.
    Nov 29 06:12:12 ubuntu-bionic systemd[1630]: Stopped target Timers.
    Nov 29 06:12:12 ubuntu-bionic systemd[1630]: Stopped target Sockets.
    Nov 29 06:12:12 ubuntu-bionic systemd[1630]: Closed GnuPG cryptographic agent and passphrase cache.
    Nov 29 06:12:12 ubuntu-bionic systemd[1630]: Closed GnuPG network certificate management daemon.
    Nov 29 06:12:12 ubuntu-bionic systemd[1630]: Closed GnuPG cryptographic agent and passphrase cache (access for web browsers).
    Nov 29 06:12:12 ubuntu-bionic systemd[1630]: Closed GnuPG cryptographic agent and passphrase cache (restricted).
    Nov 29 06:12:12 ubuntu-bionic systemd[1630]: Closed GnuPG cryptographic agent (ssh-agent emulation).
    Nov 29 06:12:12 ubuntu-bionic systemd[1630]: Reached target Shutdown.
    Nov 29 06:12:12 ubuntu-bionic systemd[1630]: Starting Exit the Session...
    Nov 29 06:12:12 ubuntu-bionic systemd[1630]: Received SIGRTMIN+24 from PID 3866 (kill).
    Nov 29 06:12:12 ubuntu-bionic systemd[1]: Stopped User Manager for UID 1000.
    Nov 29 06:12:12 ubuntu-bionic systemd[1]: Removed slice User Slice of vagrant.
    Nov 29 06:13:48 ubuntu-bionic systemd[1]: Created slice User Slice of vagrant.
    Nov 29 06:13:48 ubuntu-bionic systemd[1]: Starting User Manager for UID 1000...
    Nov 29 06:13:48 ubuntu-bionic systemd[1]: Started Session 5 of user vagrant.
    Nov 29 06:13:48 ubuntu-bionic systemd[3869]: Listening on GnuPG cryptographic agent and passphrase cache (access for web browsers).
    Nov 29 06:13:48 ubuntu-bionic systemd[3869]: Listening on GnuPG cryptographic agent and passphrase cache (restricted).
    Nov 29 06:13:48 ubuntu-bionic systemd[3869]: Reached target Paths.
    Nov 29 06:13:48 ubuntu-bionic systemd[3869]: Listening on GnuPG cryptographic agent (ssh-agent emulation).
    Nov 29 06:13:48 ubuntu-bionic systemd[3869]: Listening on GnuPG cryptographic agent and passphrase cache.
    Nov 29 06:13:48 ubuntu-bionic systemd[3869]: Reached target Timers.
    Nov 29 06:13:48 ubuntu-bionic systemd[3869]: Listening on GnuPG network certificate management daemon.
    Nov 29 06:13:48 ubuntu-bionic systemd[3869]: Reached target Sockets.
    Nov 29 06:13:48 ubuntu-bionic systemd[3869]: Reached target Basic System.
    Nov 29 06:13:48 ubuntu-bionic systemd[3869]: Reached target Default.
    Nov 29 06:13:48 ubuntu-bionic systemd[3869]: Startup finished in 44ms.
    Nov 29 06:13:48 ubuntu-bionic systemd[1]: Started User Manager for UID 1000.
    Nov 29 06:15:03 ubuntu-bionic systemd[1]: Stopping User Manager for UID 1000...
    Nov 29 06:15:03 ubuntu-bionic systemd[3869]: Stopped target Default.
    Nov 29 06:15:03 ubuntu-bionic systemd[3869]: Stopped target Basic System.
    Nov 29 06:15:03 ubuntu-bionic systemd[3869]: Stopped target Paths.
    Nov 29 06:15:03 ubuntu-bionic systemd[3869]: Stopped target Sockets.
    Nov 29 06:15:03 ubuntu-bionic systemd[3869]: Closed GnuPG cryptographic agent and passphrase cache.
    Nov 29 06:15:03 ubuntu-bionic systemd[3869]: Closed GnuPG cryptographic agent and passphrase cache (restricted).
    Nov 29 06:15:03 ubuntu-bionic systemd[3869]: Closed GnuPG network certificate management daemon.
    Nov 29 06:15:03 ubuntu-bionic systemd[3869]: Closed GnuPG cryptographic agent (ssh-agent emulation).
    Nov 29 06:15:03 ubuntu-bionic systemd[3869]: Closed GnuPG cryptographic agent and passphrase cache (access for web browsers).
    Nov 29 06:15:03 ubuntu-bionic systemd[3869]: Reached target Shutdown.
    Nov 29 06:15:03 ubuntu-bionic systemd[3869]: Starting Exit the Session...
    Nov 29 06:15:03 ubuntu-bionic systemd[3869]: Stopped target Timers.
    Nov 29 06:15:03 ubuntu-bionic systemd[3869]: Started Exit the Session.
    Nov 29 06:15:03 ubuntu-bionic systemd[3869]: Received SIGRTMIN+24 from PID 3978 (n/a).
    """)

SHORT_CONTENT = dedent("""\
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] e820: BIOS-provided physical RAM map:
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] BIOS-e820: [mem 0x0000000000000000-0x000000000009fbff] usable
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] BIOS-e820: [mem 0x000000000009fc00-0x000000000009ffff] reserved
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] BIOS-e820: [mem 0x00000000000f0000-0x00000000000fffff] reserved
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] BIOS-e820: [mem 0x0000000000100000-0x000000007ffeffff] usable
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] BIOS-e820: [mem 0x000000007fff0000-0x000000007fffffff] ACPI data
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] BIOS-e820: [mem 0x00000000fec00000-0x00000000fec00fff] reserved
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] BIOS-e820: [mem 0x00000000fee00000-0x00000000fee00fff] reserved
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] BIOS-e820: [mem 0x00000000fffc0000-0x00000000ffffffff] reserved
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] NX (Execute Disable) protection: active
    Nov 29 06:09:07 ubuntu-bionic kernel: [    0.000000] SMBIOS 2.5 present.
    """)

CONFIG = dedent("""\
    ---
    logs:
     - path:    {tmpdir}/syslog
     - path:    {tmpdir}/kernlog
     - path:    {tmpdir}/periodic-1.log
     - path:    {tmpdir}/periodic-2.log
     - path:    {tmpdir}/missing.log
    """)

class DynamicFileWriter(Thread):
    '''Write to files that should show activity'''


    KEEP_WRITING = True


    def __init__(self, path, min_wait, max_wait, content):
        self.path = path

        # Convert frequencies to 1/60 second
        self.min_wait = int(min_wait * 60)
        self.max_wait = int(max_wait * 60)

        self.content = content

        super().__init__(daemon=True)


    def run(self):

        # Write to output folder
        while True:
            for line in self.content.split("\n"):

                # Check for kill code
                if not DynamicFileWriter.KEEP_WRITING:
                    return

                # Output line
                with open(self.path, 'at') as fh:
                    fh.write(line + "\n")

                # Wait
                wait_60ths = randint(self.min_wait, self.max_wait)
                sleep(float(wait_60ths) / 60.0)





if __name__ == '__main__':

    project = os.path.abspath(os.path.dirname(__file__))
    tempdir = os.path.join(project, 'testfiles')

    if os.path.exists(tempdir):
        print("rm -rf " + tempdir)
        shutil.rmtree(tempdir)
    os.mkdir(tempdir)

    config_path = os.path.join(tempdir, 'devlogs.yml')
    writers = list()

    try:

        # Create config file
        with open(config_path, 'wt') as fh:
            fh.write(CONFIG.format(tmpdir=tempdir))

        # Create files to look at
        logs = [
            (os.path.join(tempdir, 'syslog'), LONG_CONTENT),
            (os.path.join(tempdir, 'kernlog'), SHORT_CONTENT),
            (os.path.join(tempdir, 'periodic-1.log'), ''),
            (os.path.join(tempdir, 'periodic-2.log'), ''),
        ]
        for path, content in logs:
            with open(path, 'wt') as fh:
                fh.write(content)

        # Start threads to write to files that get updated
        writers.append(DynamicFileWriter(os.path.join(tempdir, 'periodic-1.log'), 0.5, 2, LONG_CONTENT))
        writers.append(DynamicFileWriter(os.path.join(tempdir, 'periodic-2.log'), 3, 10, SHORT_CONTENT))
        for w in writers:
            w.start()

        # Start server
        main(('--path', config_path, 'run', '--project_assets'))

    finally:

        # Stop writing threads
        DynamicFileWriter.KEEP_WRITING = False
        for t in writers:
            t.join()

        # Cleanup files
        if os.path.exists(config_path):
            os.unlink(config_path)
        for path, content in logs:
            if os.path.exists(path):
                os.unlink(path)

        os.unlink(tempdir)

