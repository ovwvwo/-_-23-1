#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def decimal_to_binary(ip_address):
    """
    Преобразует IP-адрес из десятичного формата в двоичный.
    
    Аргументы:
        ip_address (str): IP-адрес в десятичном формате (например, "192.168.1.1")
    
    Возвращает:
        str: IP-адрес в двоичном формате (например, "11000000.10101000.00000001.00000001")
    """
    # Разделяем IP-адрес на октеты
    octets = ip_address.split(".")
    
    # Проверяем, что IP-адрес состоит из 4 октетов
    if len(octets) != 4:
        return "Ошибка: IP-адрес должен содержать 4 октета, разделенных точкой."
    
    binary_octets = []
    for octet in octets:
        try:
            # Проверяем, что октет является числом от 0 до 255
            decimal_octet = int(octet)
            if decimal_octet < 0 or decimal_octet > 255:
                return f"Ошибка: Каждый октет должен быть числом от 0 до 255. Получено: {octet}"
            
            # Преобразуем десятичное число в двоичное и удаляем префикс '0b'
            binary_octet = bin(decimal_octet)[2:]
            
            # Дополняем нулями слева до 8 бит
            binary_octet = binary_octet.zfill(8)
            
            binary_octets.append(binary_octet)
        except ValueError:
            return f"Ошибка: Невозможно преобразовать '{octet}' в число."
    
    # Объединяем октеты с помощью точки
    return ".".join(binary_octets)

def binary_to_decimal(ip_address):
    """
    Преобразует IP-адрес из двоичного формата в десятичный.
    
    Аргументы:
        ip_address (str): IP-адрес в двоичном формате (например, "11000000.10101000.00000001.00000001")
    
    Возвращает:
        str: IP-адрес в десятичном формате (например, "192.168.1.1")
    """
    # Разделяем IP-адрес на октеты
    octets = ip_address.split(".")
    
    # Проверяем, что IP-адрес состоит из 4 октетов
    if len(octets) != 4:
        return "Ошибка: IP-адрес должен содержать 4 октета, разделенных точкой."
    
    decimal_octets = []
    for octet in octets:
        # Проверяем, что октет содержит только 0 и 1 и имеет длину 8
        if not all(bit in '01' for bit in octet) or len(octet) != 8:
            return f"Ошибка: Каждый двоичный октет должен содержать ровно 8 бит (0 или 1). Получено: {octet}"
        
        # Преобразуем двоичное число в десятичное
        decimal_octet = int(octet, 2)
        decimal_octets.append(str(decimal_octet))
    
    # Объединяем октеты с помощью точки
    return ".".join(decimal_octets)

def validate_ip_format(ip_address):
    """
    Определяет формат введенного IP-адреса (десятичный или двоичный).
    
    Аргументы:
        ip_address (str): IP-адрес в любом формате
    
    Возвращает:
        str: "decimal", "binary" или "invalid"
    """
    octets = ip_address.split(".")
    
    # Проверяем, что IP-адрес состоит из 4 октетов
    if len(octets) != 4:
        return "invalid"
    
    # Проверяем формат
    is_decimal = True
    is_binary = True
    
    for octet in octets:
        # Проверка для десятичного формата
        try:
            decimal_value = int(octet)
            if decimal_value < 0 or decimal_value > 255:
                is_decimal = False
        except ValueError:
            is_decimal = False
        
        # Проверка для двоичного формата
        if not all(bit in '01' for bit in octet) or len(octet) != 8:
            is_binary = False
    
    if is_decimal:
        return "decimal"
    elif is_binary:
        return "binary"
    else:
        return "invalid"

def main():
    """
    Основная функция программы, обрабатывающая ввод пользователя.
    """
    print("=" * 60)
    print("Программа для конвертации IP-адресов")
    print("=" * 60)
    print("Введите IP-адрес в десятичном формате (например, 192.168.1.1)")
    print("или в двоичном формате (например, 11000000.10101000.00000001.00000001)")
    
    while True:
        user_input = input("\nВведите IP-адрес (или 'выход' для завершения): ")
        
        if user_input.lower() in ['выход', 'exit', 'quit', 'q']:
            print("Программа завершена.")
            break
        
        # Определяем формат введенного IP-адреса
        ip_format = validate_ip_format(user_input)
        
        if ip_format == "decimal":
            # Если формат десятичный, преобразуем в двоичный
            binary_ip = decimal_to_binary(user_input)
            print(f"\nДесятичная запись: {user_input}")
            print(f"Двоичная запись:   {binary_ip}")
        
        elif ip_format == "binary":
            # Если формат двоичный, преобразуем в десятичный
            decimal_ip = binary_to_decimal(user_input)
            print(f"\nДвоичная запись:   {user_input}")
            print(f"Десятичная запись: {decimal_ip}")
        
        else:
            print("Ошибка: Введенный IP-адрес имеет неверный формат.")
            print("IP-адрес должен содержать 4 октета, разделенных точкой.")
            print("Для десятичного формата: каждый октет должен быть числом от 0 до 255.")
            print("Для двоичного формата: каждый октет должен содержать 8 бит (0 или 1).")

# Проверим работу программы на примерах из задания №1
def verify_examples():
    print("\n" + "=" * 60)
    print("Проверка примеров из задания №1")
    print("=" * 60)
    
    # Двоичные IP-адреса из задания
    binary_ips = [
        "01011101.10111011.01001000.00110000",
        "01001000.10100011.00000100.10100001",
        "00001111.11011001.11101000.11110101"
    ]
    
    for i, binary_ip in enumerate(binary_ips, 1):
        decimal_ip = binary_to_decimal(binary_ip)
        print(f"{i}) Двоичная запись:   {binary_ip}")
        print(f"   Десятичная запись: {decimal_ip}\n")
    
    # Десятичные IP-адреса из задания
    decimal_ips = [
        "65.58.20.252",
        "154.246.184.244"
    ]
    
    for i, decimal_ip in enumerate(decimal_ips, 4):
        binary_ip = decimal_to_binary(decimal_ip)
        print(f"{i}) Десятичная запись: {decimal_ip}")
        print(f"   Двоичная запись:   {binary_ip}\n")

if __name__ == "__main__":
    # Запуск проверки примеров
    verify_examples()
    # Запуск основной программы
    main()
