import frappe
@frappe.whitelist()
def work_order_creation(a,b):
    qty=int(a)
    frappe.errprint(type(qty))
    doc=frappe.new_doc("Work Order")
    doc.update({
                'doctype':'Work Order',
                'production_item':"Paddy",
                'bom_no':b,
                'qty':qty,
                "fg_warehouse":"Finished Goods - R",
                "wip_warehouse":"Stores - R"
            })
    doc.save(ignore_permissions=True)