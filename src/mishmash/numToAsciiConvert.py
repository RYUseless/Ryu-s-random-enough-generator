# Funkce pro výpočet velkého čísla
def compute_large_number():
    base = 874741608
    exponent1 = 1504175 % 1612
    modulus1 = 174073
    exponent2 = 1612

    # Výpočet velkého čísla
    result = (base ** exponent1) % (modulus1 ** exponent2)
    return result


# Funkce pro rozdělení čísla na 128 sekcí
def split_number(number, sections=128):
    number_str = str(number)

    # Pokud je číslo kratší než počet sekcí, nepřidáváme nuly, ale rozdělíme jen dostupné číslice
    section_length = max(1, len(number_str) // sections)
    sections_list = [int(number_str[i:i + section_length]) for i in range(0, len(number_str), section_length)]

    return sections_list


# Funkce pro převod sekcí na ASCII znaky (rozsah 32 až 126)
def sections_to_ascii(sections_list):
    ascii_str = ''
    for section in sections_list:
        ascii_char = chr(32 + (section % 95))  # 95 je počet tisknutelných znaků v ASCII (od 32 do 126)
        ascii_str += ascii_char
    return ascii_str.strip()  # Odstranění počátečních a koncových mezer


# Hlavní funkce
def generate_random_ascii_string():
    result = compute_large_number()
    sections_list = split_number(result)
    ascii_string = sections_to_ascii(sections_list)
    return ascii_string


# Výpis výsledku
random_ascii_string = generate_random_ascii_string()
print(random_ascii_string)
print(len(random_ascii_string.encode("utf-8")))


