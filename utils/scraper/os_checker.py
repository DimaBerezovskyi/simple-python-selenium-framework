import os
import platform


class OSChecker:
    @staticmethod
    def check_os():
        os_name = os.uname().sysname
        arch = os.uname().machine

        # Check if os_name is "Darwin" and replace it with "mac"
        if os_name == "Darwin":
            os_name = "mac"
        if os_name == "mac":
            return "-".join([os_name, arch])
        else:
            return "".join([os_name, arch])

    def print_os_info(self):
        os_name, arch = self.check_os()
        print(f"Operating System: {os_name}, arch={arch}")

    def _get_driver_type(self=None):
        os_arch_mapping = {
            "arm64": "chrome_arm64",
            "x86_64": "chrome_x86_64",
            "ubuntu": "ubuntu",  # Add additional mappings as needed
        }

        default_driver_type = self
        os_arch = platform.machine()
        os_name = platform.system().lower()

        driver_type = os_arch_mapping.get(os_arch, default_driver_type)
        if os_name in os_arch_mapping:
            driver_type = os_arch_mapping[os_name]

        return driver_type
