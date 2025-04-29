#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def validate_ip(ip_address):
    """
    Проверяет корректность IP-адреса.
    
    Аргументы:
        ip_address (str): IP-адрес для проверки
    
    Возвращает:
        bool: True, если IP-адрес корректный, иначе False
    """
    # Разделяем IP-адрес на октеты
    octets = ip_address.split(".")
    
    # Проверяем, что IP-адрес состоит из 4 октетов
    if len(octets) != 4:
        return False
    
    # Проверяем, что каждый октет является числом от 0 до 255
    for octet in octets:
        try:
            value = int(octet)
            if value < 0 or value > 255:
                return False
        except ValueError:
            return False
    
    return True

def determine_ip_class(ip_address):
    """
    Определяет класс IP-адреса.
    
    Аргументы:
        ip_address (str): IP-адрес
    
    Возвращает:
        tuple: (класс сети, префикс маски подсети по умолчанию)
    """
    # Получаем первый октет
    first_octet = int(ip_address.split(".")[0])
    
    # Определяем класс IP-адреса
    if 1 <= first_octet <= 126:  # 0XXXXXXX - 0XXXXXXX
        return "A", 8
    elif 128 <= first_octet <= 191:  # 10XXXXXX - 10XXXXXX
        return "B", 16
    elif 192 <= first_octet <= 223:  # 110XXXXX - 110XXXXX
        return "C", 24
    elif 224 <= first_octet <= 239:  # 1110XXXX - 1110XXXX
        return "D", 0  # Для мультивещательных адресов не применяется стандартная маска
    elif 240 <= first_octet <= 255:  # 1111XXXX - 1111XXXX
        return "E", 0  # Для экспериментальных адресов не применяется стандартная маска
    elif first_octet == 127:
        return "Loopback", 8
    else:
        return "Неизвестный", 0

def get_subnet_mask(prefix):
    """
    Возвращает маску подсети в десятичном формате на основе префикса.
    
    Аргументы:
        prefix (int): Длина префикса (например, 24 для /24)
    
    Возвращает:
        str: Маска подсети в десятичном формате (например, 255.255.255.0)
    """
    # Создаем маску подсети в двоичном виде
    binary_mask = "1" * prefix + "0" * (32 - prefix)
    
    # Разбиваем двоичную маску на октеты
    octets = [binary_mask[i:i+8] for i in range(0, 32, 8)]
    
    # Конвертируем каждый октет в десятичное число
    decimal_octets = [str(int(octet, 2)) for octet in octets]
    
    # Объединяем октеты с помощью точки
    return ".".join(decimal_octets)

def get_network_range(ip_address, prefix):
    """
    Вычисляет начальный и конечный адрес подсети.
    
    Аргументы:
        ip_address (str): IP-адрес
        prefix (int): Длина префикса
    
    Возвращает:
        tuple: (начальный адрес, конечный адрес)
    """
    # Разделяем IP-адрес на октеты и конвертируем в целые числа
    octets = [int(octet) for octet in ip_address.split(".")]
    
    # Конвертируем IP в 32-битное целое число
    ip_int = (octets[0] << 24) + (octets[1] << 16) + (octets[2] << 8) + octets[3]
    
    # Создаем маску подсети как целое число
    mask_int = (2**32 - 1) - (2**(32 - prefix) - 1)
    
    # Вычисляем начальный адрес сети (IP AND MASK)
    network_int = ip_int & mask_int
    
    # Вычисляем конечный адрес сети (NETWORK OR NOT MASK)
    broadcast_int = network_int | (2**(32 - prefix) - 1)
    
    # Конвертируем начальный адрес обратно в точечно-десятичную нотацию
    network_octets = [
        (network_int >> 24) & 255,
        (network_int >> 16) & 255,
        (network_int >> 8) & 255,
        network_int & 255
    ]
    network_address = ".".join(map(str, network_octets))
    
    # Конвертируем конечный адрес обратно в точечно-десятичную нотацию
    broadcast_octets = [
        (broadcast_int >> 24) & 255,
        (broadcast_int >> 16) & 255,
        (broadcast_int >> 8) & 255,
        broadcast_int & 255
    ]
    broadcast_address = ".".join(map(str, broadcast_octets))
    
    return network_address, broadcast_address

