frappe.pages["operation-status"].on_page_load = function (wrapper) {
  var page = frappe.ui.make_app_page({
    parent: wrapper,
    title: "Operation status",
    single_column: true,
  });
  new erpnext.OPERATION_STATUS(page);
};
erpnext.OPERATION_STATUS = class OPERATION_STATUS {
  constructor(page) {
    this.page = page;
    this.make_form();
  }
  make_form() {
    this.form = new frappe.ui.FieldGroup({
      fields: [
        {
          label: "Work Order",
          fieldtype: "Link",
          fieldname: "id",
          options: "Work Order",
		  change : () => frappe.call(
			{
			  method:"retail.retail.page.operation_status.operation.setup",
			  args:{
				work_order:this.form.get_value("id")
			  },
			  callback: function(r){
				this.form.get_field('html1').html(r.message)
			  }.bind(this)
			}
		  )
        },

        {
          
          fieldtype: "Section Break",
        },
		{
			fieldname:"html1",
			fieldtype: "HTML",
		},
		{
			fieldname:"html2",
			fieldtype: "HTML",
			
		},

      ],
      body: this.page.body,
    });
    this.form.make();
  }
};
