import board
import digitalio
import storage

DRIVE_NAME = "CIRCUITPY"

print(f'Boot: renaming drive to {DRIVE_NAME}')
storage.remount("/", readonly=False)
mount = storage.getmount("/")
mount.label = DRIVE_NAME
storage.remount("/", readonly=True)
print(f'Boot: enabling drive')
storage.enable_usb_drive()


