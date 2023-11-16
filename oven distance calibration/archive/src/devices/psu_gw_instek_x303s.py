"""
    Copyright 2022 Continental Corporation

    :file: psu_gw_instek_x303s.py
    :platform: Windows
    :synopsis:
        Class for implementation of PSU GW Instek GPD x303s Series utilities

    :author:
        - Ganga Prabhakar G <ganga.prabhakar.guntamukkala@continental-corporation.com>
"""

import logging
import time
import re

# custom import
from ptf.verify_utils import ptf_asserts

LOG = logging.getLogger('GW INSTEK')


class GwInstekGPDX303S:
    """
    Class for ``GW INSTEK`` GPD-X303S series power supplies.
    """
    # set value tolerance
    TOLERANCE = 0.05

    # flag for maximum number of tries for sending command to PSU
    # introduced because PSU sends some garbage data after several hrs. runtime
    MAXIMUM_QUERY_ATTEMPTS = 3

    # Maximum Voltage limit for the GW INSTEK GDP-X303S models.
    # It is defined here as there are no commands to read or set the limits.
    MAX_VOLT = 30

    # Regular expression to read a value from device
    # e.g. retrieving 12.00 from response string '12.00V\r\n'.
    VALUE_REGEX = r"[.\d]+"

    VOLT_SET_RETRY_COUNT = 15

    def __init__(self, **kwargs):
        """
        Initialization for `GW INSTEK`` GPD x303s Series power supplies.

        :param kwargs: User inputs and power supply specific information passed as keyword
            arguments from base ``Psu`` class using ``__initialize_subclass`` method.
        """
        # Retrieving necessary parameters from the base class for later usage
        self.__operating_voltage = kwargs['operational_volt']
        self.__operating_current = kwargs['operational_curr']
        self.__commands = kwargs['psu_commands']
        self.__device_connection = kwargs['device_connection']
        self.__init_channel = kwargs['channel']
        if self.__init_channel == 'None' or self.__init_channel == '0':
            ptf_asserts.fail("Channel cannot be 'none' or '0'. Please check your input")
        # defining device type
        self.__device_type = 'GW INSTEK'
        # Stabilizing retry count and wait time used while querying output voltage or
        # current during setting
        self.__stable_retry_count = GwInstekGPDX303S.VOLT_SET_RETRY_COUNT
        # 50ms is minimum response time based on the information from x303S manual
        self.__stable_wait_time = 0.05

        # Stores if we are in startup phase or not. Startup phase flag is used to set
        # voltage/current before first time enabling of power supply output.
        # This will prevent any issues/damages to the connected setup due to earlier unknown
        # voltage or current settings
        self.__startup_phase = True

        # setting operational voltage provided to ECU
        self.set_operating_voltage(volt_value=self.__operating_voltage, channel=self.__init_channel,
                                   tolerance=self.TOLERANCE)
        # setting operational current only if it is not None.
        if self.__operating_current:
            self.set_operating_current(curr_value=self.__operating_current,
                                       channel=self.__init_channel, tolerance=self.TOLERANCE)
        self.__startup_phase = False

    @staticmethod
    def __verify_value(actual_value, exp_value, tolerance):
        """
        Method for verifying a value set on PSU

        :param float actual_value: Value received from PSU
        :param float exp_value: Expected value in response
        :param float tolerance: Tolerance for the expected value
        """
        # checking if the actual set value on PSU is within tolerance
        ptf_asserts.verify_with_tol(actual_value, exp_value, tolerance,
                                    'Value {} exceeds expected tolerance to expected value {}'
                                    .format(actual_value, exp_value))

    def __query_psu(self, function, value=None, resp_required=False):
        """
        Method for requesting PSU via RS-232 and read back PSU response if required

        .. note:: Due to some weird behaviour of PSU after several hrs run a retry mechanism is
            added. If a failure is detected then the command will be sent again (max. 3 times). Even
            then the error does not go away then a PSU reset will be required.

        :param str function: PSU supported function
        :param value: Value to be passed via cmd
        :type value: float, int
        :param bool resp_required: Flag if response is required

        :returns: Response (Function, Value) if required else None
        :rtype: tuple, None
        """
        for query_attempts in range(GwInstekGPDX303S.MAXIMUM_QUERY_ATTEMPTS):
            try:
                if resp_required:
                    # Additional check for 0 is added for not missing the request of 0.0
                    if value or value == 0:
                        return self.__device_connection.query(function, [value])

                    return self.__device_connection.query(function)

                # Additional check for 0 is added for not missing the request of 0.0
                if value or value == 0:
                    self.__device_connection.write_ascii_values(function, [value])
                else:
                    self.__device_connection.write(function)

                # Break after the first successful write
                break

            # pylint: disable=broad-except
            # ignoring pylint issue as it will capture all exceptions which will help in capturing
            # un-known exceptions raised by device
            except Exception as error:
                if query_attempts < GwInstekGPDX303S.MAXIMUM_QUERY_ATTEMPTS:
                    LOG.warning("Error occurred in sending command : %s\n"
                                "Error: %s\nTrying again ...", function, error)
                else:
                    LOG.error("Maximum attempts (%s) done for '%s' command. "
                              "Please reset PSU.", query_attempts, function)
                    ptf_asserts.fail(str(error))
                LOG.debug("Attempt : %s for Command : %s", query_attempts + 1, function)
        return None  # to make pylint happy

    def __verify_stabilized_voltage(self, **kwargs):
        """
        This internal method waits certain time for the output voltage to stabilize with
        multiple query attempts

        :param kwargs: user input volt value and tolerance in keyword arguments
        """
        read_value = None
        self.__stable_retry_count = GwInstekGPDX303S.VOLT_SET_RETRY_COUNT
        while self.__stable_retry_count != 0:
            # check measured voltage in-case it's not startup phase
            read_value = self.get_output_voltage(channel=kwargs['channel'])
            try:
                self.__verify_value(read_value, kwargs['volt_value'], kwargs['tolerance'])
                LOG.info("Operational Voltage set to '%f' V", kwargs['volt_value'])
                break
            except ptf_asserts.PtfAssertCompareError:
                time.sleep(self.__stable_wait_time)
                LOG.info("Voltage value isn't set to the expected value. Retrying...")
                self.__stable_retry_count = self.__stable_retry_count - 1
        return read_value

    def set_operating_current(self, **kwargs):
        """
        Method for setting current value on PSU and verifying it

        :param kwargs: Channel number, Current value and tolerance(+/-) to be set on PSU.
            Default tolerance '0.05' will be used, if no value is given.
        """
        LOG.debug('Setting Current Value of channel no.%s', str(kwargs['channel']))
        # Framing the device command using json string and input value. For e.g. "ISET1:5"
        device_command = \
            self.__commands[self.__device_type]["SET_GET_CURR"] + str(kwargs['channel']) + ':' \
                                                                + str(kwargs['curr_value'])
        self.__query_psu(device_command)
        # checking set current is matching with the queried value.
        read_value = self.get_set_current(channel=kwargs['channel'])

        self.__verify_value(read_value, kwargs['curr_value'], kwargs['tolerance'])
        LOG.info("Operational Current set to '%f' A", kwargs['curr_value'])

    def set_operating_voltage(self, **kwargs):
        """
        Method for setting voltage value on PSU and verifying it

        :param kwargs: Channel number, Voltage value and tolerance(+/-) to be set on PSU.
            Default tolerance '0.05' will be used, if no value is given.
        """
        LOG.debug('Setting Voltage Value of channel no.%s', str(kwargs['channel']))
        # Verifying the input volt value is not greater than the voltage limit of power supply.
        ptf_asserts.verify_gt_eq(GwInstekGPDX303S.MAX_VOLT, kwargs['volt_value'],
                                 'Voltage value {} is greater than voltage limit value {}'
                                 .format(kwargs['volt_value'], GwInstekGPDX303S.MAX_VOLT))
        # Framing the device command using json string and input value. For e.g. "VSET1:12"
        device_command = \
            self.__commands[self.__device_type]["SET_GET_VOLT"] + str(kwargs['channel']) + ':' \
                                                                + str(kwargs['volt_value'])
        self.__query_psu(device_command)
        # checking if it's startup phase
        if self.__startup_phase:
            # check set voltage in-case it's startup phase
            read_value = self.get_set_voltage(channel=kwargs['channel'])
        else:
            read_value = self.__verify_stabilized_voltage(volt_value=kwargs['volt_value'],
                                                          channel=kwargs['channel'],
                                                          tolerance=kwargs['tolerance'])
        ptf_asserts.verify_with_tol(read_value, kwargs['volt_value'], kwargs['tolerance'],
                                    'Output voltage {} is not set to expected value {} even after '
                                    'multiple tries'.format(read_value, kwargs['volt_value']))
        LOG.info("Operating voltage of '%s' is set to '%f' V", self.__device_type, read_value)

    def get_set_voltage(self, **kwargs):
        """
        Method for reading back set voltage value

        :param kwargs: Channel number in a keyword argument

        :returns: Set voltage value of requested channel in float
        :rtype: float
        """
        LOG.debug('Querying the Set Voltage Value from channel no.%s', str(kwargs['channel']))
        # Framing the device command using json string and input value.
        device_command = \
            self.__commands[self.__device_type]["SET_GET_VOLT"] + str(kwargs['channel']) + '?'
        response = self.__query_psu(device_command, resp_required=True)
        # Retrieving only the float value from response.
        # e.g. retrieving 12.00 from response string '12.00V\r\n'.
        voltage = float(re.findall(GwInstekGPDX303S.VALUE_REGEX, response)[0])
        # throw back value in response
        return voltage

    def get_set_current(self, **kwargs):
        """
        Method for reading back set current value

        :param kwargs: Keyword argument holding channel number

        :returns: Set current value of requested channel in float
        :rtype: float
        """
        LOG.debug('Querying the Set Current Value from channel no.%s', str(kwargs['channel']))
        # Framing the device command using json string and input value.
        device_command = \
            self.__commands[self.__device_type]["SET_GET_CURR"] + str(kwargs['channel']) + '?'
        response = self.__query_psu(device_command, resp_required=True)
        # Retrieving only the float value from response.
        # e.g. retrieving 2.00 from response string '2.00A\r\n'.
        current = float(re.findall(GwInstekGPDX303S.VALUE_REGEX, response)[0])
        # throw back value in response
        return current

    def get_output_voltage(self, **kwargs):
        """
        Method for reading back output voltage value

        :param kwargs: Keyword argument holding channel number

        :returns: Output voltage value of requested channel in float
        :rtype: float
        """
        LOG.debug('Querying the Output Voltage Value from channel no.%s', str(kwargs['channel']))
        # Framing the device command using json string and input value.
        device_command = \
            self.__commands[self.__device_type]["GET_MEASURED_VOLT"] + str(kwargs['channel']) + '?'
        response = self.__query_psu(device_command, resp_required=True)
        # Retrieving only the float value from response.
        # e.g. retrieving 12.00 from response string '12.00V\r\n'.
        voltage = float(re.findall(GwInstekGPDX303S.VALUE_REGEX, response)[0])
        # throw back value in response
        return voltage

    def get_output_current(self, **kwargs):
        """
        Method for reading back output current value

        :param kwargs: Keyword argument holding channel number

        :returns: Output current value of requested channel in float
        :rtype: float
        """
        LOG.debug('Querying the Output Current Value from channel no.%s', str(kwargs['channel']))
        # Framing the device command using json string and input value.
        device_command = \
            self.__commands[self.__device_type]["GET_MEASURED_CURR"] + str(kwargs['channel']) + '?'
        response = self.__query_psu(device_command, resp_required=True)
        # Retrieving only the float value from response.
        # e.g. retrieving 2.00 from response string '12.00A\r\n'.
        current = float(re.findall(GwInstekGPDX303S.VALUE_REGEX, response)[0])
        # throw back value in response
        return current

    @staticmethod
    def get_voltage_limit():
        """
        Method for fetching voltage limit value set on PSU

        .. note::
            GW Instek x303S does not have voltage limit getting function. This method stays
            dummy in this class as the methods are derived based on the base class ``Psu``.
            Hence a Log warning is printed for user information.
        """
        LOG.warning('Querying the Voltage Limit is not possible for GW INSTEK x303S power '
                    'supply series')

    @staticmethod
    def get_current_limit():
        """
        Method for fetching current limit value set on PSU

        .. note::
            GW Instek x303S does not have current limit getting function. This method stays
            dummy in this class as the methods are derived based on the base class ``Psu``.
            Hence a Log warning is printed for user information.
        """
        LOG.warning('Querying the Current Limit is not possible for GW INSTEK '
                    'x303S power supply series')

    # pylint: disable=unused-argument
    def enable_output(self, **kwargs):
        """
        Method for enabling PSU output

        :param kwargs: No arguments needed for this power supply to disable output.

        .. note::
            All the public methods in this class are derived based on the base class ``Psu`` and
            only Psu class is exposed to user. Reason behind kwargs is to allow user to input
            channel number, which is necessary for channel based power supplies. e.g. Siglent.
            As the GW INSTEK series does not need a channel input for this API, kwargs are not used.
        """
        LOG.debug('Enabling Output...')
        self.__query_psu(self.__commands[self.__device_type]["SET_OUTPUT_ON"])
        response = self.__query_psu(self.__commands[self.__device_type]["GET_OUTPUT_STATE"],
                                    resp_required=True)
        # There is no specific query output status in GW INSTEK x303S power supply series.
        # Possible to query only full status of power supply having Channel mode,
        # output status, baud rate, etc
        # re to get the output status (5th bit) out of 8 bits of power supply status. e.g.
        # '11010110\r\n'
        output_stat = re.findall(GwInstekGPDX303S.VALUE_REGEX, response)[0][5:-2]
        ptf_asserts.verify(output_stat, self.__commands[self.__device_type]["IS_OUTPUT_ON"],
                           'PSU output is not enabled ...')
        LOG.info('PSU output enabled ...')

    # pylint: disable=unused-argument
    def disable_output(self, **kwargs):
        """
        Method for disabling PSU output

        :param kwargs: No arguments needed for this power supply to disable output.

        .. note::
            All the public methods in this class are derived based on the base class ``Psu`` and
            only Psu class is exposed to user. Reason behind kwargs is to allow user to input
            channel number, which is necessary for channel based power supplies. e.g. Siglent.
            As the GW INSTEK series does not need a channel input for this API, kwargs are not used.
        """
        LOG.debug('Disable Output')
        self.__query_psu(self.__commands[self.__device_type]["SET_OUTPUT_OFF"])
        response = self.__query_psu(self.__commands[self.__device_type]["GET_OUTPUT_STATE"],
                                    resp_required=True)
        # There is no specific query output status in GW INSTEK x303S power supply series.
        # Possible to query only full status of power supply having Channel mode,
        # output status, baud rate, etc
        # re to get the output status (5th bit) out of 8 bits of power supply status. e.g.
        # '11010110\r\n'
        output_stat = re.findall(GwInstekGPDX303S.VALUE_REGEX, response)[0][5:-2]
        ptf_asserts.verify(output_stat, self.__commands[self.__device_type]["IS_OUTPUT_OFF"],
                           'PSU output is not disabled ...')
        LOG.info('PSU output disabled ...')

    # pylint: disable=unused-argument
    @staticmethod
    def set_voltage_limit(**kwargs):
        """
        Method for setting voltage limit value and verify it. To avoid setting voltage above it.

        :param kwargs: No arguments as this power supply doesn't support this function.

        .. note::
            GW Instek x303S does not have voltage limit setting function. This method stays
            dummy in this class as the methods are derived based on the base class ``Psu``.
            Hence a Log warning is printed for user information.
        """
        LOG.warning('Setting the Voltage Limit is not possible for GW INSTEK '
                    'x303S power supply series')

    # pylint: disable=unused-argument
    @staticmethod
    def set_current_limit(**kwargs):
        """
        Method for setting current limit value and verify it. To avoid setting current above it.

        :param kwargs: No arguments as this power supply doesn't support this function.

        .. note::
            GW Instek x303S does not have current limit setting function. This method stays
            dummy in this class as the methods are derived based on the base class ``Psu``.
            Hence a Log warning is printed for user information.
        """
        LOG.warning('Setting the Current Limit is not possible for GW INSTEK '
                    'x303S power supply series')

    def close(self):
        """ Method for disabling PSU output and closing PSU connected COM port """
        # close PSU port after disabling output if PSU port was detected
        if self.__device_connection:
            LOG.info('Disabling PSU power output')
            self.disable_output()
            LOG.info('Closing %s port', self.__device_connection)
            self.__device_connection.close()

    # pylint: disable=unused-argument
    @staticmethod
    def get_psu_status(**kwargs):
        """
        This method will read the current status of power supply.

        .. note::
            GW Instek x303S series does not have power supply status reading function. This method stays
            dummy in this class as the methods are derived based on the base class ``Psu``.
            Hence a Log warning is printed for user information.
        """
        LOG.warning('Getting the power supply status is not possible for GW Instek x303S power '
                    'supply series')
