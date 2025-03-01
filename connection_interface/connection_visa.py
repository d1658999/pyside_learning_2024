import time

import pyvisa

from utils.log_init import log_set
from utils.parameters.external_paramters import tcpip

logger = log_set('Visa')


class VisaComport:
    def __init__(self, equipment_name):
        self.inst = None
        self.begin_visa(equipment_name)

    def begin_visa(self, equipment_name):
        if equipment_name in ['CMW100', 'Cmw100', 'cmw100']:
            try:
                self.inst = pyvisa.ResourceManager().open_resource('TCPIP0::127.0.0.1::INSTR')

            except Exception as err:
                logger.info(err)
                logger.info('Please check if connecting to CMW100 or the comport is occupied')

            else:
                logger.info('Connect to CMW100')
                logger.info('TCPIP0::127.0.0.1::INSTR')

            self.inst.timeout = 10000  # set the default timeout

        elif '8820' in equipment_name or '8821' in equipment_name:
            gpib_wanted = None
            for gpib in self.get_gpib_usb():  # this is to search GPIB for 8820/8821
                inst = pyvisa.ResourceManager().open_resource(gpib)
                inst_res = inst.query('*IDN?').strip()
                if '8820' in inst_res or '8821' in inst_res:
                    gpib_wanted = gpib
                    break

            self.inst = pyvisa.ResourceManager().open_resource(gpib_wanted)  # to build object of 'inst'
            logger.info(f"Connect to {self.inst.query('*IDN?').strip()}")

            self.inst.timeout = 5000  # set the default timeout

        elif equipment_name in ['psu', 'PSU']:
            psu_list = ['E3631A', 'E3642A', 'E36313A']
            psu_select = None
            try:
                gpib_usb_wanted = None
                for gpib_usb in self.get_gpib_usb():  # this is to search GPIB for PSU
                    inst = pyvisa.ResourceManager().open_resource(gpib_usb)
                    print(inst)
                    inst_res = inst.query('*IDN?').strip()
                    logger.info('----------Search PSU we are using----------')
                    for psu in psu_list:
                        if psu in inst_res:
                            gpib_usb_wanted = gpib_usb
                            psu_select = psu
                            break

                    if psu_select is not None:
                        break

            except Exception as err:
                logger.info(err)
                logger.info('Please check if connecting to PSU')

            else:
                logger.info(f'Connect to {psu_select} successfully')
                self.inst = pyvisa.ResourceManager().open_resource(gpib_usb_wanted)  # to build object of 'inst'

            self.inst.timeout = 5000  # set the default timeout

        elif equipment_name == 'temp_chamber':
            gpib_wanted = None
            try:
                for gpib in self.get_gpib_usb():  # this is to search GPIB for tempchamber
                    inst = pyvisa.ResourceManager().open_resource(gpib)
                    inst_res = inst.query('*IDN?').strip()
                    logger.info('----------Search temp chamber we are using----------')
                    if 'NA:CMD_ERR' in inst_res:
                        gpib_wanted = gpib
                        break

            except Exception as err:
                logger.info(err)
                logger.info('Please check if connecting to temp_chamber')

            else:
                logger.info(f'Connect to temp_chamber successfully')
                self.inst = pyvisa.ResourceManager().open_resource(gpib_wanted)  # to build object of 'inst'

            self.inst.timeout = 5000  # set the default timeout

        elif 'FSW' in equipment_name or 'fsw' in equipment_name:
            try:
                gpib_usb_wanted = None
                for gpib_usb in self.get_gpib_usb():  # this is to search GPIB for FSW
                    inst = pyvisa.ResourceManager().open_resource(gpib_usb)
                    inst_res = inst.query('*IDN?').strip()
                    logger.info('----------Search FSW we are using----------')
                    if 'FSW' in inst_res or 'fsw' in inst_res:
                        gpib_usb_wanted = gpib_usb
                        break

            except Exception as err:
                logger.info(err)
                logger.info('Please check if connecting to FSW')

            else:
                logger.info(f'Connect to FSW successfully')
                self.inst = pyvisa.ResourceManager().open_resource(gpib_usb_wanted)  # to build object of 'inst'

            self.inst.timeout = 75000  # set the default timeout

        elif 'E7515B' in equipment_name:
            port = 5025
            resource = f'TCPIP0::{tcpip}::{port}::SOCKET'
            try:
                inst = pyvisa.ResourceManager().open_resource(resource)
                inst.read_termination = '\n'
                inst.write_termination = '\n'
                inst_res = inst.query('*IDN?').strip()
                logger.info('----------Get UXM we are using----------')
                logger.info(inst_res)

            except Exception as err:
                logger.info(err)
                logger.info('Please check if connecting to UXM')

            else:
                logger.info(f'Connect to UXM successfully')
                self.inst = inst  # to build object of 'inst'

            self.inst.timeout = 5000  # set the default timeout
        # elif 'E7515B' in equipment_name:
        #     try:
        #         resource = self.get_gpib_tcpip()  # this is to search tcpip by visa
        #         inst = pyvisa.ResourceManager().open_resource(resource)
        #         inst_res = inst.query('*IDN?').strip()
        #         logger.info('----------Get UXM we are using----------')
        #         logger.info(inst_res)
        #
        #     except Exception as err:
        #         logger.info(err)
        #         logger.info('Please check if connecting to UXM')
        #
        #     else:
        #         logger.info(f'Connect to UXM successfully')
        #         self.inst = pyvisa.ResourceManager().open_resource(resource)  # to build object of 'inst'
        #
        #     self.inst.timeout = 5000  # set the default timeout

    @staticmethod
    def get_gpib_usb():
        resources = []
        print(pyvisa.ResourceManager().list_resources())
        for resource in pyvisa.ResourceManager().list_resources():
            if 'GPIB' in resource or 'USB' in resource:
                resources.append(resource)
                logger.debug(resource)
        return resources

    @staticmethod
    def get_gpib_tcpip():
        for resource in pyvisa.ResourceManager().list_resources():
            if tcpip in resource:
                logger.info(resource)

                return resource

    def write(self, command):
        self.inst.write(command)

    def query(self, command):
        return self.inst.query(command)

    def query_2(self, command):
        return self.inst.query_binary_values(command, datatype='B', container=bytes)

    def close(self):
        self.inst.close()


def main():
    test = VisaComport('E7515B')
    # print(test.query('*IDN?'))
    # print(test.query('SYSTem:BASE:OPTion:VERSion? "CMW_NRSub6G_Meas"'))
    # t = "CMW_NRSub6G_Meas"
    # tt = f'SYSTem:BASE:OPTion:VERSion? {t}'
    # test.query(tt)


if __name__ == '__main__':
    main()