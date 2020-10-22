# from escpos.printer import Usb
#
# """ Seiko Epson Corp. Receipt Printer (EPSON TM-T88III) """
# p = Usb(0x04b8, 0x0202, 0, profile="TM-T88III")
# p.text("Hello World\n")
# p.image("logo.gif")
# p.barcode('1324354657687', 'EAN13', 64, 2, '', '')
# p.cut()


# https://pypi.org/project/PyESCPOS/#dummy-print-example
from escpos import DummyConnection
from escpos.impl.epson import GenericESCPOS

conn = DummyConnection()
printer = GenericESCPOS(conn)
printer.init()
printer.text('Hello World!')
print(printer.device.output)
