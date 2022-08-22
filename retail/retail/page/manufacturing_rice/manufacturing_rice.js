frappe.pages['manufacturing-rice'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Rice Mill Manufacturing',
		single_column: true
	});
new erpnext.Ricemill(page);
};
erpnext.Ricemill = class Ricemill {
constructor(page) {
  this.page = page;
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
		change : () => frappe.call(
		  {
			method:"retail.retail.page.manufacturing_rice.ricemill.setup",
			args:{
			  ricemill:this.form.get_value("item_to_manufacture")
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
