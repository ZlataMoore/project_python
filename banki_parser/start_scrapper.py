import jinja2
from project_python.banki_parser.bs4_parser import read


def get_banks(price, initial_fee, is_have_child_before_2018, purpose_type, max_payment: int):
    banks = []

    for bank in read(price, initial_fee, is_have_child_before_2018, purpose_type):
        if bank['payment_per_mouth'] <= max_payment:
            banks.append(bank)

    banks.sort(key=lambda x: (x['period'], x['payment_per_mouth'], x['overpayment'], x['bank']))
    with open("banks.html", encoding="UTF-8") as f:
        template_str = f.read()
    template = jinja2.Environment(loader=jinja2.FileSystemLoader("../map_of_flats")).from_string(template_str)
    html_str = template.render(banks=banks)

    return html_str


if __name__ == '__main__':
    print(get_banks(5_000_000, 2_000_000, 1, 'new', 20_000))
