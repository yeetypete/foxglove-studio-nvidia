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

- `nvidia-vaapi-driver` (Ubuntu: `apt install nvidia-vaapi-driver`). The
  NVIDIA GPU must be set as your display render device.
- `LIBVA_DRIVER_NAME=nvidia vainfo --display drm --device /dev/dri/renderD128`
  should list H264/HEVC/VP9/AV1 profiles.

## Install

```bash
make install
make uninstall
```

> [!IMPORTANT]
> You must re-run `make install` after every Foxglove Studio upgrade.

Tested with: Foxglove 3.0.0 (Electron 43 / Chromium 150), nvidia-vaapi-driver
0.0.14, NVIDIA 610.43.02 open kernel module, RTX 5090, Ubuntu 26.04 LTS,
sway 1.11 (Wayland).
