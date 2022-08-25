import frappe
from erpnext.manufacturing.doctype.work_order.work_order import make_job_card
from frappe.utils import flt
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
    make_stock_entry(work_order_id=doc.name,purpose="Material Transfer for Manufacture",qty= 1)
    return doc.name



@frappe.whitelist()
def make_stock_entry(work_order_id, purpose, qty=None):
    work_order = frappe.get_doc("Work Order", work_order_id)
    if not frappe.db.get_value("Warehouse", work_order.wip_warehouse, "is_group"):
        wip_warehouse = work_order.wip_warehouse
    else:
        wip_warehouse = None
    stock_entry = frappe.new_doc("Stock Entry")
    stock_entry.purpose = purpose
    stock_entry.work_order = work_order_id
    stock_entry.company = work_order.company
    stock_entry.from_bom = 1
    stock_entry.bom_no = work_order.bom_no
    stock_entry.use_multi_level_bom = work_order.use_multi_level_bom
    # accept 0 qty as well
    stock_entry.fg_completed_qty = (
        qty if qty is not None else (flt(work_order.qty) - flt(work_order.produced_qty))
    )
    if work_order.bom_no:
        stock_entry.inspection_required = frappe.db.get_value(
            "BOM", work_order.bom_no, "inspection_required"
        )
    if purpose == "Material Transfer for Manufacture":
        stock_entry.to_warehouse = wip_warehouse
        stock_entry.project = work_order.project
    else:
        stock_entry.from_warehouse = wip_warehouse
        stock_entry.to_warehouse = work_order.fg_warehouse
        stock_entry.project = work_order.project
    stock_entry.set_stock_entry_type()
    stock_entry.get_items()
    stock_entry.set_serial_no_batch_for_finished_good()
    stock_entry.save()
    stock_entry.submit()
    