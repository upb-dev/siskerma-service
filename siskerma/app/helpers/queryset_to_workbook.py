import datetime
from io import BytesIO

import xlsxwriter
from django.core.exceptions import ObjectDoesNotExist
from django.forms.utils import pretty_name

HEADER_SYTLE = {'bold': True}
DEFAULT_STYLE = {'bold': False}
CELL_STYLE_MAP = (
    (datetime.datetime, {'set_num_format': "YYYY/MM/DD HH:MM"}),
    (datetime.date, {'set_num_format': 'DD/MM/YYYY'}),
    (datetime.time, {'set_num_format': "HH:MM"}),
    (bool, {'set_num_format': "BOOLEAN"}),
)


def multi_getattr(obj, attr, default=None):
    attributes = attr.split(".")

    for i in attributes:
        try:
            if obj._meta.get_field(i).choices:
                obj = getattr(obj, f"get_{i}_display")()
            else:
                obj = getattr(obj, i)
        except AttributeError:
            if default:
                return default
            else:
                raise

    return obj


def get_column_head(obj, name):
    names = name.split(".")

    tmp = ''

    for i in names:
        tmp += obj._meta.get_field(i).verbose_name
        tmp += '.'

    return pretty_name(tmp)


def get_column_cell(obj, name):
    try:
        attr = multi_getattr(obj, name)
    except ObjectDoesNotExist:
        return None

    if hasattr(attr, '_meta'):
        return str(attr).strip()
    elif hasattr(attr, 'all'):
        return ', '.join(str(x).strip() for x in attr.all())

    if isinstance(attr, datetime.datetime):
        from django.utils.timezone import localtime
        attr = localtime(attr)
        attr = attr.replace(tzinfo=None)

    return attr


def queryset_to_workbook(queryset,
                         columns,
                         header_style=HEADER_SYTLE,
                         default_style=DEFAULT_STYLE,
                         cell_style_map=CELL_STYLE_MAP):
    virtual = BytesIO()
    workbook = xlsxwriter.Workbook(virtual)
    report_date = datetime.date.today()
    sheet_name = f"Export {report_date.strftime('%Y-%m-%d')}"
    sheet = workbook.add_worksheet(sheet_name)

    obj = queryset.first()

    for num, column in enumerate(columns):
        value = get_column_head(obj, column)
        sheet.write(0, num, value, workbook.add_format(header_style))

    for x, obj in enumerate(queryset, start=1):
        for y, column in enumerate(columns):
            value = get_column_cell(obj, column)
            style = workbook.add_format(default_style)

            for value_type, cell_style in cell_style_map:
                if isinstance(value, value_type):
                    style = workbook.add_format(cell_style)

                    break
            sheet.write(x, y, value, style)
    workbook.close()
    virtual.seek(0)

    return virtual
