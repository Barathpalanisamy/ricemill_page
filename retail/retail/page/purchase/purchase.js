frappe.pages["purchase"].on_page_load = function (wrapper) {
  var page = frappe.ui.make_app_page({
    parent: wrapper,
    title: "Purchase Invoice",
    single_column: true,
  });

  new erpnext.Purchase_Invoice(page);
};
var column_no,
  checkbox_width = "100px";
var tbl = document.createElement("table");
tbl.id = "tableid";
var tblBody = document.createElement("tbody");
tblBody.id='itemtablebody'

var heading = document.createElement("tr");
if (column_no == null) {
    var cell = document.createElement("th");
	cell.id="th0"
    cell.style.width = checkbox_width;
    let form = document.createElement("form");
    let checkbox = document.createElement("input");
    checkbox.id = "master_check";
    form.appendChild(checkbox);
    checkbox.type = "Checkbox";
    cell.appendChild(checkbox);
    heading.appendChild(cell);
	
    for (let k = 0; k < 15; k++) {
      var cell = document.createElement("th");
	  cell.id='th'+(k+1)
      var cell_heading = document.createTextNode("item" + String(k));
      cell.appendChild(cell_heading);
      heading.appendChild(cell);
    }
    tblBody.appendChild(heading);
	
  }
  tbl.appendChild(tblBody);
  document.body.appendChild(tbl);
  tbl.setAttribute("border", "1");
if(document.getElementById("th0"))
	document.getElementById("th0").addEventListener("click", check_all);
if (document.getElementById("add-row"))
	document.getElementById("add-row").remove();
if (document.getElementById("delete-row"))
	document.getElementById("delete-row").remove();
  button();

erpnext.Purchase_Invoice = class Purchase_Invoice {
  constructor(page) {
    this.page = page;
    this.make_form();
  }
  make_form() {
    var barcode = this;
    var item_list = [];
    this.form = new frappe.ui.FieldGroup({
      fields: [
        {
          label: "Supplier",
          fieldname: "supplier",
          fieldtype: "Link",
          options: "Supplier",
        },
        { fieldtype: "Column Break" },

        {
          label: "Date",
          fieldname: "data",
          fieldtype: "Date",
          default: "Today",
        },

        { fieldtype: "Section Break" },

        {
          label: "Bar Code",
          fieldtype: "Data",
          fieldname: "bar_code",
          options: "Barcode",
          change: () => {
            if (this.form.get_value("bar_code"))
              frappe.call({
                method:
                  "erpnext.selling.page.point_of_sale.point_of_sale.search_for_serial_or_batch_or_barcode_number",
                args: {
                  search_value: this.form.get_value("bar_code"),
                },
                callback: async function (r) {
                  const data = r && r.message;
                  if (!data || Object.keys(data).length === 0) {
                    frappe.show_alert({
                      message: __("Cannot find Item with this Barcode"),
                      indicator: "red",
                    });
                    return;
                  } else {
                    var item_name = [];
                    item_list.push(r.message["item_code"]);

                    await frappe.db
                      .get_doc("Item", r.message["item_code"])
                      .then((res) => {
                        item_name.push(res.item_name);
                        item_name.push(
                          res.purchase_uom ? res.purchase_uom : res.stock_uom
                        );
                      });

                    generateTable(item_name);
                    if (document.getElementById("add-row"))
                      document.getElementById("add-row").remove();
                    if (document.getElementById("delete-row"))
                      document.getElementById("delete-row").remove();
                    button();
                    barcode.form.get_field("bar_code").set_value("");
                  }
                },
              });
          },
        },

        {
          fieldname: "html1",
          fieldtype: "HTML",
          hidden: 1,
          options: `
		<style>
			td, th{
				width: 150px;
			}
		</style>
		`,
        },
      ],

      body: this.page.body,
    });
    this.form.make();
  }
};

function generateTable(item_list) {
  var heading = document.createElement("tr");

//   if (column_no == null) {
//     var cell = document.createElement("th");
// 	cell.id="th0"
//     cell.style.width = checkbox_width;
//     let form = document.createElement("form");
//     let checkbox = document.createElement("input");
//     checkbox.id = "master_check";
//     form.appendChild(checkbox);
//     checkbox.type = "Checkbox";
//     cell.appendChild(checkbox);
//     heading.appendChild(cell);
	
//     for (let k = 0; k < 15; k++) {
//       var cell = document.createElement("th");
// 	  cell.id='th'+(k+1)
//       var cell_heading = document.createTextNode("item" + String(k));
//       cell.appendChild(cell_heading);
//       heading.appendChild(cell);
//     }
//     tblBody.appendChild(heading);
	
//   }

  for (let i = 0; i < 1; i++) {
    column_no = column_no >= 0 ? column_no + 1 : 0;

    var row = document.createElement("tr");
    row.id = "row" + column_no;
    {
      var cell = document.createElement("td");
      var form = document.createElement("form");
      var checkbox = document.createElement("input");
      checkbox.type = "Checkbox";
      checkbox.id = "check" + column_no;
      cell.appendChild(checkbox);
      cell.style.width = checkbox_width;
      row.appendChild(cell);
      for (let j = 0; j < 15; j++) {
        var cell = document.createElement("td");
        var form = document.createElement("form");
        var input = document.createElement("input");
        input.id = "row" + column_no + " col" + j;
        input.value = item_list.length > j ? item_list[j] : "";

        row.appendChild(cell);
        form.appendChild(input);
        cell.appendChild(form);
      }
    }
    tblBody.appendChild(row);
  }
  tbl.appendChild(tblBody);
  document.body.appendChild(tbl);
  tbl.setAttribute("border", "1");
  
}

function button() {
	var button = document.createElement("button");
	var add = document.createTextNode("Add");
	button.setAttribute("id", "add-row");
	button.appendChild(add);
	var button1 = document.createElement("button");
	var deleterow = document.createTextNode("Delete Row");
	button1.setAttribute("id", "delete-row");
	button1.appendChild(deleterow);
	document.body.appendChild(button);
	document.body.appendChild(button1);
	if(document.getElementById("delete-row"))
		document.getElementById("delete-row").addEventListener("click", delete_row);
	if(document.getElementById("add-row"))
		document.getElementById("add-row").addEventListener("click", add_row);
}


function add_row(){
	generateTable([])
	if (document.getElementById("add-row"))
		document.getElementById("add-row").remove();
		if (document.getElementById("delete-row"))
			document.getElementById("delete-row").remove();
		button();
}


function delete_row() {
	let t=document.getElementById('itemtablebody')
	let count = t.childElementCount
	if(count>0){
		for(let i=1; i<count;i++){
			if(($(document.getElementById('itemtablebody').childNodes).length-1)>=i)
			if($(document.getElementById('itemtablebody').childNodes[i].childNodes[0].childNodes[0]).is( ":checked" )){
				document.getElementById('itemtablebody').childNodes[i].remove()
				i-=1;
			}
		}
		
	}
	
	
}


function check_all(){
	let t=document.getElementById('itemtablebody')
	let count = t.childElementCount
	for(let i=0; i<count;i++){
			if($(document.getElementById('master_check')).is( ":checked" )){
				$(document.getElementById('itemtablebody').childNodes[i].childNodes[0].childNodes[0]).prop("checked", true);
			} else{
				$(document.getElementById('itemtablebody').childNodes[i].childNodes[0].childNodes[0]).prop("checked", false);
			}
	}
}