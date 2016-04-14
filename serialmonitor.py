#!/usr/bin/python
# coding=utf-8

from serial import Serial
from serial import SerialException
import serial.tools.list_ports as tools
from read import ler_serial
import time


def get_porta():
    lista_portas = tools.comports()

    count = lista_portas.__len__()

    if count == 0:
        print 'Não há portas seriais disponíveis'
        return False

    print 'Selecione uma porta serial'
    print '=========================='
    print ''

    index = 0
    for porta_serial in lista_portas:
        texto_opcao = str(index) + ' - ' + porta_serial.device
        if porta_serial.description != 'n/a':
            texto_opcao += ' (' + porta_serial.description.strip() + ')'
        print texto_opcao
        index += 1
    print str(index) + ' - Sair'
    print ''

    opcao = raw_input('> ')

    if int(opcao) < count:
        return lista_portas[int(opcao)].device
    else:
        return False


def get_baud_rate():
    itens = ['110', '300', '600', '1200', '2400', '4800', '9600', '14400', '19200', '28800', '38400', '56000', '57600', '115200']

    print 'Selecione baud rate'
    print '==================='
    print ''

    index = 0
    for item in itens:
        print str(index) + ' - ' + item
        index += 1
    print str(index) + ' - Sair'
    print ''

    opcao = raw_input('> ')

    if int(opcao) < len(itens):
        return itens[int(opcao)]
    else:
        return False


def show_help(porta_serial, baud_rate):
    print ''
    print 'Porta "' + porta_serial + '" aberta a ' + baud_rate + 'bps'
    print ''
    print 'Encerrar: exit()'
    print ''
    print 'Carecteres especiais'
    print '       LF (Line Feed): <L>'
    print ' CR (Carriage Return): <C>'
    print '              LF + CR: <LC>'
    print '             Ctrl + Z: <CZ>'


if __name__ == "__main__":
    porta = get_porta()
    if not porta:
        exit()

    baud = get_baud_rate()
    if not baud:
        exit()

    serial = None
    try:
        serial = Serial(port=porta, baudrate=baud)
    except SerialException as E:
        print 'Não foi possível abrir a porta serial'
        print str(E)
        exit()

    show_help(porta, baud)

    ler = ler_serial(serial)
    ler.start()

    """
    a = ['0054', '0075', '0064', '006F', '0020', '0062', '0065', '006D', '0020', '0070', '006F', '0072', '0020', '0061', '00ED', '003F']
    b = ''
    for i in a:
        b += chr(int(i, 16))
    print b
    """

    while True:
        cmd = raw_input('')

        if cmd == 'exit()':
            ler.active = False
            exit()

        if '<L>' in cmd:
            cmd = cmd.replace('<L>', '\r')

        if '<C>' in cmd:
            cmd = cmd.replace('<C>', '\n')

        if '<LC>' in cmd:
            cmd = cmd.replace('<LC>', '\r\n')

        if '<CZ>' in cmd:
            cmd = cmd.replace('<CZ>', chr(26))

        serial.write(cmd)
