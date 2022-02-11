from xml.dom import minidom

# Create schema_id name dicts.
INVOICE_INFO_SECTION_TAGS = {"document_id": "InvoiceNumber", "date_issue": "InvoiceDate", "date_due": "DueDate"}
PAYMENT_INFO_SECTION_TAGS = {"iban": "Iban"}
AMOUNTS_SECTION_TAGS = {"amount_total_tax": "Amount", "currency": "Currency"}
VENDOR_SECTION_TAGS = {"sender_name": "Vendor", "sender_address": "VendorAddress"}

DATAPOINT_TAGS = {"item_quantity": "Quantity", "item_description": "Notes", "item_total_base": "Amount"}


# Find attribute in root by scheme name
def find_by_schema_id(root, name):
    for e in root.childNodes:
        try:
            if e.getAttribute("schema_id") == name:
                return e
        except:
            pass


def reformat_xml(xml_string):
    org = minidom.parseString(xml_string)
    root = minidom.Document()

    # Create base XML structure
    InvoiceRegisters = root.createElement('InvoiceRegisters')
    root.appendChild(InvoiceRegisters)

    Invoices = root.createElement('Invoices')
    InvoiceRegisters.appendChild(Invoices)

    Payable = root.createElement('Payable')
    Invoices.appendChild(Payable)

    content_element = org.getElementsByTagName("content")[0]
    tags = {**INVOICE_INFO_SECTION_TAGS, **PAYMENT_INFO_SECTION_TAGS, **AMOUNTS_SECTION_TAGS, **VENDOR_SECTION_TAGS}

    # Set header tags
    for att_name, tag_name in tags.items():
        el = root.createElement(tag_name)
        Payable.appendChild(el)

        # Find sections, look for attribute in each section
        att_node = find_by_schema_id(find_by_schema_id(content_element, "invoice_info_section"), att_name) or \
                   find_by_schema_id(find_by_schema_id(content_element, "payment_info_section"), att_name) or \
                   find_by_schema_id(find_by_schema_id(content_element, "amounts_section"), att_name) or \
                   find_by_schema_id(find_by_schema_id(content_element, "vendor_section"), att_name)
        try:
            el_value = root.createTextNode(att_node.firstChild.nodeValue)
            el.appendChild(el_value)
        except:
            pass

    details = root.createElement("Details")
    Payable.appendChild(details)

    # Set details tags
    for el in find_by_schema_id(content_element, "line_items_section").getElementsByTagName("tuple"):
        detail = root.createElement("Detail")
        details.appendChild(detail)
        for dp in el.getElementsByTagName("datapoint"):
            try:
                dt_name = dp.getAttribute("schema_id")
                if dt_name in DATAPOINT_TAGS.keys():
                    dt_el = root.createElement(DATAPOINT_TAGS[dt_name])
                    detail.appendChild(dt_el)

                    dt_value = root.createTextNode(dp.firstChild.nodeValue.replace("\n", " "))
                    dt_el.appendChild(dt_value)
            except:
                pass

    xml_str = root.toprettyxml(indent="\t")

    return xml_str

if __name__ == '__main__':
    reformat_xml()