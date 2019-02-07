import subprocess

WHITELIST = (
    # Anything with super is OK
    'Super',
    # Leave VERY basic window and menu keys
    '<Alt>Tab',
    '<Shift><Alt>Tab',
    '<Alt>F4',
    '<Alt>Space'
)


def main():
    result = subprocess.run(['gsettings', 'list-keys', 'org.gnome.desktop.wm.keybindings'],
                            capture_output=True, universal_newlines=True)
    for keybindings_key in result.stdout.split('\n'):
        if not keybindings_key:
            continue
        result = subprocess.run(['gsettings', 'get', 'org.gnome.desktop.wm.keybindings', keybindings_key],
                                capture_output=True, universal_newlines=True)

        if result.stdout.startswith('@as '):
            default = True
            keybindings = eval(result.stdout[3:])
        else:
            default = False
            keybindings = eval(result.stdout)

        if keybindings:
            print(f"{keybindings_key} {keybindings}")
            for keybind in keybindings[:]:
                for ok in WHITELIST:
                    if ok in keybind:
                        break
                else:
                    keybindings.remove(keybind)
                    print(f'.. removed {keybind}')

            # set keybindings
            result = subprocess.run(['gsettings', 'set', 'org.gnome.desktop.wm.keybindings',
                                     keybindings_key, str(keybindings)],
                                    capture_output=True, universal_newlines=True)

        # default flag is set so maybe we need to remove that and set empty to get rid of
        # potential crap
        if default and not keybindings:
            result = subprocess.run(['gsettings', 'set', 'org.gnome.desktop.wm.keybindings',
                                     keybindings_key, '[]'],
                                    capture_output=True, universal_newlines=True)


if __name__ == "__main__":
    main()
