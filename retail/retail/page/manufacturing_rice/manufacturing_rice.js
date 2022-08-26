frappe.pages["manufacturing-rice"].on_page_load = function (wrapper) {
  var page = frappe.ui.make_app_page({
    parent: wrapper,
    title: "Rice Mill Manufacturing",
    single_column: true,
  });
  new erpnext.Ricemill(page);
};
var me;
erpnext.Ricemill = class Ricemill {
  constructor(page) {
    this.page = page;
    me = this;
    this.make_form();
  }
  make_form() {
    this.form = new frappe.ui.FieldGroup({
      fields: [
        {
          label: "Item To Manufacture",
          fieldtype: "Link",
          fieldname: "item_to_manufacture",
          options: "Item",
          change: () =>
            frappe.call({
              method: "retail.retail.page.manufacturing_rice.ricemill.setup",
              args: {
                ricemill: this.form.get_value("item_to_manufacture"),
              },
              callback: function (r) {
                this.form.get_field("html1").html(r.message);
              }.bind(this),
            }),
        },
        {
          fieldtype: "Column Break",
        },
        {
          label: "Work Order",
          fieldname: "work_order",
          fieldtype: "Link",
          options: "Work Order",
          change: () => frappe.call({
            method: "retail.retail.page.manufacturing_rice.ricemill.function",
            args: {workorder:this.form.get_value("work_order"),},
            callback(r) {
              me.form.get_field("html1").html(r.message);
            },
            })

        },

        {
          fieldtype: "Section Break",
        },
        {
          fieldname: "html1",
          fieldtype: "HTML",
        },
       
      ],

      body: this.page.body,
    });
    this.form.make();
  }
};

function myFunction(ricemill) {
  var a = document.getElementById("qty").value;
  var b = document.getElementById("bom_name").value;
  if (a && b) {
    frappe.call({
      method:
        "retail.retail.page.manufacturing_rice.work_order.work_order_creation",
      args: { a: a, b: b, c: ricemill },
	  callback(r){
        me.form.get_field("work_order").set_value(r.message)
	  }
    });
  }
}



function finish(){
  frappe.call({
    method:"retail.retail.page.manufacturing_rice.ricemill.fields_list",
    args: {workorder:this.form.get_value("work_order"),},
     callback(r){
        me.form.get_field("work_order").set_value("")
        me.form.get_field("item_to_manufacture").set_value("")
	  }


  })
}