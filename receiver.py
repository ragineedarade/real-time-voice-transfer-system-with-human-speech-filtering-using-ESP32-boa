import machine
import ubluetooth
import ustruct


class BTService:
    def __init__(self):
        self.bt = ubluetooth.BLE()
        self.bt.active(True)
        self.bt.irq(handler=self.bt_irq)
        self.conn_handle = None
        self.bt.gap_scan(0)

    def bt_irq(self, event, data):
        if event == 1:  # Central connected
            self.conn_handle, _, _ = data
            print('Connected')
        elif event == 2:  # Central disconnected
            self.conn_handle = None
            print('Disconnected')
        elif event == 5:  # Scan result
            addr_type, addr, adv_type, rssi, adv_data = data
            if b'\xAB\xCD' in adv_data:
                self.bt.gap_scan(None)
                self.bt.gap_connect(addr_type, addr)
        elif event == 7:  # New data received
            conn_handle, attr_handle, value = data
            audio_data = ustruct.unpack('h', value)[0]
            self.play_audio(audio_data)

    def play_audio(self, data):
        dac.write(data)


bt_service = BTService()

dac = machine.DAC(machine.Pin(25))

while True:
    pass  # Main loop does nothing, all work is done in IRQ
