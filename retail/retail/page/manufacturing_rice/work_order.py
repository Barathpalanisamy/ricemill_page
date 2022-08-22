import frappe
from erpnext.manufacturing.doctype.work_order.work_order import make_job_card
from frappe.utils import flt
from erpnext.manufacturing.doctype.work_order.work_order import make_stock_entry

@frappe.whitelist()
def work_order_creation(a,b, c):
    qty=int(a)
    doc=frappe.new_doc("Work Order")
    doc.update({
                'doctype':'Work Order',
                'production_item':c,
                'bom_no':b,
                'qty':qty,
                "fg_warehouse":"Finished Goods - R",
                "wip_warehouse":"Stores - R"
            })
    doc.get_items_and_operations_from_bom()
    doc.save(ignore_permissions=True)
    doc.submit()
    frappe.errprint(doc.name)
    stock=make_stock_entry(work_order_id=doc.name,purpose="Material Transfer for Manufacture",qty= 1)
    stock.save
