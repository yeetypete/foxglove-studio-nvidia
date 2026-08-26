# foxglove-studio-nvidia

NVDEC hardware video decode for Foxglove Studio (Electron/Chromium) on Linux
with an NVIDIA GPU, via
[nvidia-vaapi-driver](https://github.com/elFarto/nvidia-vaapi-driver).

## Why this is needed

- Chromium blocklists VA-API on NVIDIA unless the `VaapiOnNvidiaGPUs` feature
  is enabled.
- Foxglove's main process calls
  `app.commandLine.appendSwitch("enable-features", ...)`, which **replaces**
  any `--enable-features` you pass on the command line. So the only way to
  enable it is to patch the string inside `/opt/Foxglove/resources/app.asar`.
  See `patch-asar.py`.

## Requirements

- [nvidia-vaapi-driver](https://github.com/elFarto/nvidia-vaapi-driver) built
  from git master (tested at commit
  [03bb5a0](https://github.com/elFarto/nvidia-vaapi-driver/commit/03bb5a0),
  2026-07-17). The NVIDIA GPU must be set as your display render device.
- `LIBVA_DRIVER_NAME=nvidia vainfo --display drm --device /dev/dri/renderD128`
  should list H264/HEVC/VP9/AV1 profiles.

## Installation

```bash
make install
make uninstall
```

> [!IMPORTANT]
> You must re-run `make install` after every Foxglove Studio upgrade.

## Verification

Play an H.264/H.265 topic and check that NVDEC is busy:

```bash
nvidia-smi dmon -s u   # "dec" column should show values > 0
```

> [!NOTE]
> The "GPU feature status" list in Foxglove's Performance tab is not reliable.
> It can report "Not hardware accelerated" while real streams run on NVDEC.

## Common issues

- **Hybrid laptops decode on the iGPU.** On laptops with an iGPU you must
  explicitly switch to discrete graphics in the BIOS
  (e.g. ThinkPad: Config > Display > Graphics Device > Discrete Graphics). Note
  that your battery life may suffer.

Tested with: Foxglove 3.0.0 (Electron 43 / Chromium 150), nvidia-vaapi-driver
git 03bb5a0, NVIDIA 610.43.02 open kernel module, RTX 5090,
Ubuntu 26.04 LTS, sway 1.11 (Wayland).