def analyze_ip(ip_address):
    """
    Анализирует IP-адрес и возвращает информацию о нем.
    
    Аргументы:
        ip_address (str): IP-адрес для анализа
    
    Возвращает:
        dict: Информация о сети
    """
    if not validate_ip(ip_address):
        return {"error": "Неверный формат IP-адреса"}
    
    # Определяем класс IP-адреса и стандартный префикс для этого класса
    ip_class, default_prefix = determine_ip_class(ip_address)
    
    # Если класс D или E, не применяем стандартную маску
    if ip_class in ["D", "E", "Неизвестный"]:
        result = {
            "ip_address": ip_address,
            "ip_class": ip_class,
            "note": f"Для IP-адресов класса {ip_class} не применяется стандартная маска подсети"
        }
        return result
    
    # Получаем маску подсети
    subnet_mask = get_subnet_mask(default_prefix)
    
    # Получаем начальный и конечный адрес сети
    network_address, broadcast_address = get_network_range(ip_address, default_prefix)
    
    # Количество хостов в сети
    num_hosts = 2**(32 - default_prefix) - 2
    
    # Формируем результат
    result = {
        "ip_address": ip_address,
        "ip_class": ip_class,
        "network_prefix": default_prefix,
        "subnet_mask": subnet_mask,
        "network_address": network_address,
        "broadcast_address": broadcast_address,
        "usable_hosts": num_hosts
    }
    
    return result

def display_ip_info(ip_info):
    """
    Выводит информацию об IP-адресе на экран.
    
    Аргументы:
        ip_info (dict): Информация о сети
    """
    print("\n" + "=" * 60)
    
    if "error" in ip_info:
        print(f"Ошибка: {ip_info['error']}")
        return
    
    if "note" in ip_info:
        print(f"IP-адрес: {ip_info['ip_address']}")
        print(f"Класс IP: {ip_info['ip_class']}")
        print(f"Примечание: {ip_info['note']}")
        return
    
    print(f"IP-адрес:              {ip_info['ip_address']}")
    print(f"Класс IP:              {ip_info['ip_class']}")
    print(f"Префикс сети:          /{ip_info['network_prefix']}")
    print(f"Маска подсети:         {ip_info['subnet_mask']}")
    print(f"Начальный адрес сети:  {ip_info['network_address']}")
    print(f"Конечный адрес сети:   {ip_info['broadcast_address']}")
    print(f"Количество хостов:     {ip_info['usable_hosts']}")
    
    print("=" * 60)

def explain_ip_classes():
    """
    Выводит информацию о классах IP-адресов.
    """
    print("\n" + "-" * 60)
    print("Информация о классах IP-адресов:")
    print("-" * 60)
    print("Класс A: 1.0.0.0 - 126.255.255.255")
    print("         Маска подсети: 255.0.0.0 (префикс /8)")
    print("         Первый бит: 0")
    print("         Для крупных сетей (~16.7 млн хостов)")
    print()
    print("Класс B: 128.0.0.0 - 191.255.255.255")
    print("         Маска подсети: 255.255.0.0 (префикс /16)")
    print("         Первые два бита: 10")
    print("         Для средних сетей (~65,5 тыс. хостов)")
    print()
    print("Класс C: 192.0.0.0 - 223.255.255.255")
    print("         Маска подсети: 255.255.255.0 (префикс /24)")
    print("         Первые три бита: 110")
    print("         Для малых сетей (254 хоста)")
    print()
    print("Класс D: 224.0.0.0 - 239.255.255.255")
    print("         Первые четыре бита: 1110")
    print("         Для групповой адресации (мультикаст)")
    print()
    print("Класс E: 240.0.0.0 - 255.255.255.255")
    print("         Первые четыре бита: 1111")
    print("         Зарезервированы для экспериментальных целей")
    print()
    print("Адреса 127.0.0.0 - 127.255.255.255 зарезервированы для локальной обратной связи")
    print("-" * 60)

def main():
    """
    Основная функция программы.
    """
    print("=" * 60)
    print("Анализатор IP-адресов")
    print("=" * 60)
    print("Программа определяет класс сети, начальный и конечный адрес сети,")
    print("а также маску подсети на основании заданного IP-адреса")
    
    # Выводим информацию о классах IP-адресов
    explain_ip_classes()
    
    # Примеры IP-адресов для демонстрации работы программы
    example_ips = [
        "10.0.0.1",       # Класс A
        "172.16.0.1",     # Класс B
        "192.168.1.1",    # Класс C
        "224.0.0.1",      # Класс D (мультикаст)
        "240.0.0.1",      # Класс E (экспериментальный)
        "127.0.0.1"       # Loopback
    ]
    
    print("\n" + "=" * 60)
    print("Демонстрация работы программы на примерах")
    print("=" * 60)
    
    for example_ip in example_ips:
        ip_info = analyze_ip(example_ip)
        display_ip_info(ip_info)
    
    # Интерактивный режим
    while True:
        print("\nВведите IP-адрес для анализа (или 'выход' для завершения):")
        user_input = input("> ")
        
        if user_input.lower() in ['выход', 'exit', 'quit', 'q']:
            print("\nПрограмма завершена.")
            break
        
        # Анализируем введенный IP-адрес
        ip_info = analyze_ip(user_input)
        display_ip_info(ip_info)

if __name__ == "__main__":
    main()
