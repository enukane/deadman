import rtmidi

class Launchpad :
    ROW_MAX=8
    COLUMN_MAX=8
    HEAD_MAPS=[0x51, 0x47, 0x3d, 0x33, 0x29, 0x1f, 0x15, 0x0b]

    COLOR_GREEN="green"
    COLOR_YELLOWGREEN="yellowgreen"
    COLOR_YELLOW="yellow"
    COLOR_RED="red"
    COLOR_BLACK="black"
    COLOR_WHITE="white"

    def __init__ (self) :
        self.is_port_opened = False
        self.midi_out = rtmidi.MidiOut()
        available_ports = self.midi_out.get_ports()

        if available_ports:
            self.midi_out.open_port(0)
            self.is_port_opened = True
        else:
            self.is_port_opened = False

        self.pad_maps = [[0 for i in range(self.ROW_MAX)] for j in range(self.COLUMN_MAX)]
        for idx in range(self.ROW_MAX):
            for i in range(self.COLUMN_MAX):
                self.pad_maps[idx][i] = self.HEAD_MAPS[idx] + i

    def get_led_addr(self, idx):
        row = int(idx / self.ROW_MAX)
        column = idx % self.COLUMN_MAX
        return self.pad_maps[row][column]

    def get_color_code(self, color) :
        if color == self.COLOR_GREEN :
            return 25
        elif color == self.COLOR_YELLOWGREEN :
            return 17
        elif color == self.COLOR_YELLOW :
            return 13
        elif color == self.COLOR_RED :
            return 5
        elif color == self.COLOR_BLACK :
            return 0
        elif color == self.COLOR_WHITE :
            return 3
        else:
            return 3

    def set_color(self, num, color) :
        if self.is_port_opened == False :
            return
        led_addr = self.get_led_addr(num)
        color_code = self.get_color_code(color)

        sysex = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x18, 0x0a, led_addr, color_code, 0xf7]

        self.midi_out.send_message(sysex)

    def clear_color(self) :
        for i in range(64) :
            self.set_color(i, self.COLOR_BLACK)
